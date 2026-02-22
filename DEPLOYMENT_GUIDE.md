# 自動化雲端出卷系統 - 完整部署指南

## 📋 目錄
1. [系統架構](#系統架構)
2. [第一階段：建立 Google Sheets 題庫](#第一階段建立-google-sheets-題庫)
3. [第二階段：開發 Streamlit 應用](#第二階段開發-streamlit-應用)
4. [第三階段：部署到 Streamlit Cloud](#第三階段部署到-streamlit-cloud)
5. [第四階段：維護與更新](#第四階段維護與更新)

---

## 系統架構

本系統採用「三層蛋糕」架構，確保**資料與程式邏輯完全分離**：

| 層級 | 元件 | 技術 | 用途 |
|------|------|------|------|
| **資料層** | Google Sheets | 雲端試算表 | 存放所有考題、答案、分數 |
| **邏輯層** | Streamlit 應用 | Python + Streamlit | 讀取題庫、篩選、隨機抽題、匯出 |
| **部署層** | Streamlit Cloud | GitHub + Streamlit Cloud | 自動部署、版本管理、持續更新 |

### 核心優勢

✅ **題庫獨立**：修改 Google Sheets 題目，網頁自動更新，無需重新部署  
✅ **程式獨立**：更新 GitHub 程式碼，Streamlit Cloud 自動重新部署  
✅ **零停機**：題庫和程式可分別更新，互不影響  
✅ **成本低**：Google Sheets 免費，Streamlit Cloud 免費方案足夠使用  

---

## 第一階段：建立 Google Sheets 題庫

### 步驟 1：建立 Google 試算表

1. 前往 [Google Sheets](https://sheets.google.com)
2. 點擊「建立新試算表」
3. 命名為 `法律考題題庫` 或你喜歡的名稱

### 步驟 2：設定欄位結構

在第一列設定以下欄位（**欄位名稱必須完全相同**）：

| 欄位 | 類型 | 說明 | 範例 |
|------|------|------|------|
| ID | 文字 | 題目編號 | Q001 |
| 類型 | 文字 | 題目類型 | 申論題 / 實例題 |
| 科目 | 文字 | 法律科目 | 民法 / 刑法 / 民訴 / 刑訴 / 行政法 / 憲法 |
| 題目內容 | 文字 | 完整題目敘述 | 甲向乙購買一輛機車，約定... |
| 參考解答 | 文字 | 標準答案 | 本題涉及民法物權編... |
| 分數 | 數字 | 題目配分 | 25 / 50 / 100 |

### 步驟 3：新增題目

在第二列開始輸入題目資料。範例：

```
ID          類型      科目    題目內容                           參考解答                    分數
Q001        申論題    民法    甲向乙購買機車...                 本題涉及民法物權編...      25
Q002        實例題    刑法    某甲持刀搶劫...                   構成搶劫罪...              50
Q003        申論題    民訴    民事訴訟程序...                   民訴法第一編...            25
```

### 步驟 4：分享試算表

1. 點擊右上角「分享」按鈕
2. 選擇「任何有連結的人都可以檢視」
3. **複製分享連結**（稍後會用到）

### 步驟 5：取得試算表 ID

從分享連結中提取試算表 ID：

```
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit?usp=sharing
                                        ^^^^^^^^
                                    這就是 SHEET_ID
```

**保存此 ID，稍後設定 Streamlit 應用時會用到。**

---

## 第二階段：開發 Streamlit 應用

### 步驟 1：安裝 Streamlit

在你的電腦上打開終端機（Terminal / Command Prompt），執行：

```bash
pip install streamlit gspread oauth2client python-docx reportlab pandas
```

### 步驟 2：建立應用程式

在你的專案資料夾中建立 `app.py` 檔案，內容如下：

```python
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import random
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import io

# ==================== 設定 ====================
st.set_page_config(
    page_title="自動化出卷系統",
    page_icon="📝",
    layout="wide"
)

# ==================== Google Sheets 連接 ====================
@st.cache_resource
def connect_to_sheets(sheet_id):
    """連接 Google Sheets（使用公開試算表）"""
    try:
        # 使用 gspread 的公開試算表連接方式
        import gspread
        from gspread_dataframe import get_as_dataframe
        
        # 如果試算表是公開的，可以直接使用 URL
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"連接失敗：{e}")
        return None

# ==================== 主程式 ====================
def main():
    st.title("📝 自動化雲端出卷系統")
    st.markdown("---")
    
    # 側邊欄設定
    with st.sidebar:
        st.header("⚙️ 系統設定")
        
        sheet_id = st.text_input(
            "Google Sheets ID",
            placeholder="貼上你的試算表 ID",
            help="從分享連結中複製 ID"
        )
        
        if sheet_id:
            # 讀取題庫
            df = connect_to_sheets(sheet_id)
            
            if df is not None:
                st.success("✅ 題庫連接成功")
                
                # 顯示題庫統計
                st.metric("總題數", len(df))
                
                # 篩選條件
                st.subheader("篩選條件")
                
                # 科目篩選
                subjects = df['科目'].unique().tolist()
                selected_subjects = st.multiselect(
                    "選擇科目",
                    subjects,
                    default=subjects
                )
                
                # 題型篩選
                types = df['類型'].unique().tolist()
                selected_types = st.multiselect(
                    "選擇題型",
                    types,
                    default=types
                )
                
                # 分數篩選
                min_score, max_score = st.slider(
                    "分數範圍",
                    int(df['分數'].min()),
                    int(df['分數'].max()),
                    (int(df['分數'].min()), int(df['分數'].max()))
                )
                
                # 目標總分
                target_score = st.number_input(
                    "目標總分",
                    min_value=25,
                    max_value=500,
                    value=100,
                    step=25
                )
                
                # 應用篩選
                filtered_df = df[
                    (df['科目'].isin(selected_subjects)) &
                    (df['類型'].isin(selected_types)) &
                    (df['分數'] >= min_score) &
                    (df['分數'] <= max_score)
                ]
                
                st.info(f"符合條件的題目：{len(filtered_df)} 題")
                
                # 生成考卷按鈕
                if st.button("🎲 隨機生成考卷", use_container_width=True):
                    if len(filtered_df) == 0:
                        st.error("沒有符合條件的題目")
                    else:
                        st.session_state.generated_exam = generate_exam(
                            filtered_df, target_score
                        )
                        st.session_state.show_exam = True
    
    # 主要內容區
    if 'show_exam' in st.session_state and st.session_state.show_exam:
        display_exam(st.session_state.generated_exam)
    else:
        st.info("👈 請在左側設定篩選條件並生成考卷")

def generate_exam(df, target_score):
    """隨機生成符合目標分數的考卷"""
    selected_questions = []
    current_score = 0
    
    # 隨機排序題目
    shuffled_df = df.sample(frac=1).reset_index(drop=True)
    
    for _, row in shuffled_df.iterrows():
        question_score = int(row['分數'])
        if current_score + question_score <= target_score:
            selected_questions.append(row)
            current_score += question_score
    
    return {
        'questions': selected_questions,
        'total_score': current_score,
        'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def display_exam(exam_data):
    """顯示生成的考卷"""
    st.subheader(f"📄 考卷 - 總分：{exam_data['total_score']} 分")
    st.caption(f"生成時間：{exam_data['generated_time']}")
    
    # 題目顯示
    for idx, question in enumerate(exam_data['questions'], 1):
        with st.container(border=True):
            st.markdown(f"### 第 {idx} 題 ({int(question['分數'])} 分)")
            st.markdown(f"**科目**：{question['科目']} | **類型**：{question['類型']}")
            st.markdown(f"**題目**：\n{question['題目內容']}")
            
            if pd.notna(question['參考解答']):
                with st.expander("查看參考解答"):
                    st.markdown(f"{question['參考解答']}")
    
    # 匯出功能
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 下載為 Word", use_container_width=True):
            word_file = export_to_word(exam_data)
            st.download_button(
                label="點擊下載 Word 檔",
                data=word_file,
                file_name=f"考卷_{exam_data['generated_time'].replace(':', '-')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    
    with col2:
        if st.button("📥 下載為 PDF", use_container_width=True):
            pdf_file = export_to_pdf(exam_data)
            st.download_button(
                label="點擊下載 PDF 檔",
                data=pdf_file,
                file_name=f"考卷_{exam_data['generated_time'].replace(':', '-')}.pdf",
                mime="application/pdf"
            )

def export_to_word(exam_data):
    """匯出為 Word 檔"""
    doc = Document()
    
    # 標題
    title = doc.add_heading('法律考試考卷', 0)
    title.alignment = 1  # 置中
    
    doc.add_paragraph(f"生成時間：{exam_data['generated_time']}")
    doc.add_paragraph(f"總分：{exam_data['total_score']} 分")
    doc.add_paragraph()
    
    # 題目
    for idx, question in enumerate(exam_data['questions'], 1):
        doc.add_heading(f"第 {idx} 題 ({int(question['分數'])} 分)", level=2)
        doc.add_paragraph(f"科目：{question['科目']} | 類型：{question['類型']}")
        doc.add_paragraph(f"題目：{question['題目內容']}")
        doc.add_paragraph()
    
    # 保存到記憶體
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output.getvalue()

def export_to_pdf(exam_data):
    """匯出為 PDF 檔"""
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # 自訂標題樣式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#000000',
        spaceAfter=30,
        alignment=1
    )
    
    story = []
    
    # 標題
    story.append(Paragraph("法律考試考卷", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # 基本資訊
    story.append(Paragraph(f"生成時間：{exam_data['generated_time']}", styles['Normal']))
    story.append(Paragraph(f"總分：{exam_data['total_score']} 分", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # 題目
    for idx, question in enumerate(exam_data['questions'], 1):
        story.append(Paragraph(f"第 {idx} 題 ({int(question['分數'])} 分)", styles['Heading2']))
        story.append(Paragraph(
            f"<b>科目：</b>{question['科目']} | <b>類型：</b>{question['類型']}",
            styles['Normal']
        ))
        story.append(Paragraph(f"<b>題目：</b>{question['題目內容']}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        if idx < len(exam_data['questions']):
            story.append(PageBreak())
    
    doc.build(story)
    output.seek(0)
    return output.getvalue()

if __name__ == "__main__":
    main()
```

### 步驟 3：本地測試

在終端機執行：

```bash
streamlit run app.py
```

應用會在 `http://localhost:8501` 開啟。測試所有功能：
- ✅ 輸入 Google Sheets ID
- ✅ 篩選科目、題型、分數
- ✅ 生成考卷
- ✅ 下載 Word 和 PDF

---

## 第三階段：部署到 Streamlit Cloud

### 步驟 1：建立 GitHub 儲存庫

1. 前往 [GitHub](https://github.com) 並登入
2. 點擊「New repository」
3. 命名為 `auto-exam-system`
4. 選擇 **Public**（方便 Streamlit Cloud 存取）
5. 點擊「Create repository」

### 步驟 2：推送程式碼到 GitHub

在你的專案資料夾中執行：

```bash
# 初始化 Git
git init

# 新增所有檔案
git add .

# 提交
git commit -m "Initial commit: Streamlit exam system"

# 新增遠端儲存庫
git remote add origin https://github.com/[你的用戶名]/auto-exam-system.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 步驟 3：部署到 Streamlit Cloud

1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
2. 點擊「Deploy an app」
3. 選擇你的 GitHub 儲存庫 `auto-exam-system`
4. 選擇 `main` 分支
5. 設定 Main file path 為 `app.py`
6. 點擊「Deploy」

Streamlit Cloud 會自動部署你的應用，並提供一個公開 URL。

### 步驟 4：設定 Secrets（可選）

如果你想使用私密的 Google Sheets（需要認證），可以在 Streamlit Cloud 設定 Secrets：

1. 在 Streamlit Cloud 應用頁面點擊「Settings」
2. 點擊「Secrets」
3. 新增你的 Google Sheets 認證資訊

---

## 第四階段：維護與更新

### 更新題庫

**操作對象**：Google Sheets  
**影響範圍**：只有題庫  
**步驟**：
1. 打開你的 Google Sheets
2. 新增或修改題目
3. 重新整理 Streamlit 應用（按 F5 或點擊右上角「Rerun」）
4. ✅ 新題目立即可用

### 更新程式功能

**操作對象**：GitHub 程式碼  
**影響範圍**：只有應用功能  
**步驟**：
1. 修改本地 `app.py`
2. 提交並推送到 GitHub：
   ```bash
   git add app.py
   git commit -m "新增功能：..."
   git push origin main
   ```
3. Streamlit Cloud 自動偵測更新並重新部署
4. ✅ 新功能立即上線，題庫資料完全不受影響

### 常見更新場景

| 場景 | 修改位置 | 重新部署 |
|------|--------|--------|
| 新增考題 | Google Sheets | ❌ 無需 |
| 修改題目敘述 | Google Sheets | ❌ 無需 |
| 新增科目 | Google Sheets | ❌ 無需 |
| 修改篩選條件 | GitHub (app.py) | ✅ 需要 |
| 新增匯出格式 | GitHub (app.py) | ✅ 需要 |
| 改變 UI 介面 | GitHub (app.py) | ✅ 需要 |

---

## 故障排除

### 問題 1：無法連接 Google Sheets

**症狀**：應用顯示「連接失敗」

**解決方案**：
1. 確認試算表已分享為「任何有連結的人都可以檢視」
2. 確認試算表 ID 正確複製
3. 檢查網路連接

### 問題 2：Streamlit Cloud 部署失敗

**症狀**：部署時顯示紅色錯誤

**解決方案**：
1. 檢查 `requirements.txt` 是否包含所有依賴
2. 確認 GitHub 儲存庫是 Public
3. 查看 Streamlit Cloud 的部署日誌

### 問題 3：生成的考卷分數不符

**症狀**：考卷總分超過目標分數

**解決方案**：
- 這是正常的。演算法會盡量接近目標分數，但可能因為題目分數組合而無法完全相符
- 可以修改 `app.py` 中的 `generate_exam` 函數來調整邏輯

---

## 進階自訂

### 新增更多科目

編輯 Google Sheets，在「科目」欄位新增科目名稱即可。

### 修改匯出格式

編輯 `app.py` 中的 `export_to_word` 和 `export_to_pdf` 函數。

### 新增題目難度篩選

在 Google Sheets 新增「難度」欄位，然後在 `app.py` 中新增篩選邏輯。

---

## 總結

你現在已經擁有一個完整的「三層蛋糕」系統：

| 層級 | 維護方式 | 更新頻率 |
|------|--------|--------|
| 📊 **Google Sheets 題庫** | 隨時編輯 | 實時更新 |
| 🧠 **Streamlit 邏輯** | GitHub 管理 | 推送後自動部署 |
| 🌐 **Streamlit Cloud 部署** | 全自動 | 無需手動操作 |

**核心優勢**：題庫和程式完全分離，互不影響。你可以安心地新增題目，而不用擔心破壞程式邏輯。

---

## 聯絡與支援

如有任何問題，請參考 [Streamlit 官方文件](https://docs.streamlit.io) 或 [Google Sheets API 文件](https://developers.google.com/sheets)。

祝你使用愉快！📚✨
