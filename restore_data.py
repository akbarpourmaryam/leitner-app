#!/usr/bin/env python3
"""
Restore utility for Leitner App
Restores data from CSV backup files
"""

import sqlite3
import csv
import os
import sys
from datetime import datetime

DATABASE = "db.sqlite3"
BACKUP_DIR = "backups"

def list_available_backups():
    """List all available backups"""
    if not os.path.exists(BACKUP_DIR):
        print("❌ No backups directory found.")
        return []
    
    backups = [d for d in os.listdir(BACKUP_DIR) if d.startswith("backup_") and os.path.isdir(os.path.join(BACKUP_DIR, d))]
    backups.sort(reverse=True)
    return backups

def restore_from_backup(backup_name):
    """Restore data from a specific backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup '{backup_name}' not found.")
        return False
    
    users_file = os.path.join(backup_path, "users.csv")
    cards_file = os.path.join(backup_path, "cards.csv")
    
    if not os.path.exists(users_file) or not os.path.exists(cards_file):
        print(f"❌ Backup files not found in '{backup_name}'.")
        return False
    
    # Confirm before proceeding
    print(f"\n⚠️  WARNING: This will replace your current data!")
    print(f"Restoring from: {backup_name}")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Restore cancelled.")
        return False
    
    # Backup current database first
    if os.path.exists(DATABASE):
        backup_current = f"{DATABASE}.before-restore-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(DATABASE, backup_current)
        print(f"📦 Current database backed up to: {backup_current}")
    
    # Create new database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
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
    
    # Restore users
    print("📥 Restoring users...")
    with open(users_file, 'r') as f:
        reader = csv.DictReader(f)
        user_count = 0
        for row in reader:
            # Note: We can't restore password_hash from CSV for security
            # You'll need to reset passwords after restore
            print(f"⚠️  Note: User '{row['email']}' will need to re-register (passwords not backed up for security)")
            user_count += 1
    
    # Restore cards
    print("📥 Restoring cards...")
    with open(cards_file, 'r') as f:
        reader = csv.DictReader(f)
        card_count = 0
        for row in reader:
            cursor.execute("""
                INSERT INTO cards (id, user_id, title, link, idea, solved_date, 
                                 leitner_box, next_review, last_reviewed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['id'], row['user_id'], row['title'], row['link'],
                row['idea'] if row['idea'] else None,
                row['solved_date'], row['leitner_box'], row['next_review'],
                row['last_reviewed'] if row['last_reviewed'] else None,
                row['created_at']
            ))
            card_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Restore completed successfully!")
    print(f"📊 Restored {card_count} cards")
    print(f"\n⚠️  IMPORTANT: You'll need to re-register your account")
    print(f"   Use the same email as before: check {users_file}")
    
    return True

def main():
    print("🔄 Leitner App - Data Restore Utility")
    print("=" * 50)
    
    backups = list_available_backups()
    
    if not backups:
        print("\n❌ No backups found.")
        print("💡 Create backups using: python backup_data.py")
        return
    
    print(f"\n📦 Available backups ({len(backups)}):\n")
    
    for i, backup in enumerate(backups, 1):
        timestamp = backup.replace("backup_", "")
        try:
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {i}. {formatted}")
        except:
            print(f"  {i}. {backup}")
    
    print(f"\n{'='*50}")
    
    if len(sys.argv) > 1:
        # Backup name provided as argument
        backup_name = sys.argv[1]
        if not backup_name.startswith("backup_"):
            # Try to find by number
            try:
                idx = int(backup_name) - 1
                if 0 <= idx < len(backups):
                    backup_name = backups[idx]
                else:
                    print(f"❌ Invalid backup number: {backup_name}")
                    return
            except ValueError:
                print(f"❌ Invalid backup: {backup_name}")
                return
    else:
        # Interactive mode
        choice = input(f"\nEnter backup number to restore (1-{len(backups)}) or 'q' to quit: ")
        
        if choice.lower() == 'q':
            print("👋 Cancelled.")
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(backups):
                backup_name = backups[idx]
            else:
                print("❌ Invalid selection.")
                return
        except ValueError:
            print("❌ Invalid input.")
            return
    
    restore_from_backup(backup_name)

if __name__ == "__main__":
    main()

