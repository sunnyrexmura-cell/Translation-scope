import requests
from datetime import datetime
import config

class MoneyForwardService:
    def __init__(self):
        """マネーフォワード API サービスを初期化"""
        self.base_url = config.MF_API_BASE_URL
        self.api_key = config.MF_API_KEY

    def punch_clock(self, employee_id: str, punch_type: str) -> bool:
        """打刻をマネーフォワードに送信

        Args:
            employee_id: 従業員ID
            punch_type: 打刻種別（出勤/退勤）

        Returns:
            成功時 True、失敗時 False
        """
        try:
            if not self.api_key:
                raise Exception("MF_API_KEY が設定されていません")

            # マネーフォワード API エンドポイント
            # 実際のエンドポイントは API 仕様に合わせて調整が必要
            endpoint = f"{self.base_url}/v1/punch_clock"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "employee_id": employee_id,
                "punch_type": punch_type,
                "timestamp": datetime.now().isoformat()
            }

            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                return True
            else:
                raise Exception(f"API エラー: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"打刻送信エラー: {str(e)}")
            return False
