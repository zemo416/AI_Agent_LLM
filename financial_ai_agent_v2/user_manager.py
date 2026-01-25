"""
User Management Module
Handles user identification and session management
"""

import uuid
import streamlit as st
from datetime import datetime

def get_or_create_user_id():
    """
    Get or create a unique user ID for the current browser session
    Uses st.session_state to persist across page reloads
    """
    # Check if user_id exists in session state
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        # Generate a new UUID for this user
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.user_created_at = datetime.now().isoformat()

    return st.session_state.user_id

def clear_user_session():
    """Clear all user session data"""
    if 'user_records' in st.session_state:
        st.session_state.user_records = []
    if 'current_month_data' in st.session_state:
        st.session_state.current_month_data = None

def get_user_info():
    """Get current user information"""
    return {
        'user_id': st.session_state.get('user_id'),
        'created_at': st.session_state.get('user_created_at'),
        'total_records': len(st.session_state.get('user_records', []))
    }
