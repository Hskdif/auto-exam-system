# 自動化雲端出卷系統 - 專案交付總結

**專案名稱**：自動化雲端出卷系統 (Automated Cloud Exam System)  
**完成日期**：2026 年 2 月 22 日  
**開發者**：Manus AI  
**架構**：Google Sheets + Streamlit + Streamlit Cloud

---

## 📌 專案概述

本專案實現了「三層蛋糕」架構的自動化出卷系統，完全分離資料層與邏輯層，確保題庫和程式可獨立更新，互不影響。

### 核心特色

| 特色 | 說明 |
|------|------|
| **資料獨立** | Google Sheets 題庫，隨時編輯，無需重新部署 |
| **程式獨立** | Streamlit 應用，修改功能後自動部署 |
| **零停機** | 題庫更新不影響程式，程式更新不影響題庫 |
| **免費使用** | Google Sheets 免費，Streamlit Cloud 免費方案足夠 |
| **易於維護** | 清晰的架構，易於擴展和自訂 |

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────────────────────────┐
│                  🌐 部署層                              │
│           Streamlit Cloud (自動部署)                    │
│  https://auto-exam-system-[id].streamlit.app            │
├─────────────────────────────────────────────────────────┤
│                  🧠 邏輯層                              │
│  Streamlit 應用 (app.py)                               │
│  - 題庫讀取與快取                                       │
│  - 智能篩選（科目、題型、分數）                         │
│  - 隨機出卷演算法                                       │
│  - 多格式匯出（Word、PDF）                             │
├─────────────────────────────────────────────────────────┤
│                  📊 資料層                              │
│  Google Sheets 題庫                                     │
│  - ID、類型、科目、題目內容、參考解答、分數             │
│  - 隨時編輯，無需技術知識                               │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 交付物清單

### 核心程式碼

| 檔案 | 用途 | 說明 |
|------|------|------|
| `app.py` | 主應用程式 | 完整的 Streamlit 應用，包含所有功能 |
| `requirements.txt` | 依賴管理 | Python 套件清單，用於部署 |
| `.gitignore` | Git 設定 | 忽略敏感檔案和快取 |

### 文件與指南

| 檔案 | 用途 | 內容 |
|------|------|------|
| `README.md` | 專案說明 | 完整的專案介紹和使用指南 |
| `QUICK_START.md` | 快速開始 | 5 分鐘快速部署指南 |
| `DEPLOYMENT_GUIDE.md` | 詳細部署 | 四個階段的完整部署說明 |
| `GITHUB_SETUP.md` | GitHub 設定 | GitHub 儲存庫建立和推送指南 |
| `GOOGLE_SHEETS_TEMPLATE.md` | 題庫設定 | Google Sheets 題庫模板和最佳實踐 |
| `PROJECT_SUMMARY.md` | 本文件 | 專案交付總結 |

---

## 🎯 核心功能

### 1. 題庫管理

**位置**：Google Sheets  
**功能**：
- 在線編輯題目（無需程式知識）
- 支援多個科目和題型
- 自動版本控制和備份
- 隨時隨地編輯（手機、平板、電腦）

**必要欄位**：
```
ID | 類型 | 科目 | 題目內容 | 參考解答 | 分數
```

### 2. 智能篩選

**位置**：Streamlit 應用左側邊欄  
**篩選維度**：
- **科目篩選**：選擇要包含的法律科目
- **題型篩選**：選擇申論題、實例題等
- **分數篩選**：設定題目分數範圍
- **目標總分**：設定考卷目標分數

### 3. 隨機出卷

**演算法**：
1. 隨機排序題目
2. 貪心選擇：逐題加入，直到達到目標分數
3. 返回選中題目和實際分數

**特點**：
- 確保題目多樣性
- 盡量接近目標分數
- 支援自訂目標分數

### 4. 多格式匯出

**支援格式**：
- **Word (.docx)**：保留格式，便於編輯
- **PDF**：便於列印和分享

**匯出內容**：
- 考卷標題和基本資訊
- 所有題目（題號、分數、科目、類型）
- 題目內容和參考解答
- 生成時間和總分

---

## 🚀 部署步驟

### 第一步：準備 Google Sheets 題庫（2 分鐘）

1. 建立 Google Sheets 試算表
2. 設定欄位：ID、類型、科目、題目內容、參考解答、分數
3. 新增至少 3 題題目
4. 分享為「任何有連結的人都可以檢視」
5. 複製試算表 ID

### 第二步：本地測試（2 分鐘）

```bash
# 安裝依賴
pip install -r requirements.txt

# 運行應用
streamlit run app.py

# 打開瀏覽器
# http://localhost:8501
```

### 第三步：推送到 GitHub（1 分鐘）

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/[用戶名]/auto-exam-system.git
git branch -M main
git push -u origin main
```

### 第四步：部署到 Streamlit Cloud（1 分鐘）

1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
2. 點擊「Create app」
3. 選擇儲存庫、分支、主檔案
4. 點擊「Deploy」

**完成！** 應用已上線。

---

## 📊 技術棧

| 層級 | 技術 | 版本 | 用途 |
|------|------|------|------|
| **前端** | Streamlit | 1.28.1 | 網頁介面 |
| **後端** | Python | 3.8+ | 邏輯處理 |
| **資料** | Google Sheets | - | 題庫存儲 |
| **匯出** | python-docx | 0.8.11 | Word 匯出 |
| **匯出** | reportlab | 4.0.7 | PDF 匯出 |
| **資料處理** | pandas | 2.0.3 | 資料操作 |
| **部署** | Streamlit Cloud | - | 自動部署 |
| **版本控制** | GitHub | - | 程式碼管理 |

---

## 🔄 維護與更新流程

### 更新題庫

**操作對象**：Google Sheets  
**影響範圍**：只有題庫  
**步驟**：
1. 打開 Google Sheets
2. 新增或修改題目
3. 重新整理 Streamlit 應用
4. ✅ 新題目立即可用

**優勢**：無需技術知識，隨時編輯

### 更新程式功能

**操作對象**：GitHub 程式碼  
**影響範圍**：只有應用功能  
**步驟**：
1. 編輯本地 `app.py`
2. 本地測試：`streamlit run app.py`
3. 推送到 GitHub：`git push origin main`
4. ✅ Streamlit Cloud 自動部署

**優勢**：自動部署，無需手動操作

---

## 💡 使用場景

### 場景 1：法律教育機構

**需求**：定期為學生生成隨機考卷  
**解決方案**：
1. 在 Google Sheets 中維護題庫
2. 每次生成新考卷時，使用應用隨機出卷
3. 匯出為 PDF 列印或 Word 編輯

### 場景 2：線上考試平台

**需求**：動態管理題庫和出卷規則  
**解決方案**：
1. 題庫存放在 Google Sheets（易於管理）
2. 應用邏輯存放在 GitHub（易於版本控制）
3. 部署在 Streamlit Cloud（自動更新）

### 場景 3：個人學習助手

**需求**：自訂複習考卷  
**解決方案**：
1. 建立個人題庫
2. 按科目和難度篩選
3. 生成個性化考卷

---

## 🔐 安全性考慮

### Google Sheets 安全性

- **公開分享**：試算表設為「任何有連結的人都可以檢視」
- **讀取限制**：應用只讀取試算表，不修改
- **敏感資訊**：避免在試算表中存放敏感資訊

### Streamlit Cloud 安全性

- **程式碼保護**：程式碼存放在 GitHub（可設為私密）
- **祕密管理**：使用 Streamlit Cloud 的 Secrets 功能管理敏感資訊
- **HTTPS**：Streamlit Cloud 自動提供 HTTPS

### 建議措施

1. **定期備份**：定期下載 Google Sheets 備份
2. **版本控制**：使用 GitHub 進行版本管理
3. **存取控制**：限制誰可以編輯 Google Sheets
4. **監控日誌**：監控應用使用情況

---

## 📈 效能優化

### 快取策略

應用使用 Streamlit 的 `@st.cache_data` 裝飾器快取 Google Sheets 資料，減少 API 呼叫。

```python
@st.cache_data(ttl=300)  # 5 分鐘快取
def load_google_sheets(sheet_id):
    # 讀取 Google Sheets
    ...
```

### 優化建議

1. **增加快取時間**：如果題庫不常變化，可增加快取時間
2. **批量操作**：避免頻繁的小規模更新
3. **資料清理**：定期清理不使用的題目

---

## 🛠️ 進階自訂

### 新增科目

在 Google Sheets 的「科目」欄位新增科目名稱即可。應用會自動識別。

### 新增題型

在 Google Sheets 的「類型」欄位新增題型名稱即可。應用會自動識別。

### 修改匯出格式

編輯 `app.py` 中的 `export_to_word()` 和 `export_to_pdf()` 函數。

### 新增難度篩選

1. 在 Google Sheets 新增「難度」欄位
2. 在 `app.py` 中新增篩選邏輯
3. 推送到 GitHub，自動部署

### 新增統計功能

在 `app.py` 中新增統計邏輯，例如按科目統計題目數量。

---

## 📚 文件結構

```
auto-exam-system/
├── app.py                      # 主應用程式（Streamlit）
├── requirements.txt            # Python 依賴
├── .gitignore                  # Git 忽略設定
├── README.md                   # 專案說明
├── QUICK_START.md              # 快速開始指南
├── DEPLOYMENT_GUIDE.md         # 詳細部署指南
├── GITHUB_SETUP.md             # GitHub 設定指南
├── GOOGLE_SHEETS_TEMPLATE.md   # Google Sheets 模板
└── PROJECT_SUMMARY.md          # 本文件
```

---

## 🐛 常見問題

### Q1：如何新增新科目？

**A**：在 Google Sheets 的「科目」欄位新增科目名稱即可。應用會自動識別。

### Q2：如何修改匯出格式？

**A**：編輯 `app.py` 中的 `export_to_word()` 和 `export_to_pdf()` 函數。

### Q3：無法連接 Google Sheets？

**A**：
1. 確認試算表已分享為「任何有連結的人都可以檢視」
2. 確認試算表 ID 正確複製
3. 檢查網路連接

### Q4：Streamlit Cloud 部署失敗？

**A**：
1. 檢查 `requirements.txt` 是否包含所有依賴
2. 查看部署日誌找出錯誤
3. 確認 `app.py` 沒有語法錯誤

### Q5：如何備份題庫？

**A**：
1. 在 Google Sheets 點擊「檔案」→「下載」
2. 選擇「逗號分隔值 (.csv)」
3. 定期保存備份

---

## 🎓 學習資源

### Streamlit 文件

- [Streamlit 官方文件](https://docs.streamlit.io)
- [Streamlit Cloud 文件](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit 教程](https://docs.streamlit.io/library/get-started)

### Google Sheets API

- [Google Sheets API 文件](https://developers.google.com/sheets)
- [gspread 文件](https://docs.gspread.org)

### Python 套件

- [pandas 文件](https://pandas.pydata.org/docs)
- [python-docx 文件](https://python-docx.readthedocs.io)
- [reportlab 文件](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

## 🎉 下一步

1. ✅ **完成部署**：按照 [QUICK_START.md](QUICK_START.md) 快速部署
2. 📖 **閱讀文件**：詳細了解 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. 🔧 **自訂應用**：根據需求修改 `app.py`
4. 📊 **新增題目**：在 Google Sheets 中新增題目
5. 🚀 **分享應用**：與他人分享你的應用

---

## 📞 支援與反饋

### 獲取幫助

- 📖 查看 [README.md](README.md)
- 🚀 參考 [QUICK_START.md](QUICK_START.md)
- 📋 查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- 🔗 查看 [GITHUB_SETUP.md](GITHUB_SETUP.md)

### 報告問題

- 在 GitHub 上建立 Issue
- 查看應用日誌找出錯誤
- 檢查 Streamlit Cloud 部署日誌

---

## 📄 授權

MIT License - 自由使用和修改

---

## 🙏 致謝

感謝使用本系統！祝你出卷順利！

**Made with ❤️ for educators and students**

---

## 版本資訊

| 項目 | 值 |
|------|-----|
| **系統版本** | 1.0.0 |
| **發佈日期** | 2026-02-22 |
| **Python 版本** | 3.8+ |
| **Streamlit 版本** | 1.28.1 |
| **狀態** | 生產就緒 |

---

**專案完成日期**：2026 年 2 月 22 日  
**開發者**：Manus AI  
**最後更新**：2026 年 2 月 22 日
