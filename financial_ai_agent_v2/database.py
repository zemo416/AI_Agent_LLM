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

        self.conn.commit()

    def insert_financial_record(self, result: Dict) -> int:
        """
        Insert a new financial record
        Returns: record_id
        """
        try:
            # Insert main record
            self.cursor.execute("""
                INSERT INTO financial_records
                (timestamp, income, fixed_expenses, saving_goal, remaining, risk_level, savings_ratio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
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

    def get_all_records(self) -> List[Dict]:
        """Retrieve all financial records"""
        try:
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

    def delete_all_records(self) -> bool:
        """Delete all financial records"""
        try:
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

    def get_statistics(self) -> Dict:
        """Get statistical summary of all records"""
        try:
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
