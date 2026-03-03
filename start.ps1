# 勤怠管理アプリ起動スクリプト

Write-Host "=======================================`n  勤怠管理アプリ - 起動中`n=======================================" -ForegroundColor Cyan

# 現在のディレクトリに移動
Set-Location $PSScriptRoot

Write-Host "`n[1/3] Python依存パッケージを確認中...`n" -ForegroundColor Yellow

# 依存パッケージをインストール
pip install -q -r requirements.txt

Write-Host "[2/3] Streamlitアプリを起動中...`n" -ForegroundColor Yellow
Write-Host "ブラウザで以下にアクセスしてください:`n  http://localhost:8501`n" -ForegroundColor Green

# Streamlitを起動
python -m streamlit run main.py
