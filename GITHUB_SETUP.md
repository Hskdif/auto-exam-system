# GitHub 設定與部署指南

## 📌 概述

本指南將引導你完成以下步驟：
1. 建立 GitHub 儲存庫
2. 推送程式碼到 GitHub
3. 連接 Streamlit Cloud 進行自動部署

---

## 第一步：建立 GitHub 儲存庫

### 1.1 前置準備

- 擁有 GitHub 帳號（若無，前往 [github.com](https://github.com) 註冊）
- 已安裝 Git（下載：[git-scm.com](https://git-scm.com)）

### 1.2 建立新儲存庫

1. 登入 [GitHub](https://github.com)
2. 點擊右上角「+」→「New repository」
3. 填寫以下資訊：
   - **Repository name**：`auto-exam-system`
   - **Description**：`自動化雲端出卷系統 - Automated Cloud Exam System`
   - **Public/Private**：選擇 **Public**（Streamlit Cloud 需要公開存取）
   - **Initialize this repository with**：不勾選任何選項
4. 點擊「Create repository」

### 1.3 複製儲存庫 URL

建立完成後，你會看到一個頁面，複製 HTTPS URL：

```
https://github.com/[你的用戶名]/auto-exam-system.git
```

---

## 第二步：推送程式碼到 GitHub

### 2.1 初始化本地 Git 儲存庫

在你的專案資料夾中打開終端機，執行：

```bash
# 初始化 Git
git init

# 新增所有檔案
git add .

# 檢查狀態
git status
```

你應該會看到所有檔案都被列為「new file」。

### 2.2 設定 Git 使用者資訊

首次使用 Git 時，需要設定使用者資訊：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的郵箱@example.com"
```

### 2.3 建立初始提交

```bash
git commit -m "Initial commit: Streamlit exam system with Google Sheets integration"
```

### 2.4 新增遠端儲存庫

```bash
git remote add origin https://github.com/[你的用戶名]/auto-exam-system.git
```

驗證是否成功：

```bash
git remote -v
```

應該看到：
```
origin  https://github.com/[你的用戶名]/auto-exam-system.git (fetch)
origin  https://github.com/[你的用戶名]/auto-exam-system.git (push)
```

### 2.5 推送到 GitHub

```bash
# 重新命名分支為 main（如果需要）
git branch -M main

# 推送到 GitHub
git push -u origin main
```

系統會要求輸入 GitHub 帳號和密碼（或 Personal Access Token）。

### 2.6 驗證推送成功

1. 在瀏覽器中打開你的 GitHub 儲存庫
2. 應該能看到所有檔案已上傳

---

## 第三步：部署到 Streamlit Cloud

### 3.1 連接 Streamlit Cloud

1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
2. 點擊「Sign in」
3. 選擇「Sign in with GitHub」
4. 授權 Streamlit 存取你的 GitHub 帳號

### 3.2 部署應用

1. 點擊「Create app」
2. 填寫以下資訊：
   - **Repository**：選擇 `[你的用戶名]/auto-exam-system`
   - **Branch**：選擇 `main`
   - **Main file path**：輸入 `app.py`
3. 點擊「Deploy」

### 3.3 等待部署完成

Streamlit Cloud 會自動：
1. 克隆你的儲存庫
2. 安裝 `requirements.txt` 中的依賴
3. 執行 `app.py`
4. 提供一個公開 URL

部署通常需要 2-5 分鐘。完成後，你會看到一個類似以下的 URL：

```
https://auto-exam-system-[random-id].streamlit.app
```

---

## 第四步：更新程式碼

### 4.1 本地修改

1. 編輯你的程式碼（例如 `app.py`）
2. 測試修改：
   ```bash
   streamlit run app.py
   ```

### 4.2 推送更新

```bash
# 新增變更
git add .

# 提交
git commit -m "新增功能：描述你的更改"

# 推送
git push origin main
```

### 4.3 自動部署

Streamlit Cloud 會自動偵測 GitHub 的更新，並重新部署應用。

你可以在 Streamlit Cloud 儀表板中監控部署進度。

---

## 常見問題

### Q1：如何更新 Google Sheets ID？

**A**：使用者在應用的左側邊欄直接輸入新的 ID，無需更新程式碼。

### Q2：如何新增新功能？

**A**：
1. 在本地編輯 `app.py`
2. 測試功能
3. 推送到 GitHub
4. Streamlit Cloud 自動部署

### Q3：如何回滾到之前的版本？

**A**：
1. 在 GitHub 中查看提交歷史
2. 點擊要回滾的提交
3. 點擊「Browse the repository at this point in the history」
4. 複製該提交的 SHA
5. 在本地執行：
   ```bash
   git reset --hard [commit-sha]
   git push --force origin main
   ```

### Q4：Streamlit Cloud 部署失敗怎麼辦？

**A**：
1. 檢查 `requirements.txt` 是否包含所有依賴
2. 確認 `app.py` 沒有語法錯誤
3. 在 Streamlit Cloud 儀表板中查看部署日誌
4. 常見錯誤：
   - 缺少依賴：在 `requirements.txt` 中新增
   - 檔案路徑錯誤：確認相對路徑正確
   - Python 版本不相容：在 `runtime.txt` 中指定版本

### Q5：如何設定私密變數（如 API 密鑰）？

**A**：
1. 在 Streamlit Cloud 應用頁面點擊「Settings」
2. 點擊「Secrets」
3. 新增你的密鑰（格式為 TOML）
4. 在程式碼中使用：
   ```python
   import streamlit as st
   api_key = st.secrets["api_key"]
   ```

---

## 進階：自訂部署設定

### 建立 `runtime.txt`（可選）

指定 Python 版本：

```
python-3.11
```

### 建立 `.streamlit/config.toml`（可選）

自訂 Streamlit 設定：

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false

[logger]
level = "info"
```

---

## 監控與維護

### 在 Streamlit Cloud 儀表板中

1. 查看應用狀態
2. 查看部署日誌
3. 查看應用使用統計
4. 管理應用設定

### 本地開發最佳實踐

1. **定期提交**：
   ```bash
   git commit -m "描述性的提交訊息"
   ```

2. **使用分支進行開發**：
   ```bash
   git checkout -b feature/新功能
   # 開發...
   git push origin feature/新功能
   # 在 GitHub 上建立 Pull Request
   ```

3. **定期同步**：
   ```bash
   git pull origin main
   ```

---

## 故障排除

### 問題 1：推送時認證失敗

**解決方案**：
1. 使用 Personal Access Token 代替密碼
2. 在 GitHub 設定中建立 Token：Settings → Developer settings → Personal access tokens
3. 選擇 `repo` 權限
4. 複製 Token 並在推送時使用

### 問題 2：Streamlit Cloud 無法找到 `app.py`

**解決方案**：
1. 確認 `app.py` 在儲存庫根目錄
2. 確認檔案名稱完全相同（區分大小寫）
3. 重新部署應用

### 問題 3：應用運行緩慢

**解決方案**：
1. 優化 Google Sheets 讀取（新增快取）
2. 減少不必要的計算
3. 升級 Streamlit Cloud 方案

---

## 總結

你現在已經完成了：

✅ 建立 GitHub 儲存庫  
✅ 推送程式碼到 GitHub  
✅ 部署到 Streamlit Cloud  
✅ 設定自動部署流程  

現在，每當你推送程式碼到 GitHub 時，Streamlit Cloud 會自動部署新版本。

**祝你使用愉快！** 🚀
