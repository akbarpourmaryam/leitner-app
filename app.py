
import os
import sqlite3
import re
from datetime import datetime, timedelta, date
from flask import Flask, g, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Config ---
DATABASE = os.path.join(os.path.dirname(__file__), "db.sqlite3")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
LEITNER_SCHEDULE = {1:1, 2:3, 3:7, 4:14, 5:30}

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY, 
    DATABASE=DATABASE,
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_TIME_LIMIT=None  # CSRF tokens don't expire
)

# Enable CSRF protection
csrf = CSRFProtect(app)

# --- DB helpers ---
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(
        """
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
        """
    )
    db.commit()

@app.before_request
def before_request():
    init_db()

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return dict(current_user=current_user())

# --- Validation utils ---
def is_valid_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Check if password meets minimum requirements"""
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
    return db.execute("SELECT id, email FROM users WHERE id=?", (uid,)).fetchone()

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
        
        # Validation
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
        try:
            db.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, generate_password_hash(password)),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
            return render_template("register.html")
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def compute_next_review(solved_date: date, box: int) -> date:
    days = LEITNER_SCHEDULE.get(box, 1)
    return solved_date + timedelta(days=days)

@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    user = current_user()
    q = request.args.get("q","").strip()
    if q:
        cards = db.execute(
            """SELECT * FROM cards WHERE user_id=? AND (title LIKE ? OR idea LIKE ?) 
               ORDER BY created_at DESC""",
            (user["id"], f"%{q}%", f"%{q}%"),
        ).fetchall()
    else:
        cards = db.execute(
            "SELECT * FROM cards WHERE user_id=? ORDER BY created_at DESC",
            (user["id"],),
        ).fetchall()

    # stats
    total = db.execute("SELECT COUNT(*) c FROM cards WHERE user_id=?", (user["id"],)).fetchone()["c"]
    due_today = db.execute(
        "SELECT COUNT(*) c FROM cards WHERE user_id=? AND date(next_review) <= date('now')",
        (user["id"],),
    ).fetchone()["c"]
    by_box = db.execute(
        "SELECT leitner_box, COUNT(*) c FROM cards WHERE user_id=? GROUP BY leitner_box",
        (user["id"],),
    ).fetchall()
    box_counts = {row["leitner_box"]: row["c"] for row in by_box}

    return render_template("dashboard.html", cards=cards, total=total, due_today=due_today, box_counts=box_counts, q=q)

@app.route("/add", methods=["POST"])
@login_required
def add():
    user = current_user()
    title = request.form.get("title","").strip()
    link = request.form.get("link","").strip()
    idea = request.form.get("idea","").strip()
    solved_date_str = request.form.get("solved_date","").strip()
    if not solved_date_str:
        solved_date = date.today()
    else:
        solved_date = datetime.fromisoformat(solved_date_str).date()
    box = int(request.form.get("leitner_box","1"))
    if box < 1: box = 1
    if box > 5: box = 5
    next_review = compute_next_review(solved_date, box)

    if not title:
        flash("Title is required.", "error")
        return redirect(url_for("dashboard"))
    db = get_db()
    db.execute(
        """INSERT INTO cards (user_id, title, link, idea, solved_date, leitner_box, next_review)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user["id"], title, link, idea, solved_date, box, next_review),
    )
    db.commit()
    flash("Card added.", "success")
    return redirect(url_for("dashboard"))

@app.route("/review")
@login_required
def review():
    user = current_user()
    db = get_db()
    cards = db.execute(
        """SELECT * FROM cards WHERE user_id=? AND date(next_review) <= date('now')
           ORDER BY next_review ASC, id ASC""",
        (user["id"],),
    ).fetchall()
    return render_template("review.html", cards=cards)

@app.route("/mark/<int:card_id>/<string:result>", methods=["POST"])
@login_required
def mark(card_id, result):
    user = current_user()
    db = get_db()
    card = db.execute("SELECT * FROM cards WHERE id=? AND user_id=?", (card_id, user["id"])).fetchone()
    if not card:
        flash("Card not found.", "error")
        return redirect(url_for("review"))
    box = card["leitner_box"]
    if result == "pass":
        box = min(5, box + 1)
    else:
        box = 1
    today = date.today()
    next_review = compute_next_review(today, box)
    db.execute(
        "UPDATE cards SET leitner_box=?, last_reviewed=?, next_review=? WHERE id=?",
        (box, today, next_review, card_id),
    )
    db.commit()
    return redirect(url_for("review"))

@app.route("/delete/<int:card_id>", methods=["POST"])
@login_required
def delete(card_id):
    user = current_user()
    db = get_db()
    db.execute("DELETE FROM cards WHERE id=? AND user_id=?", (card_id, user["id"]))
    db.commit()
    flash("Card deleted.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
