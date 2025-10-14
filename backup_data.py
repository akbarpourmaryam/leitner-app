#!/usr/bin/env python3
"""
Simple backup utility for Leitner App
Exports all data to CSV files for safe keeping
"""

import sqlite3
import csv
from datetime import datetime
import os

DATABASE = "db.sqlite3"
BACKUP_DIR = "backups"

def create_backup():
    """Export all data to CSV files"""
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # Create timestamped backup folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(backup_folder)
    
    # Connect to database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Backup users table
    print("📥 Backing up users...")
    cursor.execute("SELECT id, email, created_at FROM users")
    users = cursor.fetchall()
    
    with open(os.path.join(backup_folder, "users.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email", "created_at"])
        for user in users:
            writer.writerow([user["id"], user["email"], user["created_at"]])
    
    print(f"✅ Backed up {len(users)} users")
    
    # Backup cards table
    print("📥 Backing up cards...")
    cursor.execute("""
        SELECT id, user_id, title, link, idea, solved_date, 
               leitner_box, next_review, last_reviewed, created_at
        FROM cards
    """)
    cards = cursor.fetchall()
    
    with open(os.path.join(backup_folder, "cards.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "user_id", "title", "link", "idea", "solved_date",
            "leitner_box", "next_review", "last_reviewed", "created_at"
        ])
        for card in cards:
            writer.writerow([
                card["id"], card["user_id"], card["title"], card["link"],
                card["idea"], card["solved_date"], card["leitner_box"],
                card["next_review"], card["last_reviewed"], card["created_at"]
            ])
    
    print(f"✅ Backed up {len(cards)} cards")
    
    conn.close()
    
    print(f"\n🎉 Backup completed successfully!")
    print(f"📁 Location: {backup_folder}")
    print(f"\nFiles created:")
    print(f"  - users.csv ({len(users)} records)")
    print(f"  - cards.csv ({len(cards)} records)")
    
    return backup_folder

def list_backups():
    """List all available backups"""
    if not os.path.exists(BACKUP_DIR):
        print("No backups found.")
        return
    
    backups = [d for d in os.listdir(BACKUP_DIR) if d.startswith("backup_")]
    if not backups:
        print("No backups found.")
        return
    
    print(f"\n📦 Available backups ({len(backups)}):")
    for backup in sorted(backups, reverse=True):
        backup_path = os.path.join(BACKUP_DIR, backup)
        timestamp = backup.replace("backup_", "")
        # Format timestamp nicely
        dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(f"  - {formatted} ({backup})")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_backups()
    else:
        create_backup()
        print("\n💡 Tip: Upload the backup folder to Dropbox/Google Drive for safety!")
        print("💡 Run 'python backup_data.py list' to see all backups")

