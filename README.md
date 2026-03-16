# Streamlit 留言板 (官方 st.connection 寫法)

這個專案使用 `st.connection` + `GSheetsConnection` 連接私有 Google Sheet，讓使用者在網頁留言並儲存。

## 1. 安裝套件

```bash
pip install -r requirements.txt
```

## 2. 建立 Google Service Account

1. 到 Google Cloud Console 建立專案。
2. 啟用 Google Sheets API 與 Google Drive API。
3. 建立 Service Account 並下載 JSON 金鑰。
4. 在目標 Google Sheet 點擊分享，加入 service account 的 `client_email`，給 `Editor` 權限。

## 3. 設定 Streamlit secrets

在專案根目錄建立 `.streamlit/secrets.toml`：

```toml
worksheet_name = "comment"

[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/你的試算表ID/edit#gid=0"
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

注意事項：

- `private_key` 內換行必須保留 `\n`。
- `.streamlit/secrets.toml` 不要提交到 Git。

## 4. 啟動

```bash
streamlit run app.py
```

## 5. 功能

- 使用者可輸入暱稱與留言。
- 按下送出後寫入 Google Sheet。
- 頁面會顯示最新 20 筆留言。
