import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import re
import os

# 嘗試導入 PDF 處理庫
try:
    import PyPDF2
    from claude_extractor import extract_legal_questions_from_text
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ==================== 頁面設定 ====================
st.set_page_config(
    page_title="自動化出卷系統",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 自動化雲端出卷系統")
st.markdown("基於 Google Sheets 的智能出卷平台 | 支援 PDF 自動提取")

# ==================== 初始化 Session State ====================
if 'exam_df' not in st.session_state:
    st.session_state.exam_df = None

if 'extracted_questions' not in st.session_state:
    st.session_state.extracted_questions = []

# ==================== Google Sheets 函數 ====================
def load_google_sheets(sheet_id):
    """從 Google Sheets 載入題庫"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)
        
        # 驗證必要欄位
        required_columns = ['ID', '類型', '科目', '題目內容', '參考解答', '分數']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ 試算表缺少必要欄位。需要：{', '.join(required_columns)}")
            return None
        
        return df
    except Exception as e:
        st.error(f"❌ 錯誤：{str(e)}")
        return None

# ==================== PDF 處理函數 ====================
def extract_legal_questions_from_pdf(pdf_file):
    """使用 Claude AI 從 PDF 文字提取法律題目"""
    if not PDF_AVAILABLE:
        st.error("❌ PDF 處理庫未安裝")
        return []
    
    try:
        # 讀取 PDF 檔案
        pdf_bytes = pdf_file.read()
        filename = pdf_file.name
        
        # 使用 Claude AI 提取
        questions = extract_legal_questions_from_text(pdf_bytes, filename)
        
        return questions
    except Exception as e:
        st.error(f"❌ PDF 提取失敗：{str(e)}")
        return []

# ==================== 核心邏輯 ====================
def generate_exam(df, target_score, selected_subjects, selected_types):
    """根據條件生成考卷"""
    if df is None or df.empty:
        return None
    
    # 篩選題目
    filtered_df = df[
        (df['科目'].isin(selected_subjects)) &
        (df['類型'].isin(selected_types))
    ].copy()
    
    if filtered_df.empty:
        return None
    
    # 隨機抽取題目
    exam_questions = []
    current_score = 0
    
    for _, row in filtered_df.iterrows():
        if current_score + row['分數'] <= target_score:
            exam_questions.append(row)
            current_score += row['分數']
    
    if not exam_questions:
        return None
    
    return pd.DataFrame(exam_questions)

# ==================== 主要介面 ====================
tab1, tab2, tab3 = st.tabs(["📝 出卷系統", "📥 上傳 PDF", "📊 題庫管理"])

# ==================== Tab 1: 出卷系統 ====================
with tab1:
    st.subheader("📝 出卷系統")
    
    col_input, col_load = st.columns([3, 1])
    
    with col_input:
        sheet_id = st.text_input(
            "請輸入 Google Sheets ID",
            placeholder="例如：1a2b3c4d5e6f7g8h9i0j",
            key="sheet_id_main"
        )
    
    with col_load:
        if st.button("📖 載入題庫", use_container_width=True):
            st.cache_data.clear()
    
    if sheet_id:
        df = load_google_sheets(sheet_id)
        
        if df is not None and not df.empty:
            st.success(f"✅ 成功載入 {len(df)} 題")
            st.session_state.exam_df = df
            
            # 顯示統計
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("總題數", len(df))
            with col2:
                st.metric("科目數", df['科目'].nunique())
            with col3:
                st.metric("題型數", df['類型'].nunique())
            with col4:
                st.metric("總分數", int(df['分數'].sum()))
            
            st.markdown("---")
            
            # 篩選條件
            col_subject, col_type, col_score = st.columns(3)
            
            with col_subject:
                selected_subjects = st.multiselect(
                    "選擇科目",
                    df['科目'].unique(),
                    default=list(df['科目'].unique())
                )
            
            with col_type:
                selected_types = st.multiselect(
                    "選擇題型",
                    df['類型'].unique(),
                    default=list(df['類型'].unique())
                )
            
            with col_score:
                target_score = st.number_input(
                    "目標分數",
                    min_value=0,
                    max_value=int(df['分數'].sum()),
                    value=100,
                    step=5
                )
            
            # 生成考卷
            if st.button("🎲 隨機生成考卷", use_container_width=True):
                exam = generate_exam(df, target_score, selected_subjects, selected_types)
                
                if exam is not None:
                    st.session_state.exam_df = exam
                    st.success(f"✅ 成功生成考卷（{len(exam)} 題，{int(exam['分數'].sum())} 分）")
                    
                    # 顯示考卷
                    st.subheader("📋 考卷預覽")
                    
                    for i, (_, row) in enumerate(exam.iterrows(), 1):
                        with st.expander(f"**題 {i}** ({row['科目']} | {row['類型']}) - {row['分數']} 分"):
                            st.write(f"**題目：**\n{row['題目內容']}")
                            st.write(f"**解答：**\n{row['參考解答']}")
                    
                    st.markdown("---")
                    st.subheader("💾 匯出考卷")
                    
                    col_export1, col_export2 = st.columns(2)
                    
                    with col_export1:
                        if st.button("📥 下載為 CSV", use_container_width=True):
                            csv_bytes = exam.to_csv(index=False).encode('utf-8-sig')
                            st.download_button(
                                label="點擊下載 CSV",
                                data=csv_bytes,
                                file_name=f"考卷_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                else:
                    st.warning("⚠️ 無法生成符合條件的考卷")

# ==================== Tab 2: 上傳 PDF ====================
with tab2:
    st.subheader("📥 上傳 PDF 並自動提取題目")
    
    if not PDF_AVAILABLE:
        st.warning("⚠️ 系統未安裝 PDF 處理庫")
    else:
        st.info("📌 說明：上傳 PDF 檔案，系統會自動提取題目內容。")
        
        uploaded_files = st.file_uploader(
            "選擇 PDF 檔案",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.subheader(f"📄 已上傳 {len(uploaded_files)} 個檔案")
            
            # 建立一個按鈕來開始分析
            if st.button("🤖 開始分析 PDF", use_container_width=True, key="analyze_pdfs"):
                st.session_state.extracted_questions = []
                
                # 創建進度條
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 一次處理所有 PDF
                for idx, uploaded_file in enumerate(uploaded_files):
                    # 更新進度
                    progress = (idx + 1) / len(uploaded_files)
                    progress_bar.progress(progress)
                    status_text.write(f"📄 正在分析: {uploaded_file.name} ({idx + 1}/{len(uploaded_files)})")
                    
                    # 提取題目
                    questions = extract_legal_questions_from_pdf(uploaded_file)
                    
                    if questions:
                        st.session_state.extracted_questions.extend(questions)
                
                # 清除進度條
                progress_bar.empty()
                status_text.empty()
                
                # 顯示完成訊息
                if st.session_state.extracted_questions:
                    st.success(f"✅ 成功提取 {len(st.session_state.extracted_questions)} 題")
                else:
                    st.warning("⚠️ 未找到任何題目。請確保 PDF 中有法律題目。")
            
            # 顯示已提取的題目
            if st.session_state.extracted_questions:
                st.markdown("---")
                st.subheader("📋 提取的題目詳情")
                
                # 顯示每個題目
                for i, q in enumerate(st.session_state.extracted_questions, 1):
                    with st.expander(f"**題 {i}** ({q['科目']} | {q['類型']}) - {q['ID']}"):
                        st.write("**題目內容：**")
                        st.write(q['題目內容'])
                        
                        if q['參考解答'] and q['參考解答'] != '待補充':
                            st.write("**參考解答：**")
                            st.write(q['參考解答'])
                        
                        st.write(f"**分數：** {q['分數']}")
                
                st.markdown("---")
                st.subheader("💾 匯出提取的題目")
                
                # 轉換為 CSV
                df_extracted = pd.DataFrame(st.session_state.extracted_questions)
                csv_bytes = df_extracted.to_csv(index=False).encode('utf-8-sig')
                
                st.download_button(
                    label="📥 下載提取的題目（CSV）",
                    data=csv_bytes,
                    file_name=f"提取題目_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                st.info("💡 提示：下載 CSV 後，可以在 Google Sheets 中匯入這些題目。")

# ==================== Tab 3: 題庫管理 ====================
with tab3:
    st.subheader("📊 題庫管理")
    
    st.info("💡 在這個頁面，你可以查看和管理你的題庫。")
    
    # 輸入 Google Sheets ID
    sheet_id_mgmt = st.text_input(
        "請輸入 Google Sheets ID",
        placeholder="例如：1a2b3c4d5e6f7g8h9i0j",
        key="sheet_id_mgmt"
    )
    
    if sheet_id_mgmt:
        if st.button("📖 載入題庫", use_container_width=True):
            st.cache_data.clear()
        
        df_mgmt = load_google_sheets(sheet_id_mgmt)
        
        if df_mgmt is not None and not df_mgmt.empty:
            st.success(f"✅ 成功載入 {len(df_mgmt)} 題")
            
            # 顯示統計
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("總題數", len(df_mgmt))
            with col2:
                st.metric("科目數", df_mgmt['科目'].nunique())
            with col3:
                st.metric("題型數", df_mgmt['類型'].nunique())
            with col4:
                st.metric("總分數", int(df_mgmt['分數'].sum()))
            
            st.markdown("---")
            
            # 顯示題庫內容
            st.subheader("📚 題庫內容")
            
            # 科目分佈
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.write("**科目分佈**")
                subject_counts = df_mgmt['科目'].value_counts()
                st.bar_chart(subject_counts)
            
            with col_chart2:
                st.write("**題型分佈**")
                type_counts = df_mgmt['類型'].value_counts()
                st.bar_chart(type_counts)
            
            st.markdown("---")
            
            # 顯示完整題庫表格
            st.subheader("📋 完整題庫")
            st.dataframe(df_mgmt, use_container_width=True)

# ==================== 頁尾 ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    自動化雲端出卷系統 v1.0 | 基於 Streamlit + Google Sheets
</div>
""", unsafe_allow_html=True)
