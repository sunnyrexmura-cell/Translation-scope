import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import List, Dict
import config
import csv
import io

class GoogleSheetsService:
    def __init__(self):
        """Google Sheets サービスを初期化"""
        self.credentials = None
        self.client = None
        self.spreadsheet = None
        self._initialize_client()

    def _initialize_client(self):
        """Google Sheets クライアントを初期化"""
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]

            self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                config.GOOGLE_SHEETS_CREDENTIALS,
                scopes=scope
            )
            self.client = gspread.authorize(self.credentials)
            self.spreadsheet = self.client.open_by_key(config.GOOGLE_SHEETS_ID)
        except Exception as e:
            raise Exception(f"Google Sheets 初期化エラー: {str(e)}")

    def get_employees(self) -> List[Dict[str, str]]:
        """従業員リストを取得"""
        try:
            worksheet = self.spreadsheet.worksheet(config.EMPLOYEES_SHEET)
            # get_all_values()を使ってセルの生の値を取得
            all_values = worksheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []

            # ヘッダー行とデータ行を分離
            headers = all_values[0]
            records = []

            for row in all_values[1:]:
                record = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        # すべての値を文字列として保存
                        record[header] = str(row[i]) if row[i] else ""
                records.append(record)

            return records
        except Exception as e:
            raise Exception(f"従業員リスト取得エラー: {str(e)}")

    def add_attendance_record(self, employee_id: str, last_name: str, first_name: str,
                             punch_type: str, status: str) -> bool:
        """打刻記録を追加

        Args:
            employee_id: 従業員番号
            last_name: 苗字
            first_name: 名前
            punch_type: 打刻種別（出勤/退勤）
            status: ステータス
        """
        try:
            worksheet = self.spreadsheet.worksheet(config.ATTENDANCE_SHEET)
            now = datetime.now()

            # マネーフォワード形式に合わせた行を作成
            # 列: 従業員番号, 苗字, 名前, 打刻所属日, 打刻日, 打刻時間, 打刻種別
            punch_date = now.strftime("%Y/%m/%d")
            punch_time = now.strftime("%H:%M")

            # 従業員番号をテキストに変換（ゼロ落ち防止）
            row = [str(employee_id), last_name, first_name, punch_date, punch_date, punch_time, punch_type]
            worksheet.insert_row(row, index=2)
            return True
        except Exception as e:
            raise Exception(f"打刻記録追加エラー: {str(e)}")

    def get_attendance_records(self) -> List[Dict[str, str]]:
        """打刻記録をすべて取得"""
        try:
            worksheet = self.spreadsheet.worksheet(config.ATTENDANCE_SHEET)
            # get_all_values()を使ってセルの生の値を取得
            all_values = worksheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []

            # ヘッダー行とデータ行を分離
            headers = all_values[0]
            records = []

            for row in all_values[1:]:
                record = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        # すべての値を文字列として保存
                        record[header] = str(row[i]) if row[i] else ""
                records.append(record)

            return records
        except Exception as e:
            raise Exception(f"打刻記録取得エラー: {str(e)}")

    def export_to_csv(self, format_type: str = "simple", records: List[Dict] = None, employees: List[Dict] = None) -> str:
        """打刻記録を CSV 形式でエクスポート

        Args:
            format_type: 'simple' = シンプル形式, 'moneyforward' = マネーフォワード形式
            records: 打刻記録（Noneの場合は取得）
            employees: 従業員リスト（Noneの場合は取得）

        Returns:
            CSV文字列
        """
        try:
            if records is None:
                records = self.get_attendance_records()
            if employees is None:
                employees = self.get_employees()

            if format_type == "moneyforward":
                return self._export_moneyforward_format(records, employees)
            else:
                return self._export_simple_format(records)

        except Exception as e:
            raise Exception(f"CSV エクスポートエラー: {str(e)}")

    def _export_simple_format(self, records: List[Dict]) -> str:
        """シンプル形式でエクスポート"""
        output = io.StringIO()
        if records:
            fieldnames = ["従業員ID", "従業員名", "打刻種別", "日時", "ステータス"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        return output.getvalue()

    def _export_moneyforward_format(self, records: List[Dict], employees: List[Dict] = None) -> str:
        """マネーフォワード Cloud 勤怠形式でエクスポート

        形式: 従業員番号,苗字,名前,打刻所属日,打刻日,打刻時間,打刻種別
        注：Shift_JIS エンコーディングは main.py で処理
        """
        # 従業員マスタを取得（従業員番号を付与するため）
        if employees is None:
            employees = self.get_employees()

        employee_num_map = {
            f"{emp.get('苗字', '')}{emp.get('名前', '')}": str(emp.get('従業員番号', ''))
            for emp in employees
        }

        output = io.StringIO()
        writer = csv.writer(output)

        # ヘッダー
        writer.writerow(["従業員番号", "苗字", "名前", "打刻所属日", "打刻日", "打刻時間", "打刻種別"])

        # データ行
        for record in records:
            last_name = record.get("苗字", "")
            first_name = record.get("名前", "")
            employee_key = f"{last_name}{first_name}"

            # 従業員番号を取得
            emp_num = employee_num_map.get(employee_key, "")

            writer.writerow([
                emp_num,  # 従業員番号
                last_name,
                first_name,
                record.get("打刻所属日", ""),
                record.get("打刻日", ""),
                record.get("打刻時間", ""),
                record.get("打刻種別", "")
            ])

        return output.getvalue()
