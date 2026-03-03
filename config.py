import os
import json
from pathlib import Path
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# マネーフォワード API
MF_API_KEY = os.getenv("MF_API_KEY", "")
MF_API_BASE_URL = "https://api.moneyforward.com"

# Google Sheets
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")

# Google Sheets 認証用JSON（環境変数から取得）
GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "{}")
try:
    # JSON文字列をパース
    GOOGLE_SHEETS_CREDENTIALS = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
    # typeフィールドの存在確認
    if not isinstance(GOOGLE_SHEETS_CREDENTIALS, dict) or "type" not in GOOGLE_SHEETS_CREDENTIALS:
        raise ValueError("Invalid credentials format: missing 'type' field")
except (json.JSONDecodeError, ValueError) as e:
    print(f"警告: Google Sheets 認証情報の読み込みに失敗しました: {str(e)}")
    GOOGLE_SHEETS_CREDENTIALS = {}

# Google Sheets シート名
EMPLOYEES_SHEET = "従業員"
ATTENDANCE_SHEET = "打刻記録"

# 定数
PUNCH_TYPE_START = "出勤"
PUNCH_TYPE_END = "退勤"

STATUS_SUCCESS = "成功"
STATUS_FAILURE = "失敗"

# UI設定
BUTTON_HEIGHT = "60px"
BUTTON_FONT_SIZE = "18px"
COLOR_START = "#28a745"  # 緑
COLOR_END = "#dc3545"    # 赤
