"""
Enterprise Financial AI Assistant
A comprehensive financial analysis platform powered by AI
Author: Zemou Huang
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
from zhipuai import ZhipuAI
from database import get_database

# Page configuration
st.set_page_config(
    page_title="Financial AI Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #1a1a2e;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        border: 1px solid #2d2d44;
    }
    .stMetric label {
        color: #b0b0c0 !important;
        font-size: 0.9rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    h1 {
        color: #1f77b4;
        font-weight: 600;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_database():
    return get_database()

db = init_database()

# Initialize session state
if 'current_month_data' not in st.session_state:
    st.session_state.current_month_data = None
if 'use_database' not in st.session_state:
    st.session_state.use_database = True

# Initialize AI client
@st.cache_resource
def get_ai_client():
    # Try to get API key from Streamlit secrets first, then fall back to environment variable
    try:
        api_key = st.secrets.get("ZHIPU_API_KEY")
    except:
        api_key = os.getenv("ZHIPU_API_KEY")

    if not api_key:
        st.warning("⚠️ ZHIPU_API_KEY not found. AI features will be limited.")
        return None
    return ZhipuAI(api_key=api_key)

client = get_ai_client()

# Core financial analysis functions (from original code)
def analyze_budget(income, fixed_expenses, saving_goal):
    """Analyze budget and return detailed results"""
    remaining = income - fixed_expenses
    result = {
        "income": income,
        "fixed": fixed_expenses,
        "goal": saving_goal,
        "remaining": remaining,
        "risk": None,
        "ratio": None,
        "messages": [],
        "flags": set(),
        "timestamp": datetime.now().isoformat()
    }

    # Input validation
    if income <= 0:
        result["flags"].add("invalid_income")
        result["messages"].append("Income must be greater than 0.")
        return result

    if saving_goal <= 0:
        result["flags"].add("zero_goal")
        result["messages"].append("Saving goal is 0. You may want to set a small goal to start.")
        return result

    # Risk assessment
    if remaining <= 0:
        result["risk"] = "High"
        result["flags"].add("negative_remaining")
        result["messages"].append("⚠️ Warning: Your expenses exceed your income.")
        return result

    if saving_goal > income:
        result["risk"] = "High"
        result["flags"].add("unrealistic_goal")
        result["messages"].append("⚠️ Your saving goal is unrealistic (greater than income).")
        return result

    if saving_goal > remaining:
        result["risk"] = "Medium"
        result["flags"].add("goal_too_high")
        result["messages"].append("⚠️ Your saving goal is too high based on current expenses.")
    else:
        result["risk"] = "Low"
        result["messages"].append("✅ Your saving goal is achievable.")

    # Calculate savings ratio
    result["ratio"] = round((saving_goal / income) * 100, 2)
    result["messages"].append(f"📊 Recommended saving ratio: {result['ratio']}%")

    # General suggestions
    result["messages"].append("💡 Suggestions:")
    result["messages"].append("  • Keep savings between 20% and 40% of income")
    result["messages"].append("  • Reduce non-essential spending if needed")
    result["messages"].append("  • Build an emergency fund (3–6 months)")

    return result

def get_ai_analysis(result):
    """Get AI-powered financial analysis"""
    if not client:
        return "AI analysis is not available. Please set ZHIPU_API_KEY."

    fact_text = "\n".join([
        f"Income: ${result['income']:.2f}",
        f"Fixed Expenses: ${result['fixed']:.2f}",
        f"Saving Goal: ${result['goal']:.2f}",
        f"Remaining: ${result['remaining']:.2f}",
        f"Risk Level: {result['risk']}",
        f"Savings Ratio: {result['ratio']}%"
    ])

    try:
        response = client.chat.completions.create(
            model="glm-4-air",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional financial advisor. "
                               "Provide actionable, specific advice based on the financial data. "
                               "Focus on concrete steps the user can take. "
                               "Be concise and use bullet points."
                },
                {"role": "user", "content": fact_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting AI analysis: {str(e)}"

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/money-bag.png", width=150)
    st.title("📊 Navigation")

    page = st.radio(
        "Select Page",
        ["Dashboard", "Budget Analysis", "Historical Data", "Reports", "Settings"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 📈 Quick Stats")
    all_records = db.get_all_records()
    if all_records:
        total_entries = len(all_records)
        stats = db.get_statistics()
        st.metric("Total Entries", total_entries)
        if stats.get('avg_savings_ratio'):
            st.metric("Avg Savings", f"{stats['avg_savings_ratio']:.1f}%")
    else:
        st.info("No data yet. Start analyzing!")

    st.divider()
    st.markdown("### 💡 About")
    st.caption("Enterprise Financial AI Assistant v2.0")
    st.caption("Powered by AI & Data Science")
    st.caption("© 2026 Zemou Huang")

# Main content area
if page == "Dashboard":
    st.title("💰 Financial Dashboard")
    st.markdown("### Welcome to your AI-powered financial assistant")

    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Smart Analysis</h3>
            <p>Get AI-powered insights on your financial health</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>📊 Real-time Tracking</h3>
            <p>Monitor your income, expenses, and savings</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>💡 Actionable Advice</h3>
            <p>Receive personalized recommendations</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Quick analysis section
    st.markdown("### 🚀 Quick Financial Check")

    with st.form("quick_analysis"):
        col1, col2, col3 = st.columns(3)

        with col1:
            income = st.number_input("💵 Monthly Income ($)", min_value=0.0, step=100.0, value=5000.0)
        with col2:
            expenses = st.number_input("💳 Fixed Expenses ($)", min_value=0.0, step=100.0, value=3000.0)
        with col3:
            goal = st.number_input("🎯 Saving Goal ($)", min_value=0.0, step=100.0, value=1000.0)

        submitted = st.form_submit_button("🔍 Analyze Now", use_container_width=True)

        if submitted:
            with st.spinner("Analyzing your financial data..."):
                result = analyze_budget(income, expenses, goal)
                st.session_state.current_month_data = result

                # Save to database
                record_id = db.insert_financial_record(result)
                if record_id > 0:
                    st.success("✅ Data saved to database!")
                else:
                    st.warning("⚠️ Could not save to database")

    # Display results if available
    if st.session_state.current_month_data:
        result = st.session_state.current_month_data

        st.divider()
        st.markdown("### 📊 Analysis Results")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Income", f"${result['income']:,.2f}", delta=None)
        with col2:
            st.metric("Expenses", f"${result['fixed']:,.2f}", delta=None)
        with col3:
            delta_value = result['remaining']
            st.metric("Remaining", f"${result['remaining']:,.2f}",
                     delta=f"${delta_value:,.2f}" if delta_value >= 0 else f"-${abs(delta_value):,.2f}",
                     delta_color="normal" if delta_value >= 0 else "inverse")
        with col4:
            risk_color = {"Low": "normal", "Medium": "off", "High": "inverse"}
            st.metric("Risk Level", result['risk'], delta_color=risk_color.get(result['risk'], "off"))

        # Messages
        risk_level = result.get('risk', 'Unknown')
        if risk_level == "Low":
            st.markdown(f"""<div class="success-box">
                <strong>✅ Good Financial Health</strong><br>
                {' '.join(result['messages'])}
            </div>""", unsafe_allow_html=True)
        elif risk_level == "Medium":
            st.markdown(f"""<div class="warning-box">
                <strong>⚠️ Moderate Risk</strong><br>
                {' '.join(result['messages'])}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="danger-box">
                <strong>🚨 High Risk</strong><br>
                {' '.join(result['messages'])}
            </div>""", unsafe_allow_html=True)

        # AI Analysis
        if client:
            with st.expander("🤖 AI-Powered Recommendations", expanded=True):
                with st.spinner("Getting AI insights..."):
                    ai_advice = get_ai_analysis(result)
                    st.markdown(ai_advice)

elif page == "Budget Analysis":
    st.title("📊 Detailed Budget Analysis")
    st.markdown("### Comprehensive financial planning tool")

    with st.form("detailed_analysis"):
        st.markdown("#### 💰 Income Information")
        col1, col2 = st.columns(2)

        with col1:
            income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=5000.0)
            additional_income = st.number_input("Additional Income ($)", min_value=0.0, step=50.0, value=0.0)

        with col2:
            total_income = income + additional_income
            st.metric("Total Income", f"${total_income:,.2f}")

        st.markdown("#### 💳 Expense Breakdown")

        col1, col2, col3 = st.columns(3)

        with col1:
            rent = st.number_input("🏠 Rent/Mortgage ($)", min_value=0.0, step=100.0, value=1500.0)
            utilities = st.number_input("💡 Utilities ($)", min_value=0.0, step=10.0, value=200.0)
            food = st.number_input("🍔 Food ($)", min_value=0.0, step=50.0, value=500.0)

        with col2:
            transportation = st.number_input("🚗 Transportation ($)", min_value=0.0, step=50.0, value=300.0)
            insurance = st.number_input("🛡️ Insurance ($)", min_value=0.0, step=50.0, value=200.0)
            debt = st.number_input("💰 Debt Payments ($)", min_value=0.0, step=50.0, value=300.0)

        with col3:
            entertainment = st.number_input("🎬 Entertainment ($)", min_value=0.0, step=20.0, value=200.0)
            healthcare = st.number_input("🏥 Healthcare ($)", min_value=0.0, step=50.0, value=100.0)
            other = st.number_input("📦 Other ($)", min_value=0.0, step=20.0, value=100.0)

        total_expenses = rent + utilities + food + transportation + insurance + debt + entertainment + healthcare + other

        st.metric("Total Expenses", f"${total_expenses:,.2f}")

        st.markdown("#### 🎯 Savings Goal")
        saving_goal = st.number_input("Monthly Saving Goal ($)", min_value=0.0, step=100.0, value=1000.0)

        analyze_button = st.form_submit_button("🔍 Analyze Budget", use_container_width=True)

        if analyze_button:
            with st.spinner("Performing detailed analysis..."):
                result = analyze_budget(total_income, total_expenses, saving_goal)
                st.session_state.current_month_data = result

                # Add expense breakdown to result
                result['expense_breakdown'] = {
                    "Rent/Mortgage": rent,
                    "Utilities": utilities,
                    "Food": food,
                    "Transportation": transportation,
                    "Insurance": insurance,
                    "Debt Payments": debt,
                    "Entertainment": entertainment,
                    "Healthcare": healthcare,
                    "Other": other
                }

                # Save to database
                record_id = db.insert_financial_record(result)
                if record_id > 0:
                    st.success("✅ Detailed analysis saved to database!")
                else:
                    st.warning("⚠️ Could not save to database")

    # Show results if available
    if st.session_state.current_month_data:
        result = st.session_state.current_month_data

        st.divider()
        st.markdown("### 📈 Detailed Results")

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Visualizations", "🤖 AI Insights"])

        with tab1:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Financial Summary")
                st.metric("Total Income", f"${result['income']:,.2f}")
                st.metric("Total Expenses", f"${result['fixed']:,.2f}")
                st.metric("Remaining", f"${result['remaining']:,.2f}")
                st.metric("Saving Goal", f"${result['goal']:,.2f}")
                st.metric("Savings Ratio", f"{result.get('ratio', 0):.1f}%")

            with col2:
                st.markdown("#### Risk Assessment")

                risk = result.get('risk', 'Unknown')
                risk_colors = {
                    "Low": "#28a745",
                    "Medium": "#ffc107",
                    "High": "#dc3545"
                }

                st.markdown(f"""
                <div style="background-color: {risk_colors.get(risk, '#6c757d')};
                            padding: 30px; border-radius: 10px; color: white; text-align: center;">
                    <h2>{risk} Risk</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Messages")
                for msg in result['messages']:
                    st.info(msg)

        with tab2:
            if 'expense_breakdown' in result:
                st.markdown("#### Expense Breakdown")

                # Pie chart
                expense_data = result['expense_breakdown']
                fig = px.pie(
                    values=list(expense_data.values()),
                    names=list(expense_data.keys()),
                    title="Expense Distribution",
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

                # Bar chart
                fig2 = go.Figure(data=[
                    go.Bar(x=list(expense_data.keys()), y=list(expense_data.values()),
                           marker_color='lightblue')
                ])
                fig2.update_layout(title="Expense Comparison", xaxis_title="Category", yaxis_title="Amount ($)")
                st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            if client:
                with st.spinner("Generating AI insights..."):
                    ai_advice = get_ai_analysis(result)
                    st.markdown(ai_advice)
            else:
                st.warning("AI features are not available. Please configure ZHIPU_API_KEY.")

elif page == "Historical Data":
    st.title("📅 Historical Financial Data")

    # Get data from database
    all_records = db.get_all_records()

    if all_records:
        st.markdown(f"### You have {len(all_records)} recorded entries")

        # Convert to DataFrame
        df_data = []
        for entry in all_records:
            df_data.append({
                "Date": entry.get('timestamp', 'N/A'),
                "Income": entry['income'],
                "Expenses": entry['fixed'],
                "Saving Goal": entry['goal'],
                "Remaining": entry['remaining'],
                "Risk": entry.get('risk', 'N/A'),
                "Ratio (%)": entry.get('ratio', 0)
            })

        df = pd.DataFrame(df_data)

        # Display data
        st.dataframe(df, use_container_width=True)

        # Trend analysis
        st.markdown("### 📈 Trends")

        if len(df) > 1:
            # Income vs Expenses trend
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Income'], mode='lines+markers', name='Income'))
            fig.add_trace(go.Scatter(x=df.index, y=df['Expenses'], mode='lines+markers', name='Expenses'))
            fig.update_layout(title="Income vs Expenses Over Time", xaxis_title="Entry", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)

            # Savings trend
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df['Remaining'], mode='lines+markers',
                                     name='Monthly Savings', fill='tozeroy'))
            fig2.update_layout(title="Savings Trend", xaxis_title="Entry", yaxis_title="Savings ($)")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Need at least 2 entries to show trends.")

        # Statistics
        st.markdown("### 📊 Statistics")
        stats = db.get_statistics()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Income", f"${stats.get('avg_income', 0):,.2f}")
        with col2:
            st.metric("Average Expenses", f"${stats.get('avg_expenses', 0):,.2f}")
        with col3:
            st.metric("Average Savings", f"${stats.get('avg_remaining', 0):,.2f}")

        # Clear data button
        st.divider()
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
                if db.delete_all_records():
                    st.session_state.current_month_data = None
                    st.success("All data cleared!")
                    st.rerun()
                else:
                    st.error("Failed to clear data")
    else:
        st.info("📭 No historical data yet. Start by analyzing your budget!")

elif page == "Reports":
    st.title("📄 Financial Reports")
    st.markdown("### Generate comprehensive financial reports")

    all_records = db.get_all_records()

    if all_records:
        st.success(f"✅ {len(all_records)} entries available for reporting")

        report_type = st.selectbox(
            "Select Report Type",
            ["Summary Report", "Detailed Analysis", "Trend Report", "Risk Assessment"]
        )

        if st.button("📊 Generate Report", use_container_width=True):
            st.markdown("### 📋 Report Generated")

            df_data = []
            for entry in all_records:
                df_data.append({
                    "Date": entry.get('timestamp', 'N/A'),
                    "Income": entry['income'],
                    "Expenses": entry['fixed'],
                    "Savings": entry['remaining'],
                    "Risk": entry.get('risk', 'N/A'),
                    "Ratio (%)": entry.get('ratio', 0)
                })

            df = pd.DataFrame(df_data)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Average Income", f"${df['Income'].mean():,.2f}")
            with col2:
                st.metric("Average Expenses", f"${df['Expenses'].mean():,.2f}")
            with col3:
                st.metric("Average Savings", f"${df['Savings'].mean():,.2f}")
            with col4:
                st.metric("Avg Savings Ratio", f"{df['Ratio (%)'].mean():.1f}%")

            st.markdown("#### Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)

            # Risk distribution
            st.markdown("#### Risk Distribution")
            risk_counts = df['Risk'].value_counts()
            fig = px.pie(values=risk_counts.values, names=risk_counts.index,
                        title="Risk Level Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # Download options
            st.markdown("#### Download Options")
            col1, col2 = st.columns(2)

            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"financial_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col2:
                # Excel export would require openpyxl
                st.info("Excel export available with openpyxl")
    else:
        st.warning("⚠️ No data available. Please analyze your budget first!")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.markdown("### Configure your preferences")

    st.markdown("#### API Configuration")
    try:
        api_key = st.secrets.get("ZHIPU_API_KEY") or os.getenv("ZHIPU_API_KEY")
    except:
        api_key = os.getenv("ZHIPU_API_KEY")
    api_key_status = "✅ Configured" if api_key else "❌ Not configured"
    st.info(f"ZHIPU_API_KEY: {api_key_status}")

    st.markdown("#### Database Information")
    stats = db.get_statistics()
    if stats.get('total_records', 0) > 0:
        st.success(f"✅ Database connected: {stats['total_records']} records")
        st.info(f"First record: {stats.get('first_record', 'N/A')}")
        st.info(f"Last record: {stats.get('last_record', 'N/A')}")
    else:
        st.info("Database is empty")

    st.markdown("#### Data Management")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
            if db.delete_all_records():
                st.session_state.current_month_data = None
                st.success("All data has been cleared!")
                st.rerun()
            else:
                st.error("Failed to clear data")

    with col2:
        if st.button("🔄 Refresh Stats", use_container_width=True):
            st.rerun()

    st.markdown("#### About")
    st.markdown("""
    **Enterprise Financial AI Assistant v2.0**

    This application provides:
    - AI-powered financial analysis
    - Real-time budget tracking
    - Data visualization
    - Historical data management
    - Comprehensive reporting

    Created by: **Zemou Huang**
    Technology Stack: Python, Streamlit, Plotly, AI (ZhipuAI)
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💰 Enterprise Financial AI Assistant | Powered by AI & Data Science | © 2026 Zemou Huang</p>
</div>
""", unsafe_allow_html=True)
