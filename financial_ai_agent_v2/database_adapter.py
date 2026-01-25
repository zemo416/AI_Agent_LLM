"""
Database Adapter
Automatically selects SQLite or PostgreSQL based on environment
"""

import os
from typing import Union

def get_database():
    """
    Get database instance based on environment
    Returns SQLite for local, PostgreSQL for cloud
    """
    database_url = os.getenv("DATABASE_URL")

    if database_url and database_url.startswith("postgresql://"):
        # Use PostgreSQL (Supabase, etc.)
        print("✅ Using PostgreSQL (Cloud Database)")
        from database_postgres import get_postgres_database
        return get_postgres_database(database_url)
    else:
        # Use SQLite (Local/Development)
        print("✅ Using SQLite (Local Database)")
        from database import get_database as get_sqlite_database
        return get_sqlite_database()
