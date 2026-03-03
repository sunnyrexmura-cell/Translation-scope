# マネーフォワード勤怠管理 - Streamlitアプリ

タブレット・スマートフォンでの簡単な打刻記録アプリケーション

## 機能

- ✅ 従業員選択ドロップダウン
- ✅ 出勤/退勤ボタン（タッチ最適化）
- ✅ Google Sheets への自動記録
- ✅ マネーフォワード API 連携
- ✅ レスポンシブデザイン（タブレット対応）

## インストール

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env` ファイルを作成し、以下を設定：

```
MF_API_KEY=your_moneyforward_api_key
GOOGLE_SHEETS_ID=your_google_sheets_id
GOOGLE_SHEETS_CREDENTIALS_JSON={"type": "service_account", "project_id": "..."}
```

## ローカル実行

```bash
streamlit run main.py
```

ブラウザで `http://localhost:8501` にアクセス

## デプロイ（Streamlit Cloud）

### 前提条件
- GitHub リポジトリ
- Google Cloud Service Account
- Streamlit Cloud アカウント

### デプロイ手順

1. GitHub にコミット・プッシュ
2. Streamlit Cloud で新規プロジェクト作成
3. GitHub リポジトリを選択
4. 環境変数を設定：
   - `MF_API_KEY`
   - `GOOGLE_SHEETS_ID`
   - `GOOGLE_SHEETS_CREDENTIALS_JSON`
5. Deploy ボタンをクリック

## ファイル構成

```
mf-kintai-app/
├── config.py                           # 設定管理
├── main.py                             # Streamlit メイン
├── requirements.txt                    # 依存パッケージ
├── .streamlit/
│   └── config.toml                     # Streamlit設定
├── services/
│   ├── __init__.py
│   ├── google_sheets_service.py        # Sheet読み書き
│   ├── moneyforward_service.py         # MF API連携
│   └── attendance_service.py           # 打刻ロジック
├── .gitignore
└── README.md
```

## トラブルシューティング

### 従業員が表示されない
- Google Sheets の認証情報を確認
- シート名が `従業員` になっているか確認

### 打刻が失敗する
- マネーフォワード API KEY を確認
- ネットワーク接続を確認

### Google Sheets に記録されない
- Service Account の書込権限を確認
- シート名が `打刻記録` になっているか確認

## 今後の拡張案

- 本日の打刻一覧表示
- 月別レポート
- Slack 通知
- オフライン対応
- ユーザー認証

## ライセンス

MIT License
