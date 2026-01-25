"""
Complete Authentication System
Handles user registration, login, and session management
"""

import streamlit as st
import bcrypt
import sqlite3
from datetime import datetime
from typing import Optional, Dict

class AuthSystem:
    """User authentication and management"""

    def __init__(self, db_path: str = "financial_data.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_users_table()

    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def create_users_table(self):
        """Create users table if it doesn't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT
            )
        """)
        self.conn.commit()

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def register_user(self, username: str, email: str, password: str, full_name: str = "") -> tuple[bool, str]:
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        try:
            # Validate inputs
            if len(username) < 3:
                return False, "Username must be at least 3 characters"
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            if '@' not in email:
                return False, "Invalid email address"

            # Hash password
            password_hash = self.hash_password(password)

            # Insert user
            self.cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))

            self.conn.commit()
            return True, "Registration successful!"

        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, username: str, password: str) -> tuple[bool, Optional[Dict]]:
        """
        Login a user
        Returns: (success: bool, user_data: dict or None)
        """
        try:
            self.cursor.execute("""
                SELECT * FROM users WHERE username = ?
            """, (username,))

            user = self.cursor.fetchone()

            if not user:
                return False, None

            # Verify password
            if not self.verify_password(password, user['password_hash']):
                return False, None

            # Update last login
            self.cursor.execute("""
                UPDATE users SET last_login = ? WHERE id = ?
            """, (datetime.now().isoformat(), user['id']))
            self.conn.commit()

            # Return user data (without password hash)
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'created_at': user['created_at'],
                'last_login': user['last_login']
            }

            return True, user_data

        except Exception as e:
            print(f"Login error: {e}")
            return False, None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user data by ID"""
        try:
            self.cursor.execute("""
                SELECT id, username, email, full_name, created_at, last_login
                FROM users WHERE id = ?
            """, (user_id,))

            user = self.cursor.fetchone()
            return dict(user) if user else None

        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def show_login_page():
    """Display login/registration interface"""
    st.title("🔐 Financial AI Assistant")
    st.markdown("### Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.markdown("#### Sign in to your account")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            col1, col2 = st.columns([1, 3])
            with col1:
                submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    auth = AuthSystem()
                    success, user_data = auth.login_user(username, password)

                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        st.session_state.user_id = str(user_data['id'])  # Use database ID as user_id
                        st.success(f"Welcome back, {user_data['username']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

    with tab2:
        st.markdown("#### Create a new account")

        with st.form("register_form"):
            new_username = st.text_input("Username (min 3 characters)")
            new_email = st.text_input("Email")
            new_full_name = st.text_input("Full Name (optional)")
            new_password = st.text_input("Password (min 6 characters)", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            col1, col2 = st.columns([1, 3])
            with col1:
                register = st.form_submit_button("Register", use_container_width=True)

            if register:
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all required fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    auth = AuthSystem()
                    success, message = auth.register_user(
                        new_username, new_email, new_password, new_full_name
                    )

                    if success:
                        st.success(message + " You can now login!")
                    else:
                        st.error(message)

    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔒 Your data is encrypted and secure</p>
        <p>💡 Demo Mode: Continue without login for a quick try</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Continue as Guest (Demo Mode)", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.guest_mode = True
        st.rerun()


def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.user_id = None
    st.session_state.guest_mode = False
    st.rerun()


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False) or st.session_state.get('guest_mode', False)


def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            show_login_page()
            return None
        return func(*args, **kwargs)
    return wrapper
