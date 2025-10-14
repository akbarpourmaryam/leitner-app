# 30-Day Testing Plan with Data Safety

## 🎯 Goal
Test the Leitner app for 30 days, track issues, and **keep all your data safe**.

---

## 🛡️ Data Protection Strategy

### Weekly Backup Schedule

**Set these reminders on your phone/calendar:**

```
Week 1: October 21 - Backup Sunday
Week 2: October 28 - Backup Sunday  
Week 3: November 4 - Backup Sunday
Week 4: November 11 - Backup Sunday
Final: November 14 - Final Backup
```

### How to Backup (Takes 2 minutes)

**If you have data locally:**
```bash
cd /Users/maryamakbarpour/Desktop/leitner_app
python3 backup_data.py
```

**If data is only on Render:**
You'll need to download it. I'll show you how below.

---

## 📥 Backup Methods

### Method 1: If Testing Locally

**Advantages:**
- ✅ Full control over data
- ✅ Easy backups
- ✅ Can copy database file directly
- ✅ No deployment needed for changes

**How to:**
1. Run app locally: `./quickstart.sh`
2. Use at http://localhost:5000
3. Backup weekly: `python3 backup_data.py`
4. Upload backups folder to Google Drive/Dropbox

### Method 2: If Testing on Render

**Advantages:**
- ✅ Access from anywhere
- ✅ Test production environment
- ✅ Share with friends to test

**Risks:**
- ⚠️ Data can be lost on redeploy
- ⚠️ Need regular backups

**Protection:**
1. Don't redeploy during test period
2. Export data weekly (manual download)
3. Keep backups in 2 places

### Method 3: Hybrid (Recommended!)

**Best of both worlds:**

1. **Use Render for daily access** (convenience)
2. **Backup locally once a week:**
   - Add problems throughout the week on Render
   - Every Sunday, export and save locally
   - Keep local copy as backup

---

## 📊 30-Day Test Tracking

### What to Track

Create a simple notes file to track:

**Week 1 (Oct 14-20):**
- [ ] Added X problems
- [ ] Reviewed Y problems
- Issues found:
  - (note any bugs, confusing UI, etc.)
- What I liked:
  - (positive feedback)

**Week 2 (Oct 21-27):**
- [ ] Added X problems
- [ ] Reviewed Y problems
- [ ] Backed up data ✓
- Issues found:
- What I liked:

**Week 3 (Oct 28 - Nov 3):**
- [ ] Added X problems
- [ ] Reviewed Y problems
- [ ] Backed up data ✓
- Issues found:
- What I liked:

**Week 4 (Nov 4-10):**
- [ ] Added X problems
- [ ] Reviewed Y problems
- [ ] Backed up data ✓
- Issues found:
- What I liked:

**Final Week (Nov 11-14):**
- [ ] Final testing
- [ ] Backed up data ✓
- [ ] Compiled feedback

---

## 🐛 Issues to Look For

### Functionality Issues
- [ ] Problems not adding correctly
- [ ] Title extraction failing
- [ ] Duplicate detection not working
- [ ] Review timing incorrect
- [ ] Box progression issues

### UX Issues
- [ ] Confusing interface
- [ ] Hard to find features
- [ ] Too many clicks
- [ ] Information not clear
- [ ] Mobile usability problems

### Feature Requests
- [ ] Missing features you need
- [ ] Nice-to-have improvements
- [ ] Workflow optimizations

---

## 💾 Backup Instructions

### Automatic Backup Script

**Run this every Sunday:**

```bash
cd /Users/maryamakbarpour/Desktop/leitner_app
python3 backup_data.py
```

**Output:**
```
📥 Backing up users...
✅ Backed up 1 users
📥 Backing up cards...
✅ Backed up 25 cards

🎉 Backup completed successfully!
📁 Location: backups/backup_20251014_143025
```

### Manual Database Backup

**Even simpler - just copy the file:**

```bash
# Copy database file
cp db.sqlite3 db.backup-$(date +%Y%m%d).sqlite3

# Or compress it
zip db-backup-$(date +%Y%m%d).zip db.sqlite3
```

### Upload to Cloud

**After backup, upload to:**

1. **Google Drive:**
   - Drag backup folder to Drive
   - Keep last 4 weeks

2. **Dropbox:**
   - Copy to Dropbox folder
   - Auto-syncs

3. **GitHub (Private Repo):**
   ```bash
   # Create private backup repo
   # Upload backup files
   # Keep version history
   ```

---

## 🔄 If You Lose Data

### Restore from Backup

**From CSV backup:**
```bash
# Import users.csv and cards.csv back into database
# (I can create a restore script if needed)
```

**From database file:**
```bash
# Just replace db.sqlite3 with backup file
cp db.backup-20251014.sqlite3 db.sqlite3
```

---

## 📱 Testing Checklist

### Day 1 Setup
- [ ] Deploy to Render (or run locally)
- [ ] Register account
- [ ] Add first 3-5 problems
- [ ] Test all features
- [ ] Create backup

### Daily Usage (Days 2-30)
- [ ] Add problems as you solve them
- [ ] Review when due
- [ ] Test AI improvement (if enabled)
- [ ] Note any issues

### Weekly Tasks
- [ ] Sunday: Create backup
- [ ] Upload backup to cloud
- [ ] Review what worked/didn't work
- [ ] Track issues found

### End of Test (Day 30)
- [ ] Final backup
- [ ] Compile all feedback
- [ ] Decide: continue using or improve first?
- [ ] Share feedback with me (optional!)

---

## 🎯 Success Criteria

After 30 days, you should be able to answer:

1. **Does it help my LeetCode practice?**
   - Are reviews timed well?
   - Do I remember problems better?
   - Is it worth the effort?

2. **Is the workflow smooth?**
   - Easy to add problems?
   - Quick to review?
   - Not too many clicks?

3. **Any critical issues?**
   - Bugs that block usage?
   - Confusing features?
   - Missing essentials?

4. **Would I keep using it?**
   - After fixing issues
   - As-is
   - Not useful

---

## 🚀 Starting Your Test

### Option A: Test Locally (Safest)

```bash
cd /Users/maryamakbarpour/Desktop/leitner_app

# Start app
./quickstart.sh

# Open browser
open http://localhost:5000

# When done, backup
python3 backup_data.py
```

**Pros:**
- ✅ Full control
- ✅ No data loss risk
- ✅ Easy backups
- ✅ Free

**Cons:**
- ❌ Only works on your computer
- ❌ Need to start server each time

### Option B: Test on Render (More Convenient)

```bash
# Already deployed!
# Just use the URL from Render dashboard
```

**Pros:**
- ✅ Access anywhere
- ✅ Always running
- ✅ Production-like testing

**Cons:**
- ⚠️ Need regular backups
- ⚠️ Data at risk if redeployed

### Option C: Both! (Recommended)

1. **Primary use: Render** (daily access)
2. **Backup: Local** (run backup script weekly)
3. **Best of both worlds!**

---

## 📝 Feedback Template

**After 30 days, answer these:**

### What Worked Well:
1. 
2. 
3. 

### Issues Found:
1. 
2. 
3. 

### Feature Requests:
1. 
2. 
3. 

### Would I recommend to others?
- Yes / No
- Why:

### Overall rating: __/10

---

## 💡 Tips for Successful Test

**1. Use it consistently:**
- Add problems right after solving
- Review when notifications show up
- Don't skip reviews

**2. Be honest about issues:**
- Note frustrations immediately
- Track time spent on tasks
- Compare to your current method

**3. Test all features:**
- Add problems
- Edit problems
- Review pass/fail
- Search function
- AI improvement (if enabled)
- Duplicate detection

**4. Backup religiously:**
- Set phone reminder
- Make it a Sunday routine
- Takes 2 minutes
- Saves hours of re-entry

---

## 🎓 After 30 Days

### If it's useful:
1. Keep using it!
2. Migrate to PostgreSQL for safety
3. Share improvements you want
4. Continue with confidence

### If issues found:
1. Share feedback
2. I'll fix the issues
3. Test for another week
4. Decide again

### If not useful:
1. Export your data (you have backups!)
2. No harm done
3. At least you tried!
4. Use what works for you

---

## 🆘 Emergency Contacts

**If you need help during testing:**

1. **Data loss:** Use your most recent backup
2. **Bugs:** Note them down, continue testing
3. **Questions:** Check documentation files
4. **Critical issue:** Stop using, restore backup

---

## ✅ Ready to Start?

**Quick Start:**

1. **Now:** Set up 4 Sunday reminders on phone
2. **Today:** Add your first 5 problems
3. **Tomorrow:** Test the review feature (they'll be due!)
4. **This Sunday:** First backup
5. **30 days later:** Review and decide!

**Good luck with your testing!** 🚀

Remember: **Backup = Peace of mind**

