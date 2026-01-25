"""
Quick test script for the Financial AI Assistant
"""

# Test imports
try:
    import streamlit as st
    print("[OK] Streamlit imported successfully")
except Exception as e:
    print(f"[FAIL] Streamlit import failed: {e}")

try:
    import pandas as pd
    print("[OK] Pandas imported successfully")
except Exception as e:
    print(f"[FAIL] Pandas import failed: {e}")

try:
    import plotly.graph_objects as go
    import plotly.express as px
    print("[OK] Plotly imported successfully")
except Exception as e:
    print(f"[FAIL] Plotly import failed: {e}")

try:
    from zhipuai import ZhipuAI
    print("[OK] ZhipuAI imported successfully")
except Exception as e:
    print(f"[FAIL] ZhipuAI import failed: {e}")

try:
    from database import get_database, FinancialDatabase
    print("[OK] Database module imported successfully")
except Exception as e:
    print(f"[FAIL] Database import failed: {e}")

# Test database functionality
try:
    db = get_database()
    print("[OK] Database connection established")

    # Test record insertion
    test_result = {
        'income': 5000.0,
        'fixed': 3000.0,
        'goal': 1000.0,
        'remaining': 2000.0,
        'risk': 'Low',
        'ratio': 20.0,
        'messages': ['Test message'],
        'flags': set()
    }

    record_id = db.insert_financial_record(test_result)
    if record_id > 0:
        print(f"[OK] Test record inserted successfully (ID: {record_id})")

        # Test retrieval
        records = db.get_all_records()
        print(f"[OK] Retrieved {len(records)} records from database")

        # Test deletion
        if db.delete_record(record_id):
            print("[OK] Test record deleted successfully")
        else:
            print("[FAIL] Failed to delete test record")
    else:
        print("[FAIL] Failed to insert test record")

except Exception as e:
    print(f"[FAIL] Database test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("All tests completed!")
print("="*50)
print("\nTo run the application:")
print("  streamlit run app.py")
