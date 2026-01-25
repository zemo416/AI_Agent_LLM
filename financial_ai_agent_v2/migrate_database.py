"""
Database migration script to add user_id column if it doesn't exist
"""

import sqlite3
import os

def migrate_database():
    """Add user_id column to financial_records table if it doesn't exist"""
    db_path = "financial_data.db"

    if not os.path.exists(db_path):
        print("No database file found. Will be created with correct schema.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if user_id column exists
        cursor.execute("PRAGMA table_info(financial_records)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'user_id' not in columns:
            print("Adding user_id column to financial_records table...")

            # Add user_id column with default value
            cursor.execute("""
                ALTER TABLE financial_records
                ADD COLUMN user_id TEXT NOT NULL DEFAULT 'default_user'
            """)

            # Create index on user_id
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id
                ON financial_records(user_id)
            """)

            conn.commit()
            print("Migration completed successfully!")
        else:
            print("user_id column already exists. No migration needed.")

        conn.close()

    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate_database()
