import streamlit as st
from datetime import datetime
from services.attendance_service import AttendanceService
from services.google_sheets_service import GoogleSheetsService
import config

# ページ設定
st.set_page_config(
    page_title="勤怠管理",
    page_icon="⏰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# キャッシュキー（打刻後に自動クリア）
if "cache_buster" not in st.session_state:
    st.session_state.cache_buster = 0
if "last_punch_message" not in st.session_state:
    st.session_state.last_punch_message = None
if "last_punch_success" not in st.session_state:
    st.session_state.last_punch_success = False
if "selected_emp_index" not in st.session_state:
    st.session_state.selected_emp_index = 0

# カスタムCSS（全スタイルをまとめる）
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .datetime {
        text-align: center;
        font-size: 1.2em;
        color: #666;
        margin-bottom: 2em;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1em;
        border-radius: 0.5em;
        text-align: center;
        font-size: 1.1em;
        margin-top: 2em;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1em;
        border-radius: 0.5em;
        text-align: center;
        font-size: 1.1em;
        margin-top: 2em;
    }
    .stButton > button {
        height: 240px !important;
        font-size: 100px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
        line-height: 1.0 !important;
        padding: 0 !important;
        min-height: 240px !important;
        word-break: break-word !important;
    }
    </style>
    """, unsafe_allow_html=True)

# タイトル
st.markdown('<h1 class="title">⏰ 勤怠管理</h1>', unsafe_allow_html=True)

# 現在日時
now = datetime.now()
st.markdown(
    f'<p class="datetime">本日: {now.strftime("%Y年%m月%d日 %H:%M")}</p>',
    unsafe_allow_html=True
)

# サービス初期化（キャッシュで高速化）
@st.cache_resource
def get_services():
    sheets_service = GoogleSheetsService()
    return {
        "sheets_service": sheets_service,
        "attendance_service": AttendanceService(sheets_service)
    }

try:
    services = get_services()
    sheets_service = services["sheets_service"]
    attendance_service = services["attendance_service"]
except Exception as e:
    st.error(f"初期化エラー: {str(e)}")
    st.stop()

# 従業員リスト取得（キャッシュ）
@st.cache_data(ttl=3600)
def get_employees_cached():
    return sheets_service.get_employees()

try:
    employees = get_employees_cached()
    if not employees:
        st.warning("従業員リストが空です")
        st.stop()

    # 初期化
    if "selected_employee" not in st.session_state:
        st.session_state.selected_employee = employees[0] if employees else None

    # 従業員選択用のセレクトボックス
    col_select, col_refresh_emp = st.columns([0.85, 0.15])

    with col_select:
        # 従業員オプション生成をキャッシュ
        @st.cache_data
        def get_emp_options():
            return [(f"{emp.get('苗字', '')} {emp.get('名前', '')} (ID: {emp.get('従業員番号', '')})", emp) for emp in employees]

        emp_options_list = get_emp_options()
        emp_options = [opt[0] for opt in emp_options_list]
        emp_dict = {opt[0]: opt[1] for opt in emp_options_list}

        selected_emp_label = st.selectbox(
            "従業員を選択",
            options=emp_options,
            index=st.session_state.selected_emp_index,
            label_visibility="collapsed",
            key="emp_select"
        )
        st.session_state.selected_emp_index = emp_options.index(selected_emp_label)
        st.session_state.selected_employee = emp_dict[selected_emp_label]

    with col_refresh_emp:
        # 更新ボタン（打刻記録の更新）
        if st.button("🔄", key="refresh_button_top", use_container_width=True, help="打刻記録を更新"):
            st.session_state.cache_buster += 1

    # 選択された従業員を確認
    if st.session_state.selected_employee is None:
        st.info("👆 従業員を選択してください")
        st.stop()

    selected_employee = st.session_state.selected_employee
    employee_id = selected_employee.get("従業員番号", "").strip()
    last_name = selected_employee.get("苗字", "").strip()
    first_name = selected_employee.get("名前", "").strip()
    employee_name = f"{last_name}{first_name}"

except Exception as e:
    st.error(f"従業員リスト取得エラー: {str(e)}")
    st.stop()

# 出勤/退勤ボタン
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("📍 出勤", key="start_button", use_container_width=True):
        success, message = attendance_service.record_attendance(
            employee_id,
            last_name,
            first_name,
            config.PUNCH_TYPE_START
        )
        st.session_state.last_punch_success = success
        st.session_state.last_punch_message = message
        st.rerun()

with col2:
    if st.button("🔚 退勤", key="end_button", use_container_width=True):
        success, message = attendance_service.record_attendance(
            employee_id,
            last_name,
            first_name,
            config.PUNCH_TYPE_END
        )
        st.session_state.last_punch_success = success
        st.session_state.last_punch_message = message
        st.rerun()

# メッセージ表示（rerun の代わり）
if st.session_state.last_punch_message:
    if st.session_state.last_punch_success:
        st.markdown(
            f'<div class="success-message">{st.session_state.last_punch_message}<br>{now.strftime("%Y-%m-%d %H:%M")}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="error-message">{st.session_state.last_punch_message}</div>',
            unsafe_allow_html=True
        )
    st.session_state.last_punch_message = None

# 打刻記録の表示とCSVエクスポート
st.divider()
st.subheader("打刻記録")

try:
    # 打刻記録を取得（常に最新データを取得）
    all_records = sheets_service.get_attendance_records()

    # 選択した従業員の記録だけをフィルタリング（苗字と名前で一致）
    user_records = [r for r in all_records
                    if r.get("苗字", "").strip() == last_name and r.get("名前", "").strip() == first_name]

    if user_records:
        # 本日のデータのみを抽出
        today = now.strftime("%Y/%m/%d")
        today_records = [r for r in user_records if r.get("打刻日", "") == today]

        # 打刻時間でソート（降順 - 新しい順）
        sorted_records = sorted(
            today_records,
            key=lambda x: x.get("打刻時間", "00:00"),
            reverse=True
        )

        if sorted_records:
            # 表示用に列を整理
            display_records = []
            for r in sorted_records:
                display_records.append({
                    "打刻時間": r.get("打刻時間", ""),
                    "打刻種別": r.get("打刻種別", ""),
                    "打刻日": r.get("打刻日", "")
                })

            # テーブル表示
            st.dataframe(display_records, width="stretch", hide_index=True)
        else:
            st.info(f"本日（{today}）の打刻記録がありません")

        # 過去のデータがあればタブで表示
        past_records = [r for r in user_records if r.get("打刻日", "") != today]
        if past_records:
            with st.expander("📋 過去の打刻記録"):
                past_sorted = sorted(
                    past_records,
                    key=lambda x: (x.get("打刻日", ""), x.get("打刻時間", "00:00")),
                    reverse=True
                )
                display_past = []
                for r in past_sorted:
                    display_past.append({
                        "打刻日": r.get("打刻日", ""),
                        "打刻時間": r.get("打刻時間", ""),
                        "打刻種別": r.get("打刻種別", "")
                    })
                st.dataframe(display_past, width="stretch", hide_index=True)

        # CSVエクスポート（Shift_JIS形式）
        csv_mf = sheets_service.export_to_csv(format_type="moneyforward")
        # Shift_JIS でエンコード
        csv_bytes = csv_mf.encode('shift_jis')

        st.download_button(
            label="CSV をダウンロード",
            data=csv_bytes,
            file_name=f"attendance_{now.strftime('%Y%m%d')}.csv",
            mime="text/csv; charset=shift_jis"
        )

    else:
        st.info(f"{employee_name} さんの打刻記録がまだありません")

except Exception as e:
    st.error(f"打刻記録取得エラー: {str(e)}")
