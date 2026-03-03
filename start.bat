@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 勤怠管理アプリを起動中...
timeout /t 3
start http://localhost:8501
python -m streamlit run main.py
pause
