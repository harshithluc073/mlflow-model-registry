@echo off
REM Start MLflow Tracking Server on Windows

echo ========================================
echo Starting MLflow Tracking Server
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start MLflow server
python scripts\start_mlflow.py --host 127.0.0.1 --port 5000

pause