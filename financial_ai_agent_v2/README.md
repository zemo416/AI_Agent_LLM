# 💰 Enterprise Financial AI Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**An AI-powered financial analysis platform for personal and business budget management**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Tech Stack](#tech-stack)

</div>

---

## 🎯 Overview

The **Enterprise Financial AI Assistant** is a comprehensive financial management platform that combines traditional budget analysis with cutting-edge AI technology. It helps individuals and businesses make informed financial decisions through intelligent analysis, visualization, and personalized recommendations.

## ✨ Features

### Core Capabilities

- **🤖 AI-Powered Analysis**
  - Intelligent budget evaluation using ZhipuAI (GLM-4)
  - Personalized financial recommendations
  - Risk assessment and prediction

- **📊 Interactive Dashboard**
  - Real-time financial metrics
  - Modern, responsive UI
  - Multi-page navigation (Dashboard, Analysis, History, Reports)

- **📈 Data Visualization**
  - Interactive charts and graphs (Plotly)
  - Expense breakdown pie charts
  - Income vs. Expenses trend analysis
  - Financial health gauges

- **💾 Data Management**
  - Historical data tracking
  - Session-based data storage
  - CSV/Excel export capabilities
  - Data persistence support

- **🎨 Professional UI/UX**
  - Gradient card designs
  - Color-coded risk indicators
  - Responsive layout
  - Custom CSS styling

### Advanced Features

- **Risk Assessment System**
  - Low/Medium/High risk classification
  - Visual risk indicators
  - Contextual warnings and suggestions

- **Detailed Budget Analysis**
  - Comprehensive expense categorization
  - Multiple income sources support
  - Savings ratio calculation
  - Goal tracking

- **Reporting System**
  - Summary reports
  - Trend analysis
  - Statistical insights
  - Downloadable reports

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- ZhipuAI API key (for AI features)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd financial_ai_agent_v2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Windows
   set ZHIPU_API_KEY=your_api_key_here

   # macOS/Linux
   export ZHIPU_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`

## 📖 Usage

### Quick Start

1. **Navigate to Dashboard**
   - Enter your monthly income, expenses, and saving goal
   - Click "Analyze Now" to get instant insights

2. **Detailed Analysis**
   - Go to "Budget Analysis" page
   - Fill in comprehensive expense breakdown
   - Get AI-powered recommendations

3. **View History**
   - Check "Historical Data" to see all past entries
   - Analyze trends over time
   - Export data for external use

4. **Generate Reports**
   - Visit "Reports" page
   - Select report type
   - Download as CSV

### Example Workflow

```
1. Enter Income: $5,000
2. Enter Expenses: $3,500
3. Set Saving Goal: $1,000
4. Analyze → Get instant feedback
5. Review AI recommendations
6. Track progress over time
```

## 📸 Screenshots

### Dashboard
- Clean, modern interface with gradient cards
- Quick financial health check
- Real-time metrics display

### Budget Analysis
- Comprehensive expense categorization
- Interactive visualizations
- AI-driven insights

### Historical Data
- Trend analysis over time
- Data table view
- Export capabilities

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive data visualization
- **Custom CSS** - Modern UI styling

### Backend
- **Python 3.8+** - Core programming language
- **Pandas** - Data manipulation and analysis
- **ZhipuAI** - AI-powered financial analysis

### Data & Storage
- **Session State** - In-memory data storage
- **CSV Export** - Data portability
- **Future: SQLite** - Persistent database storage

## 🏗️ Architecture

```
financial_ai_agent_v2/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .venv/                # Virtual environment
└── my_package/           # Additional modules (optional)
```

## 🔑 Key Functions

### Core Analysis Engine

```python
analyze_budget(income, expenses, saving_goal)
```
- Evaluates financial health
- Calculates risk levels
- Returns detailed analysis results

### AI Integration

```python
get_ai_analysis(result)
```
- Sends financial data to AI model
- Receives personalized recommendations
- Formats and displays insights

## 📊 Feature Comparison

| Feature | Basic Version | Enterprise Version (v2.0) |
|---------|--------------|---------------------------|
| Budget Analysis | ✅ Command Line | ✅ Web Interface |
| AI Integration | ✅ Basic | ✅ Advanced |
| Data Visualization | ❌ | ✅ Interactive Charts |
| Historical Tracking | ❌ | ✅ Full History |
| Reports | ❌ | ✅ Multiple Types |
| Export Data | ❌ | ✅ CSV/Excel |
| Multi-page UI | ❌ | ✅ Dashboard + 4 Pages |
| Risk Assessment | ✅ Basic | ✅ Visual Indicators |

## 🎯 Use Cases

### Personal Finance
- Monthly budget planning
- Expense tracking
- Savings goal management
- Financial health monitoring

### Business Applications
- Small business budget analysis
- Department expense tracking
- Financial forecasting
- Client demonstrations

### Educational
- Financial literacy education
- Budgeting workshops
- Personal finance courses
- Case study analysis

## 🚀 Future Enhancements

### Planned Features (v3.0)

- [ ] **SQLite Database Integration**
  - Persistent data storage
  - Multi-user support
  - Advanced querying

- [ ] **Advanced Analytics**
  - 6-month financial forecasting
  - Machine learning predictions
  - Anomaly detection

- [ ] **Enhanced Visualizations**
  - Customizable dashboards
  - More chart types
  - Interactive filters

- [ ] **Export Options**
  - PDF reports with charts
  - Excel templates
  - Scheduled email reports

- [ ] **Budget Categories**
  - Custom category creation
  - Category-based alerts
  - Spending limits

- [ ] **Multi-Currency Support**
  - Currency conversion
  - Multiple currency tracking
  - Exchange rate updates

## 🤝 Contributing

This project was created as a portfolio demonstration. Suggestions and feedback are welcome!

## 👨‍💻 Author

**Zemou Huang**
- Portfolio Project
- Contact: zh333@nau.edu
- GitHub: zemo416

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **ZhipuAI** for AI capabilities
- **Streamlit** for the amazing framework
- **Plotly** for beautiful visualizations
- **Open source community** for continuous inspiration

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact via email
- Check documentation

---

<div align="center">

**Built with ❤️ using Python, AI, and Data Science**

⭐ Star this repo if you find it useful!

</div>
