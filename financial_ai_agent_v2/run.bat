@echo off
echo ========================================
echo  Financial AI Assistant
echo  Starting application...
echo ========================================
echo.

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Warning: Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit
)

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the application
echo.
echo Starting Streamlit application...
echo.
streamlit run app.py

pause
