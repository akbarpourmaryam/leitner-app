# Test Mode Guide - SQLite Setup

## ✅ You're in Test Mode!

Perfect for:
- Personal testing
- Learning and experimentation
- Up to 10 users
- No production data yet

---

## 📥 How to Backup Your Data

### When You Have Data to Backup:

**Run this command weekly:**

```bash
cd /Users/maryamakbarpour/Desktop/leitner_app
python3 backup_data.py
```

**What it does:**
- Creates a timestamped folder in `backups/`
- Exports users to `users.csv`
- Exports cards to `cards.csv`
- Keeps all your data safe!

**List all backups:**
```bash
python3 backup_data.py list
```

### Store Backups Safely:

After running the backup, upload the `backups/` folder to:
- ✅ Google Drive
- ✅ Dropbox
- ✅ iCloud
- ✅ External hard drive
- ✅ GitHub (private repository)

**Set a reminder:** Backup every Sunday evening!

---

## 🚀 Running Your App Locally

**Start the app:**
```bash
cd /Users/maryamakbarpour/Desktop/leitner_app
./quickstart.sh
```

Or manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="test-secret-key"
python app.py
```

Then open: http://localhost:5000

---

## 📊 Current Limitations (Test Mode)

| Feature | Limit | Why |
|---------|-------|-----|
| **Users** | Best for 1-10 | SQLite locks on writes |
| **Concurrent access** | 1-3 users at once | Single file database |
| **Data persistence** | ⚠️ Can be lost on Render | No automatic backups |
| **Performance** | Fast for small datasets | Slows with 1000+ cards |

---

## ⚠️ When to Migrate to PostgreSQL

You should migrate when:

### Scenario 1: Growing Users
- ✅ You have 10+ registered users
- ✅ More than 3 people use it at the same time
- ✅ Getting timeout errors

### Scenario 2: Important Data
- ✅ Your data is valuable (can't afford to lose it)
- ✅ Other people depend on your app
- ✅ Would be upset if all data was deleted

### Scenario 3: Production Ready
- ✅ Want to make it public
- ✅ Planning to grow to 100+ users
- ✅ Need reliability and uptime

### Scenario 4: Performance Issues
- ✅ App is slow
- ✅ Database locked errors
- ✅ Timeout messages

**When any of these happen → Migrate to PostgreSQL!**

---

## 🎯 Test Mode Checklist

### Setup ✓
- [x] App deployed to Render
- [x] Works on your computer
- [x] Can add/edit/review problems
- [x] Backup script ready

### Weekly Tasks
- [ ] Backup data (run `python3 backup_data.py`)
- [ ] Upload backups to cloud storage
- [ ] Check app is working on Render
- [ ] Monitor for errors

### Before Sharing with Others
- [ ] Test with 2-3 people first
- [ ] Have recent backup
- [ ] Warn users data might be lost
- [ ] Plan PostgreSQL migration

---

## 💾 Backup Schedule Recommendation

### For Personal Use (Just You):
- **Backup:** Once a week
- **Risk:** Low (only your data)
- **Storage:** Google Drive or Dropbox

### For Testing with Friends (2-5 Users):
- **Backup:** Twice a week
- **Risk:** Moderate (friends' data)
- **Storage:** 2 places (cloud + local)

### For Small Group (5-10 Users):
- **Backup:** Daily
- **Risk:** High (many people's data)
- **Storage:** 3 places
- **Action:** Plan PostgreSQL migration soon

---

## 🔄 Quick Migration Path (When Ready)

When you're ready to migrate, I've already prepared:

1. **PRODUCTION_GUIDE.md** - Full migration guide
2. **app_postgresql.py** - PostgreSQL-ready code
3. **Migration instructions** - Step-by-step

**Just let me know and I'll help you migrate in ~30 minutes!**

---

## 📱 Current App URL

Your app is deployed at:
**https://[your-app-name].onrender.com**

(Check your Render dashboard for the exact URL)

---

## 🆘 If Something Goes Wrong

### App Crashes on Render
1. Check Render logs
2. Redeploy from dashboard
3. May lose data (no backup on Render with SQLite)

### Data Lost
1. Check your `backups/` folder
2. If you have backup → restore it
3. If no backup → start fresh (why backups are important!)

### Performance Issues
1. Check number of cards (SQLite slows with 1000+)
2. Check concurrent users (SQLite doesn't handle many)
3. Consider PostgreSQL migration

---

## 💡 Pro Tips for Test Mode

1. **Backup Before Changes**
   - Before editing code → backup
   - Before redeploying → backup
   - Before sharing with others → backup

2. **Test Locally First**
   - Try changes on localhost
   - Make sure it works
   - Then deploy to Render

3. **Keep It Small**
   - Don't add 1000+ problems yet
   - Invite 1-2 friends max
   - Test features thoroughly

4. **Monitor Usage**
   - Check Render logs regularly
   - Watch for errors
   - Notice slowdowns

5. **Plan for Growth**
   - When ready to grow → migrate
   - Don't wait until problems occur
   - Easier to migrate early

---

## 📊 What You Have Now

**GitHub Repository:**
- ✅ Full source code
- ✅ Production guide (when ready)
- ✅ PostgreSQL support (when ready)
- ✅ Backup scripts

**Local Files:**
- ✅ `app.py` - Main application (SQLite)
- ✅ `backup_data.py` - Backup utility
- ✅ `app_postgresql.py` - PostgreSQL version (future)
- ✅ `PRODUCTION_GUIDE.md` - Migration guide

**Deployment:**
- ✅ Render web service
- ✅ GitHub integration
- ✅ Auto-deploy on push

---

## ✨ Enjoy Test Mode!

You're all set for testing! Remember:

- 👍 Great for personal use
- 👍 Perfect for learning
- 👍 Good for small testing groups
- ⚠️ Not for production with many users
- 💾 Backup regularly!

When you're ready to scale or go production → just ask for the PostgreSQL migration!

---

## 🙋 Questions?

- **"How do I backup?"** → Run `python3 backup_data.py`
- **"When to migrate?"** → When you have 10+ users or valuable data
- **"Is test mode safe?"** → Yes, but backup regularly!
- **"Can I use this long-term?"** → For personal use, yes. For many users, no.

Happy testing! 🚀

