from datetime import datetime

import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 設定網頁標題、圖示與版面
st.set_page_config(page_title="聊天板", page_icon="💬", layout="centered")
st.title("💬 聊天板")

# 建立 Google Sheets 連線（憑證設定於 .streamlit/secrets.toml 的 [connections.gsheets]）
conn = st.connection("gsheets", type=GSheetsConnection)
# 優先讀取 secrets 中的 worksheet_name，若未設定則預設使用 "comment"
worksheet_name = st.secrets.get("worksheet_name", "comment")


def load_messages() -> pd.DataFrame:
    # ttl=0 表示每次都重新從 Google Sheet 讀取，不使用快取
    df = conn.read(worksheet=worksheet_name, ttl=0)
    if df is None or df.empty:
        # 若工作表為空，回傳空的 DataFrame 並預設欄位名稱
        return pd.DataFrame(columns=["timestamp", "name", "message"])

    # 確保三個必要欄位都存在，若缺少則補空字串
    expected_columns = ["timestamp", "name", "message"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
    return df[expected_columns]


# 讓使用者輸入暱稱，預設為 Anonymous
name = st.text_input("你的暱稱", value="Anonymous")


# 用 fragment 讓訊息區塊每 5 秒自動重新從 Google Sheet 讀取，實現即時更新
@st.fragment(run_every=5)
def show_messages():
    messages_df = load_messages()
    if messages_df.empty:
        st.info("目前還沒有訊息。")
    else:
        for row in messages_df.tail(50).itertuples(index=False):
            sender = row.name if str(row.name).strip() else "Anonymous"
            timestamp = str(row.timestamp)
            # 用聊天泡泡樣式顯示每則訊息
            with st.chat_message("user"):
                st.markdown(f"**{sender}**  ")
                st.write(row.message)
                st.caption(timestamp)  # 顯示發送時間


show_messages()

# 底部輸入框，使用者輸入後按 Enter 或點送出即觸發
chat_text = st.chat_input("輸入訊息...")
if chat_text is not None:
    if not chat_text.strip():
        st.warning("訊息不能是空白。")
    else:
        # 讀取目前所有資料，加入新訊息後整筆寫回 Google Sheet
        current_df = load_messages()
        new_row = pd.DataFrame(
            [
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name.strip() if name.strip() else "Anonymous",
                    "message": chat_text.strip(),
                }
            ]
        )
        updated_df = pd.concat([current_df, new_row], ignore_index=True)
        conn.update(worksheet=worksheet_name, data=updated_df)
        st.rerun()  # 重新載入頁面以顯示最新訊息