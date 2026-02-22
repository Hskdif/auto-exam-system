# 自動化雲端出卷系統 🎓

**Automated Cloud Exam System** - 基於 Google Sheets 的智能出卷平台

## 📌 核心概念：「三層蛋糕」架構

```
┌─────────────────────────────────────────┐
│  🌐 部署層：Streamlit Cloud             │  自動部署、版本管理
├─────────────────────────────────────────┤
│  🧠 邏輯層：Streamlit 應用 (app.py)    │  篩選、隨機、匯出
├─────────────────────────────────────────┤
│  📊 資料層：Google Sheets 題庫         │  題目、答案、分數
└─────────────────────────────────────────┘
```

### 🎯 核心優勢

| 優勢 | 說明 |
|------|------|
| ✅ **資料獨立** | 修改 Google Sheets，網頁自動更新，無需重新部署 |
| ✅ **程式獨立** | 更新 GitHub 程式碼，Streamlit Cloud 自動部署 |
| ✅ **零停機** | 題庫和程式可分別更新，互不影響 |
| ✅ **成本低** | Google Sheets 免費，Streamlit Cloud 免費方案足夠 |

---

## 🚀 快速開始

### 前置準備

- Python 3.8+
- Google 帳號
- GitHub 帳號（用於部署）

### 本地運行

1. **克隆或下載本專案**
   ```bash
   git clone https://github.com/[你的用戶名]/auto-exam-system.git
   cd auto-exam-system
   ```

2. **建立虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **準備 Google Sheets 題庫**
   - 參考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 的「第一階段」

5. **運行應用**
   ```bash
   streamlit run app.py
   ```

6. **打開瀏覽器**
   - 訪問 `http://localhost:8501`
   - 輸入你的 Google Sheets ID
   - 開始使用！

---

## 📚 功能說明

### 1. 題庫管理
- 在 Google Sheets 中管理所有考題
- 支援多個科目和題型
- 隨時新增、修改、刪除題目

### 2. 智能篩選
- 按科目篩選
- 按題型篩選
- 按分數範圍篩選

### 3. 隨機出卷
- 自動生成符合目標分數的考卷
- 智能演算法確保題目多樣性

### 4. 多格式匯出
- 匯出為 Word (.docx)
- 匯出為 PDF
- 保留題目、答案、分數資訊

---

## 📖 詳細指南

### Google Sheets 題庫設定

**必要欄位**（欄位名稱必須完全相同）：

| 欄位 | 類型 | 說明 |
|------|------|------|
| ID | 文字 | 題目編號（例：Q001） |
| 類型 | 文字 | 題型（例：申論題、實例題） |
| 科目 | 文字 | 科目（例：民法、刑法） |
| 題目內容 | 文字 | 完整題目敘述 |
| 參考解答 | 文字 | 標準答案 |
| 分數 | 數字 | 題目配分 |

**範例試算表**：

```
ID    類型      科目    題目內容              參考解答            分數
Q001  申論題    民法    甲向乙購買機車...    本題涉及民法...     25
Q002  實例題    刑法    某甲持刀搶劫...      構成搶劫罪...       50
Q003  申論題    民訴    民事訴訟程序...      民訴法第一編...     25
```

### 部署到 Streamlit Cloud

詳見 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 的「第三階段」

簡要步驟：
1. 推送程式碼到 GitHub
2. 連接 Streamlit Cloud
3. 選擇儲存庫和分支
4. 自動部署完成！

---

## 🔄 維護與更新流程

### 更新題庫

**操作**：編輯 Google Sheets  
**影響**：只有題庫  
**步驟**：
1. 打開 Google Sheets
2. 新增或修改題目
3. 重新整理 Streamlit 應用
4. ✅ 新題目立即可用

### 更新程式功能

**操作**：修改 GitHub 程式碼  
**影響**：只有應用功能  
**步驟**：
1. 修改本地 `app.py`
2. 提交並推送：
   ```bash
   git add app.py
   git commit -m "新增功能：..."
   git push origin main
   ```
3. Streamlit Cloud 自動部署
4. ✅ 新功能立即上線，題庫資料完全不受影響

---

## 📁 項目結構

```
auto-exam-system/
├── app.py                    # 主應用程式
├── requirements.txt          # Python 依賴
├── README.md                # 本文件
├── DEPLOYMENT_GUIDE.md      # 詳細部署指南
├── .gitignore               # Git 忽略設定
└── .streamlit/
    └── config.toml          # Streamlit 設定（可選）
```

---

## 🛠️ 技術棧

| 元件 | 技術 | 用途 |
|------|------|------|
| **前端** | Streamlit | 網頁介面 |
| **後端** | Python | 邏輯處理 |
| **資料** | Google Sheets | 題庫存儲 |
| **部署** | Streamlit Cloud | 自動部署 |
| **版本控制** | GitHub | 程式碼管理 |

---

## 📝 常見問題

### Q1：如何新增新科目？
**A**：在 Google Sheets 的「科目」欄位新增科目名稱即可。應用會自動識別。

### Q2：如何修改匯出格式？
**A**：編輯 `app.py` 中的 `export_to_word()` 和 `export_to_pdf()` 函數。

### Q3：如何新增題目難度篩選？
**A**：
1. 在 Google Sheets 新增「難度」欄位
2. 在 `app.py` 中新增篩選邏輯
3. 推送到 GitHub，自動部署

### Q4：Streamlit Cloud 免費方案有限制嗎？
**A**：免費方案限制：
- 3 個應用
- 1GB 記憶體
- 無自訂域名
- 對於小規模使用足夠

### Q5：如何備份題庫？
**A**：Google Sheets 自動保存所有版本。你也可以定期下載 CSV 備份。

---

## 🐛 故障排除

### 問題：無法連接 Google Sheets

**症狀**：應用顯示「連接失敗」

**解決方案**：
1. 確認試算表已分享為「任何有連結的人都可以檢視」
2. 確認試算表 ID 正確複製
3. 檢查網路連接
4. 確認試算表欄位名稱完全相同

### 問題：Streamlit Cloud 部署失敗

**症狀**：部署時顯示紅色錯誤

**解決方案**：
1. 檢查 `requirements.txt` 是否包含所有依賴
2. 確認 GitHub 儲存庫是 Public
3. 查看 Streamlit Cloud 的部署日誌
4. 確認 `app.py` 沒有語法錯誤

### 問題：生成的考卷分數不符

**症狀**：考卷總分超過目標分數

**解決方案**：
- 這是正常的。演算法會盡量接近目標分數，但可能因為題目分數組合而無法完全相符
- 可以調整目標分數或題目分數設定

---

## 📞 支援與反饋

- 📖 詳細指南：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- 🐛 報告問題：[GitHub Issues](https://github.com/[你的用戶名]/auto-exam-system/issues)
- 📚 Streamlit 文件：[docs.streamlit.io](https://docs.streamlit.io)
- 📊 Google Sheets API：[developers.google.com/sheets](https://developers.google.com/sheets)

---

## 📄 授權

MIT License - 自由使用和修改

---

## 🎉 致謝

感謝使用本系統！祝你出卷順利！

**Made with ❤️ for educators and students**
