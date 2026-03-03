"""
Google Sheets を初期化するスクリプト
従業員シートと打刻記録シートを作成
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from dotenv import load_dotenv

load_dotenv()

def init_sheets():
    """Google Sheets を初期化"""

    # 認証情報
    creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "{}")
    sheets_id = os.getenv("GOOGLE_SHEETS_ID", "")

    if not sheets_id:
        print("❌ GOOGLE_SHEETS_ID が設定されていません")
        return False

    try:
        creds = json.loads(creds_json)
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scopes=scope)
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(sheets_id)

        print(f"[OK] Google Sheets に接続しました: {spreadsheet.title}")

        # 既存シートを削除（最初のシート以外）
        sheets_to_delete = []
        for sheet in spreadsheet.worksheets():
            if sheet.title in ["従業員", "打刻記録", "Sheet1"]:
                sheets_to_delete.append(sheet)

        # 最初のシート以外を削除
        for i, sheet in enumerate(sheets_to_delete):
            if i > 0:  # 最初のシートは残す
                try:
                    spreadsheet.del_worksheet(sheet)
                    print(f"  - シート '{sheet.title}' を削除しました")
                except:
                    pass

        # 従業員シートを取得または作成
        try:
            employees_sheet = spreadsheet.worksheet("従業員")
            employees_sheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            employees_sheet = spreadsheet.add_worksheet(title="従業員", rows=100, cols=4)

        employees_sheet.append_row(["従業員番号", "苗字", "名前", "従業員ID"])
        employees_sheet.append_row(["001", "田中", "太郎", "001"])
        employees_sheet.append_row(["002", "鈴木", "花子", "002"])
        employees_sheet.append_row(["003", "佐藤", "次郎", "003"])
        print("[OK] 従業員シートを作成/更新しました")

        # 打刻記録シートを取得または作成
        try:
            attendance_sheet = spreadsheet.worksheet("打刻記録")
            attendance_sheet.clear()
        except gspread.exceptions.WorksheetNotFound:
            attendance_sheet = spreadsheet.add_worksheet(title="打刻記録", rows=1000, cols=5)

        attendance_sheet.append_row(["従業員ID", "従業員名", "打刻種別", "日時", "ステータス"])
        print("[OK] 打刻記録シートを作成/更新しました")

        print("\n[SUCCESS] 初期化が完了しました！")
        return True

    except Exception as e:
        print(f"[ERROR] エラー: {str(e)}")
        return False

if __name__ == "__main__":
    init_sheets()
