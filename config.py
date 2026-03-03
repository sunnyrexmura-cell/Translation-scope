import os
import json
import base64
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
# Base64 形式 または 直接 JSON 形式に対応
GOOGLE_SHEETS_CREDENTIALS = {}
try:
    # まず Base64 形式を試す
    creds_b64 = os.getenv("GOOGLE_SHEETS_CREDENTIALS_B64", "")
    if creds_b64:
        print(f"[DEBUG] Base64 credentials found, length: {len(creds_b64)}")
        json_str = base64.b64decode(creds_b64).decode('utf-8')
        print(f"[DEBUG] Decoded JSON length: {len(json_str)}")
        GOOGLE_SHEETS_CREDENTIALS = json.loads(json_str)
        print(f"[DEBUG] Parsed credentials type: {GOOGLE_SHEETS_CREDENTIALS.get('type')}")
    else:
        # Base64 形式がない場合は直接 JSON 形式を試す
        GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "{}")
        print(f"[DEBUG] Using direct JSON, length: {len(GOOGLE_SHEETS_CREDENTIALS_JSON)}")
        GOOGLE_SHEETS_CREDENTIALS = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
        print(f"[DEBUG] Parsed credentials type: {GOOGLE_SHEETS_CREDENTIALS.get('type')}")

    # typeフィールドの存在確認
    if not isinstance(GOOGLE_SHEETS_CREDENTIALS, dict) or "type" not in GOOGLE_SHEETS_CREDENTIALS:
        raise ValueError("Invalid credentials format: missing 'type' field")

    # Private key 検証
    if "private_key" in GOOGLE_SHEETS_CREDENTIALS:
        pk = GOOGLE_SHEETS_CREDENTIALS["private_key"]
        print(f"[DEBUG] Private key length: {len(pk)}, starts with: {pk[:30]}")

except (json.JSONDecodeError, ValueError, Exception) as e:
    print(f"[ERROR] Google Sheets credentials error: {str(e)}")
    import traceback
    traceback.print_exc()
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
