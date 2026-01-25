"""
Database migration script to add user_profiles table
Run this once to update existing databases
"""

import sqlite3
import os

def migrate_sqlite():
    """Migrate SQLite database to add user_profiles table"""
    db_path = "financial_data.db"

    if not os.path.exists(db_path):
        print("No SQLite database found. Will be created with correct schema on first run.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='user_profiles'
        """)

        if cursor.fetchone():
            print("user_profiles table already exists in SQLite")
        else:
            # Create table
            cursor.execute("""
                CREATE TABLE user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,

                    -- Demographics
                    age INTEGER,
                    occupation TEXT,
                    industry TEXT,

                    -- Health
                    health_status TEXT,
                    medical_history TEXT,
                    insurance_type TEXT,

                    -- Work
                    work_hours_per_week INTEGER,
                    work_intensity TEXT,
                    job_type TEXT,

                    -- Family
                    marital_status TEXT,
                    number_of_dependents INTEGER DEFAULT 0,
                    family_environment TEXT,

                    -- Financial Context
                    employment_type TEXT,
                    income_stability TEXT,

                    -- Metadata
                    profile_completed INTEGER DEFAULT 0,
                    completion_percentage INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE INDEX idx_user_profiles_user_id
                ON user_profiles(user_id)
            """)

            conn.commit()
            print("Created user_profiles table in SQLite")

        conn.close()

    except Exception as e:
        print(f"SQLite migration error: {e}")

def migrate_postgres():
    """Migrate PostgreSQL database to add user_profiles table"""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("No DATABASE_URL found, skipping PostgreSQL migration")
        return

    try:
        import psycopg2

        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'user_profiles'
            )
        """)

        if cursor.fetchone()[0]:
            print("user_profiles table already exists in PostgreSQL")
        else:
            # Create table
            cursor.execute("""
                CREATE TABLE user_profiles (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT UNIQUE NOT NULL,

                    -- Demographics
                    age INTEGER,
                    occupation TEXT,
                    industry TEXT,

                    -- Health
                    health_status TEXT,
                    medical_history TEXT,
                    insurance_type TEXT,

                    -- Work
                    work_hours_per_week INTEGER,
                    work_intensity TEXT,
                    job_type TEXT,

                    -- Family
                    marital_status TEXT,
                    number_of_dependents INTEGER DEFAULT 0,
                    family_environment TEXT,

                    -- Financial Context
                    employment_type TEXT,
                    income_stability TEXT,

                    -- Metadata
                    profile_completed BOOLEAN DEFAULT FALSE,
                    completion_percentage INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE INDEX idx_user_profiles_user_id
                ON user_profiles(user_id)
            """)

            conn.commit()
            print("Created user_profiles table in PostgreSQL")

        conn.close()

    except ImportError:
        print("psycopg2 not installed, skipping PostgreSQL migration")
    except Exception as e:
        print(f"PostgreSQL migration error: {e}")

if __name__ == "__main__":
    print("Running database migration...")
    migrate_sqlite()
    migrate_postgres()
    print("Migration complete!")
