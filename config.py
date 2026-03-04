import os
import json
import base64
from pathlib import Path
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

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
        print(f"[DEBUG] First 200 chars: {GOOGLE_SHEETS_CREDENTIALS_JSON[:200]}")

        # JSON パース試行
        try:
            GOOGLE_SHEETS_CREDENTIALS = json.loads(GOOGLE_SHEETS_CREDENTIALS_JSON)
            print(f"[DEBUG] Successfully parsed JSON")
            print(f"[DEBUG] Parsed credentials type: {GOOGLE_SHEETS_CREDENTIALS.get('type')}")
        except json.JSONDecodeError as json_err:
            print(f"[ERROR] JSON parse error: {json_err}")
            print(f"[ERROR] Error at position {json_err.pos}: {json_err.msg}")
            raise

    # typeフィールドの存在確認
    if not isinstance(GOOGLE_SHEETS_CREDENTIALS, dict) or "type" not in GOOGLE_SHEETS_CREDENTIALS:
        raise ValueError("Invalid credentials format: missing 'type' field")

    # Private key 検証・修正
    if "private_key" in GOOGLE_SHEETS_CREDENTIALS:
        pk = GOOGLE_SHEETS_CREDENTIALS["private_key"]
        print(f"[DEBUG] Private key found, length: {len(pk)}")
        # \n エスケープを実際の改行に変換（必要な場合）
        if isinstance(pk, str) and '\\n' in pk:
            pk = pk.replace('\\n', '\n')
            GOOGLE_SHEETS_CREDENTIALS["private_key"] = pk
            print(f"[DEBUG] Converted escaped newlines in private key")
        print(f"[DEBUG] Private key starts with: {pk[:40]}")
        print(f"[DEBUG] Private key ends with: {pk[-40:]}")
    else:
        print(f"[WARNING] No private_key field found in credentials")

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
