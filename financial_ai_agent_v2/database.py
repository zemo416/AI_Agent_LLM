"""
Database module for Financial AI Assistant
Handles all SQLite database operations
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class FinancialDatabase:
    """SQLite database manager for financial data"""

    def __init__(self, db_path: str = "financial_data.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def create_tables(self):
        """Create necessary tables if they don't exist"""

        # Main financial records table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                income REAL NOT NULL,
                fixed_expenses REAL NOT NULL,
                saving_goal REAL NOT NULL,
                remaining REAL NOT NULL,
                risk_level TEXT,
                savings_ratio REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create index on user_id for faster queries
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id
            ON financial_records(user_id)
        """)

        # Expense breakdown table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expense_breakdown (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (record_id) REFERENCES financial_records (id)
            )
        """)

        # AI analysis results table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                analysis_text TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (record_id) REFERENCES financial_records (id)
            )
        """)

        # Messages/flags table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS record_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                flag TEXT,
                FOREIGN KEY (record_id) REFERENCES financial_records (id)
            )
        """)

        # User profiles table for comprehensive user data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
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

        # Create index on user_id for fast profile lookups
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id
            ON user_profiles(user_id)
        """)

        self.conn.commit()

    def insert_financial_record(self, result: Dict, user_id: str) -> int:
        """
        Insert a new financial record for a specific user
        Returns: record_id
        """
        try:
            # Insert main record with user_id
            self.cursor.execute("""
                INSERT INTO financial_records
                (user_id, timestamp, income, fixed_expenses, saving_goal, remaining, risk_level, savings_ratio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                result.get('timestamp', datetime.now().isoformat()),
                result['income'],
                result['fixed'],
                result['goal'],
                result['remaining'],
                result.get('risk'),
                result.get('ratio')
            ))

            record_id = self.cursor.lastrowid

            # Insert messages
            for message in result.get('messages', []):
                for flag in result.get('flags', set()):
                    self.cursor.execute("""
                        INSERT INTO record_messages (record_id, message, flag)
                        VALUES (?, ?, ?)
                    """, (record_id, message, flag))
                    break  # Only insert one flag per message
                else:
                    # If no flags, insert message without flag
                    self.cursor.execute("""
                        INSERT INTO record_messages (record_id, message, flag)
                        VALUES (?, ?, ?)
                    """, (record_id, message, None))

            # Insert expense breakdown if available
            if 'expense_breakdown' in result:
                for category, amount in result['expense_breakdown'].items():
                    self.cursor.execute("""
                        INSERT INTO expense_breakdown (record_id, category, amount)
                        VALUES (?, ?, ?)
                    """, (record_id, category, amount))

            self.conn.commit()
            return record_id

        except Exception as e:
            print(f"Error inserting record: {e}")
            self.conn.rollback()
            return -1

    def insert_ai_analysis(self, record_id: int, analysis_text: str):
        """Insert AI analysis for a record"""
        try:
            self.cursor.execute("""
                INSERT INTO ai_analysis (record_id, analysis_text)
                VALUES (?, ?)
            """, (record_id, analysis_text))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting AI analysis: {e}")
            return False

    def get_all_records(self, user_id: str = None) -> List[Dict]:
        """Retrieve all financial records for a specific user"""
        try:
            if user_id:
                self.cursor.execute("""
                    SELECT * FROM financial_records
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                """, (user_id,))
            else:
                # For backwards compatibility, return all records if no user_id
                self.cursor.execute("""
                    SELECT * FROM financial_records
                    ORDER BY created_at DESC
                """)

            rows = self.cursor.fetchall()
            records = []

            for row in rows:
                record = dict(row)

                # Get messages for this record
                self.cursor.execute("""
                    SELECT message, flag FROM record_messages
                    WHERE record_id = ?
                """, (record['id'],))

                messages_rows = self.cursor.fetchall()
                record['messages'] = [msg['message'] for msg in messages_rows]
                record['flags'] = set([msg['flag'] for msg in messages_rows if msg['flag']])

                # Get expense breakdown
                self.cursor.execute("""
                    SELECT category, amount FROM expense_breakdown
                    WHERE record_id = ?
                """, (record['id'],))

                expenses_rows = self.cursor.fetchall()
                if expenses_rows:
                    record['expense_breakdown'] = {
                        exp['category']: exp['amount'] for exp in expenses_rows
                    }

                # Rename fields to match original format
                record['fixed'] = record.pop('fixed_expenses')
                record['goal'] = record.pop('saving_goal')
                record['risk'] = record.pop('risk_level')
                record['ratio'] = record.pop('savings_ratio')

                records.append(record)

            return records

        except Exception as e:
            print(f"Error retrieving records: {e}")
            return []

    def get_record_by_id(self, record_id: int) -> Optional[Dict]:
        """Retrieve a specific record by ID"""
        try:
            self.cursor.execute("""
                SELECT * FROM financial_records
                WHERE id = ?
            """, (record_id,))

            row = self.cursor.fetchone()
            if not row:
                return None

            record = dict(row)

            # Get messages
            self.cursor.execute("""
                SELECT message, flag FROM record_messages
                WHERE record_id = ?
            """, (record_id,))

            messages_rows = self.cursor.fetchall()
            record['messages'] = [msg['message'] for msg in messages_rows]
            record['flags'] = set([msg['flag'] for msg in messages_rows if msg['flag']])

            # Get expense breakdown
            self.cursor.execute("""
                SELECT category, amount FROM expense_breakdown
                WHERE record_id = ?
            """, (record_id,))

            expenses_rows = self.cursor.fetchall()
            if expenses_rows:
                record['expense_breakdown'] = {
                    exp['category']: exp['amount'] for exp in expenses_rows
                }

            # Get AI analysis
            self.cursor.execute("""
                SELECT analysis_text FROM ai_analysis
                WHERE record_id = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (record_id,))

            ai_row = self.cursor.fetchone()
            if ai_row:
                record['ai_analysis'] = ai_row['analysis_text']

            return record

        except Exception as e:
            print(f"Error retrieving record: {e}")
            return None

    def get_records_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Retrieve records within a date range"""
        try:
            self.cursor.execute("""
                SELECT * FROM financial_records
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (start_date, end_date))

            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error retrieving records by date: {e}")
            return []

    def delete_record(self, record_id: int) -> bool:
        """Delete a financial record and its related data"""
        try:
            # Delete related messages
            self.cursor.execute("DELETE FROM record_messages WHERE record_id = ?", (record_id,))

            # Delete related expense breakdown
            self.cursor.execute("DELETE FROM expense_breakdown WHERE record_id = ?", (record_id,))

            # Delete related AI analysis
            self.cursor.execute("DELETE FROM ai_analysis WHERE record_id = ?", (record_id,))

            # Delete main record
            self.cursor.execute("DELETE FROM financial_records WHERE id = ?", (record_id,))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error deleting record: {e}")
            self.conn.rollback()
            return False

    def delete_all_records(self, user_id: str = None) -> bool:
        """Delete all financial records for a specific user"""
        try:
            if user_id:
                # Get all record IDs for this user
                self.cursor.execute("SELECT id FROM financial_records WHERE user_id = ?", (user_id,))
                record_ids = [row[0] for row in self.cursor.fetchall()]

                # Delete related data
                for record_id in record_ids:
                    self.cursor.execute("DELETE FROM record_messages WHERE record_id = ?", (record_id,))
                    self.cursor.execute("DELETE FROM expense_breakdown WHERE record_id = ?", (record_id,))
                    self.cursor.execute("DELETE FROM ai_analysis WHERE record_id = ?", (record_id,))

                # Delete main records
                self.cursor.execute("DELETE FROM financial_records WHERE user_id = ?", (user_id,))
            else:
                # Delete all records (for backwards compatibility)
                self.cursor.execute("DELETE FROM record_messages")
                self.cursor.execute("DELETE FROM expense_breakdown")
                self.cursor.execute("DELETE FROM ai_analysis")
                self.cursor.execute("DELETE FROM financial_records")

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error deleting all records: {e}")
            self.conn.rollback()
            return False

    def get_statistics(self, user_id: str = None) -> Dict:
        """Get statistical summary of records for a specific user"""
        try:
            if user_id:
                self.cursor.execute("""
                    SELECT
                        COUNT(*) as total_records,
                        AVG(income) as avg_income,
                        AVG(fixed_expenses) as avg_expenses,
                        AVG(remaining) as avg_remaining,
                        AVG(savings_ratio) as avg_savings_ratio,
                        MIN(timestamp) as first_record,
                        MAX(timestamp) as last_record
                    FROM financial_records
                    WHERE user_id = ?
                """, (user_id,))
            else:
                self.cursor.execute("""
                    SELECT
                        COUNT(*) as total_records,
                        AVG(income) as avg_income,
                        AVG(fixed_expenses) as avg_expenses,
                        AVG(remaining) as avg_remaining,
                        AVG(savings_ratio) as avg_savings_ratio,
                        MIN(timestamp) as first_record,
                        MAX(timestamp) as last_record
                    FROM financial_records
                """)

            row = self.cursor.fetchone()
            return dict(row) if row else {}

        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}

    def upsert_user_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Insert or update user profile with completion tracking"""
        try:
            # Calculate completion percentage
            total_fields = 14
            filled_fields = sum(1 for v in profile_data.values() if v is not None and v != '')
            completion_pct = int((filled_fields / total_fields) * 100)
            profile_completed = 1 if completion_pct >= 80 else 0

            # Check if profile exists
            self.cursor.execute("SELECT id FROM user_profiles WHERE user_id = ?", (user_id,))
            exists = self.cursor.fetchone()

            if exists:
                # Update existing profile
                self.cursor.execute("""
                    UPDATE user_profiles SET
                        age = ?, occupation = ?, industry = ?,
                        health_status = ?, medical_history = ?, insurance_type = ?,
                        work_hours_per_week = ?, work_intensity = ?, job_type = ?,
                        marital_status = ?, number_of_dependents = ?, family_environment = ?,
                        employment_type = ?, income_stability = ?,
                        profile_completed = ?, completion_percentage = ?,
                        updated_at = ?
                    WHERE user_id = ?
                """, (
                    profile_data.get('age'),
                    profile_data.get('occupation'),
                    profile_data.get('industry'),
                    profile_data.get('health_status'),
                    profile_data.get('medical_history'),
                    profile_data.get('insurance_type'),
                    profile_data.get('work_hours_per_week'),
                    profile_data.get('work_intensity'),
                    profile_data.get('job_type'),
                    profile_data.get('marital_status'),
                    profile_data.get('number_of_dependents'),
                    profile_data.get('family_environment'),
                    profile_data.get('employment_type'),
                    profile_data.get('income_stability'),
                    profile_completed,
                    completion_pct,
                    datetime.now().isoformat(),
                    user_id
                ))
            else:
                # Insert new profile
                self.cursor.execute("""
                    INSERT INTO user_profiles (
                        user_id, age, occupation, industry,
                        health_status, medical_history, insurance_type,
                        work_hours_per_week, work_intensity, job_type,
                        marital_status, number_of_dependents, family_environment,
                        employment_type, income_stability,
                        profile_completed, completion_percentage
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    profile_data.get('age'),
                    profile_data.get('occupation'),
                    profile_data.get('industry'),
                    profile_data.get('health_status'),
                    profile_data.get('medical_history'),
                    profile_data.get('insurance_type'),
                    profile_data.get('work_hours_per_week'),
                    profile_data.get('work_intensity'),
                    profile_data.get('job_type'),
                    profile_data.get('marital_status'),
                    profile_data.get('number_of_dependents'),
                    profile_data.get('family_environment'),
                    profile_data.get('employment_type'),
                    profile_data.get('income_stability'),
                    profile_completed,
                    completion_pct
                ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error upserting profile: {e}")
            self.conn.rollback()
            return False

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Retrieve user profile by user_id"""
        try:
            self.cursor.execute("""
                SELECT * FROM user_profiles WHERE user_id = ?
            """, (user_id,))

            row = self.cursor.fetchone()
            return dict(row) if row else None

        except Exception as e:
            print(f"Error retrieving profile: {e}")
            return None

    def delete_user_profile(self, user_id: str) -> bool:
        """Delete user profile"""
        try:
            self.cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error deleting profile: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Singleton instance
_db_instance = None

def get_database() -> FinancialDatabase:
    """Get or create database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = FinancialDatabase()
    return _db_instance
