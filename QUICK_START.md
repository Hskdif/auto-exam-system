# 🚀 快速開始指南（5 分鐘上手）

## 📌 三步快速部署

### 第 1 步：準備 Google Sheets 題庫（2 分鐘）

#### 1.1 建立試算表
- 前往 [Google Sheets](https://sheets.google.com)
- 點擊「建立新試算表」
- 命名為 `法律考題題庫`

#### 1.2 設定欄位（第一列）
```
A1: ID          B1: 類型        C1: 科目      D1: 題目內容      E1: 參考解答      F1: 分數
```

#### 1.3 新增至少 3 題
```
Q001    申論題    民法    甲向乙購買機車...    本題涉及民法物權...    25
Q002    實例題    刑法    某甲持刀搶劫...      構成搶劫罪...          50
Q003    申論題    民訴    民事訴訟程序...      民訴法第一編...        25
```

#### 1.4 分享試算表
- 點擊「分享」
- 選擇「任何有連結的人都可以檢視」
- 複製連結，提取 ID：
  ```
  https://docs.google.com/spreadsheets/d/[ID]/edit
                                            ^^^^
  ```

### 第 2 步：本地測試（2 分鐘）

#### 2.1 安裝依賴
```bash
pip install -r requirements.txt
```

#### 2.2 運行應用
```bash
streamlit run app.py
```

#### 2.3 測試功能
1. 打開 `http://localhost:8501`
2. 在左側邊欄輸入你的 Google Sheets ID
3. 點擊「隨機生成考卷」
4. 下載 Word 或 PDF

### 第 3 步：部署到 Streamlit Cloud（1 分鐘）

#### 3.1 推送到 GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/[你的用戶名]/auto-exam-system.git
git branch -M main
git push -u origin main
```

#### 3.2 部署到 Streamlit Cloud
1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
2. 點擊「Create app」
3. 選擇儲存庫 `auto-exam-system`
4. 選擇分支 `main`
5. 設定 Main file 為 `app.py`
6. 點擊「Deploy」

**完成！** 🎉 你的應用已上線。

---

## 📊 系統架構一覽

```
┌─────────────────────────────────────────┐
│  🌐 Streamlit Cloud                     │  自動部署
│  https://auto-exam-system-xxx.streamlit.app
├─────────────────────────────────────────┤
│  📝 app.py (Streamlit 應用)             │  篩選、隨機、匯出
├─────────────────────────────────────────┤
│  📊 Google Sheets 題庫                  │  題目、答案、分數
└─────────────────────────────────────────┘
```

---

## 🎯 核心功能

| 功能 | 說明 |
|------|------|
| 📊 **題庫管理** | 在 Google Sheets 中管理所有考題 |
| 🔍 **智能篩選** | 按科目、題型、分數篩選 |
| 🎲 **隨機出卷** | 自動生成符合目標分數的考卷 |
| 📥 **多格式匯出** | 支援 Word 和 PDF 格式 |

---

## 📝 常用命令

### Git 命令
```bash
# 推送更新
git add .
git commit -m "描述你的更改"
git push origin main

# 查看狀態
git status

# 查看提交歷史
git log --oneline
```

### Streamlit 命令
```bash
# 本地運行
streamlit run app.py

# 清除快取
streamlit cache clear

# 檢查版本
streamlit version
```

---

## 🔄 更新流程

### 更新題庫
1. 打開 Google Sheets
2. 新增或修改題目
3. 重新整理 Streamlit 應用
4. ✅ 新題目立即可用

### 更新程式功能
1. 編輯 `app.py`
2. 本地測試：`streamlit run app.py`
3. 推送到 GitHub：`git push origin main`
4. ✅ Streamlit Cloud 自動部署

---

## 🐛 常見問題

### Q：無法連接 Google Sheets？
**A**：
1. 確認試算表已分享為「任何有連結的人都可以檢視」
2. 確認 ID 正確複製
3. 檢查網路連接

### Q：Streamlit Cloud 部署失敗？
**A**：
1. 檢查 `requirements.txt` 是否包含所有依賴
2. 查看部署日誌找出錯誤
3. 確認 `app.py` 沒有語法錯誤

### Q：如何新增新功能？
**A**：
1. 編輯 `app.py`
2. 測試修改
3. 推送到 GitHub
4. Streamlit Cloud 自動部署

### Q：如何備份題庫？
**A**：
1. 在 Google Sheets 點擊「檔案」→「下載」
2. 選擇「逗號分隔值 (.csv)」
3. 定期保存備份

---

## 📚 詳細文件

- 📖 [完整部署指南](DEPLOYMENT_GUIDE.md)
- 📋 [Google Sheets 模板](GOOGLE_SHEETS_TEMPLATE.md)
- 🔗 [GitHub 設定指南](GITHUB_SETUP.md)
- 📘 [README](README.md)

---

## 🎓 下一步

1. ✅ 完成快速開始
2. 📖 閱讀 [完整部署指南](DEPLOYMENT_GUIDE.md)
3. 🔧 自訂應用功能
4. 📊 新增更多題目
5. 🚀 分享你的應用

---

## 💡 小提示

- **題庫更新無需重新部署**：修改 Google Sheets 後，重新整理頁面即可
- **程式更新自動部署**：推送到 GitHub 後，Streamlit Cloud 自動部署
- **免費使用**：Google Sheets 和 Streamlit Cloud 免費方案足夠使用
- **隨時隨地編輯**：在手機上打開 Google Sheets 應用，隨時新增題目

---

## 🎉 祝賀

你已經完成了自動化出卷系統的部署！

現在你可以：
- 📝 在 Google Sheets 中管理題庫
- 🎲 自動生成隨機考卷
- 📥 匯出為 Word 或 PDF
- 🌐 與他人分享你的應用

**開始使用吧！** 🚀

---

**需要幫助？** 查看 [完整部署指南](DEPLOYMENT_GUIDE.md) 或 [README](README.md)
