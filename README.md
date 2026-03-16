# Streamlit 專家評估系統（登入基礎版）

此版本先完成：
1. 登入頁面
2. 送出帳密時，即時到 Google Sheet 驗證

## 1) 安裝套件

```bash
pip install -r requirements.txt
```

## 2) 建立 Streamlit Secrets

請在專案根目錄建立 `.streamlit/secrets.toml`，內容範例如下：

```toml
[google_sheet]
sheet_id = "你的_google_sheet_id"
worksheet_name = "accounts"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"
```

## 3) Google Sheet 欄位格式

請建立一個工作表（例如 `accounts`），第一列標題建議如下：

- `username`
- `password`
- `active`

範例資料：

| username | password | active |
| --- | --- | --- |
| admin | 123456 | TRUE |
| expert_a | pass001 | TRUE |
| disabled_user | abc123 | FALSE |

> 目前登入驗證為明碼比對。你之後可改成雜湊比對（例如 bcrypt）。

## 4) 授權服務帳號存取 Google Sheet

1. 將 service account 的 `client_email` 加到 Google Sheet 共用名單
2. 權限至少給 Viewer（讀取帳密）

## 5) 啟動

```bash
streamlit run app.py
```

## 備註

- 每次按下登入，都會重新讀取 Google Sheet 進行驗證（非快取）。
- 登入成功後會進入簡單首頁，後續可擴充專家評估表單與寫回結果。
