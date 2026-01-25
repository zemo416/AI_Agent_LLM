"""
PostgreSQL Database Module for Financial AI Assistant
Supports cloud databases like Supabase
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class PostgresDatabase:
    """PostgreSQL database manager for financial data"""

    def __init__(self, database_url: str = None):
        """Initialize database connection"""
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                self.database_url,
                cursor_factory=RealDictCursor
            )
            self.conn.autocommit = False
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
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                income DECIMAL(10, 2) NOT NULL,
                fixed_expenses DECIMAL(10, 2) NOT NULL,
                saving_goal DECIMAL(10, 2) NOT NULL,
                remaining DECIMAL(10, 2) NOT NULL,
                risk_level TEXT,
                savings_ratio DECIMAL(5, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                id SERIAL PRIMARY KEY,
                record_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (record_id) REFERENCES financial_records (id) ON DELETE CASCADE
            )
        """)

        # AI analysis results table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id SERIAL PRIMARY KEY,
                record_id INTEGER NOT NULL,
                analysis_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (record_id) REFERENCES financial_records (id) ON DELETE CASCADE
            )
        """)

        # Messages/flags table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS record_messages (
                id SERIAL PRIMARY KEY,
                record_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                flag TEXT,
                FOREIGN KEY (record_id) REFERENCES financial_records (id) ON DELETE CASCADE
            )
        """)

        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
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

            record_id = self.cursor.fetchone()['id']

            # Insert messages
            for message in result.get('messages', []):
                for flag in result.get('flags', set()):
                    self.cursor.execute("""
                        INSERT INTO record_messages (record_id, message, flag)
                        VALUES (%s, %s, %s)
                    """, (record_id, message, flag))
                    break
                else:
                    self.cursor.execute("""
                        INSERT INTO record_messages (record_id, message, flag)
                        VALUES (%s, %s, %s)
                    """, (record_id, message, None))

            # Insert expense breakdown if available
            if 'expense_breakdown' in result:
                for category, amount in result['expense_breakdown'].items():
                    self.cursor.execute("""
                        INSERT INTO expense_breakdown (record_id, category, amount)
                        VALUES (%s, %s, %s)
                    """, (record_id, category, amount))

            self.conn.commit()
            return record_id

        except Exception as e:
            print(f"Error inserting record: {e}")
            self.conn.rollback()
            return -1

    def get_all_records(self, user_id: str = None) -> List[Dict]:
        """Retrieve all financial records for a specific user"""
        try:
            if user_id:
                self.cursor.execute("""
                    SELECT * FROM financial_records
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
            else:
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
                    WHERE record_id = %s
                """, (record['id'],))

                messages_rows = self.cursor.fetchall()
                record['messages'] = [msg['message'] for msg in messages_rows]
                record['flags'] = set([msg['flag'] for msg in messages_rows if msg['flag']])

                # Get expense breakdown
                self.cursor.execute("""
                    SELECT category, amount FROM expense_breakdown
                    WHERE record_id = %s
                """, (record['id'],))

                expenses_rows = self.cursor.fetchall()
                if expenses_rows:
                    record['expense_breakdown'] = {
                        exp['category']: float(exp['amount']) for exp in expenses_rows
                    }

                # Rename fields and convert Decimal to float
                record['fixed'] = float(record.pop('fixed_expenses'))
                record['goal'] = float(record.pop('saving_goal'))
                record['risk'] = record.pop('risk_level')
                record['ratio'] = float(record.pop('savings_ratio')) if record.get('savings_ratio') else None
                record['income'] = float(record['income'])
                record['remaining'] = float(record['remaining'])
                record['timestamp'] = str(record['timestamp'])

                records.append(record)

            return records

        except Exception as e:
            print(f"Error retrieving records: {e}")
            return []

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
                    WHERE user_id = %s
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
            if row:
                result = dict(row)
                # Convert Decimal to float
                for key in ['avg_income', 'avg_expenses', 'avg_remaining', 'avg_savings_ratio']:
                    if result.get(key):
                        result[key] = float(result[key])
                # Convert timestamps to strings
                if result.get('first_record'):
                    result['first_record'] = str(result['first_record'])
                if result.get('last_record'):
                    result['last_record'] = str(result['last_record'])
                return result
            return {}

        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}

    def delete_all_records(self, user_id: str = None) -> bool:
        """Delete all financial records for a specific user"""
        try:
            if user_id:
                # With CASCADE, related records will be deleted automatically
                self.cursor.execute("DELETE FROM financial_records WHERE user_id = %s", (user_id,))
            else:
                self.cursor.execute("DELETE FROM financial_records")

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error deleting all records: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
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

def get_postgres_database(database_url: str = None) -> PostgresDatabase:
    """Get or create PostgreSQL database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = PostgresDatabase(database_url)
    return _db_instance
