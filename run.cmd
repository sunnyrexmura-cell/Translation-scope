@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ============================================
echo   勤怠管理アプリ - テスト実行
echo ============================================
echo.

echo [1/2] Python仮想環境を確認中...
if not exist venv (
    echo [OK] venv フォルダがありません
    echo [2/2] 直接実行します...
) else (
    echo [OK] venv を使用します
    call venv\Scripts\activate.bat
)

echo.
echo [実行中] http://localhost:8501
echo Ctrl+C で終了
echo.

python -m streamlit run main.py --logger.level=warning

pause
