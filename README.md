# Leet Leitner - Multi-User Spaced Repetition System

A production-ready web application for tracking LeetCode problems with a **Leitner spaced repetition** system. Supports multiple users with secure authentication.

## ✨ Features

- 🔐 **Multi-user authentication** - Secure registration and login with password hashing
- 📝 **Problem tracking** - Add problems with title, link, idea, and solved date
- 🧠 **Spaced repetition** - Automatic next-review scheduling using Leitner box system (1, 3, 7, 14, 30 days)
- 📊 **Dashboard** - View your stats, search problems, and track progress
- ⏰ **Daily reviews** - See all problems due for review today
- 🛡️ **Security** - CSRF protection, password strength requirements, email validation
- 🎨 **Modern UI** - Clean, responsive design

## 🚀 Quick Start (Local Development)

1. **Clone and setup environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
# Copy the example file
cp env.example .env

# Edit .env and set your SECRET_KEY
# For development:
export SECRET_KEY='your-secret-key-here'
export FLASK_DEBUG=True
```

3. **Run the application:**
```bash
python app.py
# Open http://localhost:5000
```

## 🌐 Deploy to Production

### Option 1: Heroku

1. **Create a Heroku app:**
```bash
heroku create your-app-name
```

2. **Set environment variables:**
```bash
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

3. **Deploy:**
```bash
git push heroku main
```

4. **Open your app:**
```bash
heroku open
```

### Option 2: Render (Free)

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Runtime:** Python 3.11+
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Add environment variable:
   - `SECRET_KEY`: Generate a strong random key (e.g., using `python -c 'import secrets; print(secrets.token_hex(32))'`)
5. Deploy!

### Option 3: Any VPS (DigitalOcean, AWS, etc.)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export SECRET_KEY="your-strong-secret-key"
export PORT=8000
```

3. **Run with gunicorn:**
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

4. **Optional: Use a process manager like systemd or supervisor for production**

## 🔒 Security Features

- ✅ Password hashing using Werkzeug security
- ✅ CSRF protection on all forms
- ✅ Password strength requirements (8+ chars, uppercase, lowercase, number)
- ✅ Email validation
- ✅ Session management
- ✅ User data isolation (users only see their own cards)

## 📝 Password Requirements

When registering, passwords must:
- Be at least 8 characters long
- Contain at least one uppercase letter
- Contain at least one lowercase letter
- Contain at least one number

## 🗄️ Database

- Uses SQLite by default (`db.sqlite3`)
- For production multi-instance deployment, consider migrating to PostgreSQL
- User data is isolated with proper foreign key constraints

## 🛠️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | dev-secret-key | Flask secret key for sessions |
| `FLASK_DEBUG` | No | False | Enable debug mode |
| `PORT` | No | 5000 | Port to run the application |
| `DATABASE` | No | db.sqlite3 | Path to SQLite database |

## 📖 Usage

1. **Register** - Create an account with your email and password
2. **Login** - Sign in to your account
3. **Add problems** - Track LeetCode problems you've solved
4. **Review** - Practice problems that are due for review
5. **Track progress** - Monitor your learning with box statistics

## 🎯 Leitner Box Schedule

| Box | Next Review |
|-----|-------------|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |

When you pass a problem, it moves to the next box. When you fail, it goes back to Box 1.

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

MIT License - Feel free to use and modify as needed.
