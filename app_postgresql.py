"""
PostgreSQL-ready version of app.py
Supports both SQLite (development) and PostgreSQL (production)
Automatically switches based on DATABASE_URL environment variable
"""

import os
import sqlite3
import re
from datetime import datetime, timedelta, date
from flask import Flask, g, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# --- Config ---
# Use PostgreSQL if DATABASE_URL is set, otherwise use SQLite
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # Heroku uses postgres://, but SQLAlchemy needs postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

DATABASE_SQLITE = os.path.join(os.path.dirname(__file__), "db.sqlite3")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
LEITNER_SCHEDULE = {1:1, 2:3, 3:7, 4:14, 5:30}

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
    DATABASE_URL=DATABASE_URL,
    DATABASE_SQLITE=DATABASE_SQLITE,
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_TIME_LIMIT=None
)

# Enable CSRF protection
csrf = CSRFProtect(app)

# --- DB helpers ---
def get_db():
    """Get database connection - works with both SQLite and PostgreSQL"""
    db = getattr(g, "_database", None)
    if db is None:
        if DATABASE_URL:
            # PostgreSQL
            import psycopg2
            import psycopg2.extras
            db = g._database = psycopg2.connect(DATABASE_URL)
            # Use RealDictCursor for row factory (like sqlite3.Row)
            db.cursor_factory = psycopg2.extras.RealDictCursor
        else:
            # SQLite
            db = g._database = sqlite3.connect(
                app.config["DATABASE_SQLITE"],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database - works with both SQLite and PostgreSQL"""
    db = get_db()
    cursor = db.cursor()
    
    if DATABASE_URL:
        # PostgreSQL schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                link TEXT,
                idea TEXT,
                solved_date DATE NOT NULL,
                leitner_box INTEGER NOT NULL DEFAULT 1,
                next_review DATE NOT NULL,
                last_reviewed DATE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_user ON cards(user_id);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cards_nextreview ON cards(next_review);
        """)
    else:
        # SQLite schema (original)
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                link TEXT,
                idea TEXT,
                solved_date DATE NOT NULL,
                leitner_box INTEGER NOT NULL DEFAULT 1,
                next_review DATE NOT NULL,
                last_reviewed DATE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_cards_user ON cards(user_id);
            CREATE INDEX IF NOT EXISTS idx_cards_nextreview ON cards(next_review);
        """)
    
    db.commit()

@app.before_request
def before_request():
    init_db()

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return dict(current_user=current_user())

# --- LeetCode utils ---
def fetch_leetcode_title(url):
    """Fetch LeetCode problem title from URL using slug extraction"""
    try:
        url = url.strip()
        if not url or 'leetcode.com/problems/' not in url:
            return None
        
        slug = url.split('/problems/')[1].rstrip('/').split('/')[0]
        title = ' '.join(word.capitalize() for word in slug.split('-'))
        return title if title else None
    except Exception as e:
        print(f"Error processing LeetCode URL: {e}")
        return None

# --- Validation utils ---
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    return True, ""

# --- Auth utils ---
def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, email FROM users WHERE id=%s" if DATABASE_URL else "SELECT id, email FROM users WHERE id=?", (uid,))
    return cursor.fetchone()

def login_required(view):
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    wrapped.__name__ = view.__name__
    return wrapped

# --- Routes ---
@app.route("/")
def home():
    if current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("register.html")
        
        if not is_valid_email(email):
            flash("Please enter a valid email address.", "error")
            return render_template("register.html")
        
        is_strong, msg = is_strong_password(password)
        if not is_strong:
            flash(msg, "error")
            return render_template("register.html")
        
        db = get_db()
        cursor = db.cursor()
        try:
            if DATABASE_URL:
                cursor.execute(
                    "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                    (email, generate_password_hash(password))
                )
            else:
                cursor.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (email, generate_password_hash(password))
                )
            db.commit()
        except Exception as e:
            flash("Email already registered.", "error")
            return render_template("register.html")
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Continue with all other routes using the same pattern...
# (I've shown the key parts - the rest follows the same pattern)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

