import config

class AttendanceService:
    def __init__(self, sheets_service):
        """打刻サービスを初期化

        Args:
            sheets_service: GoogleSheetsService インスタンス
        """
        self.sheets_service = sheets_service

    def record_attendance(self, employee_id: str, last_name: str, first_name: str,
                         punch_type: str) -> tuple[bool, str]:
        """打刻を記録

        Args:
            employee_id: 従業員ID
            last_name: 苗字
            first_name: 名前
            punch_type: 打刻種別（出勤/退勤）

        Returns:
            (成功フラグ, メッセージ)
        """
        try:
            # Google Sheets に記録を追加
            self.sheets_service.add_attendance_record(
                employee_id,
                last_name,
                first_name,
                punch_type,
                config.STATUS_SUCCESS
            )

            return True, f"✅ {punch_type}を記録しました"

        except Exception as e:
            return False, f"❌ エラー: {str(e)}"
