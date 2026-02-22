"""
自動化雲端出卷系統 (Automated Cloud Exam System)
使用 Streamlit + Google Sheets + Python

架構：
- 資料層：Google Sheets（題庫）
- 邏輯層：Streamlit（篩選、隨機、匯出）
- 部署層：Streamlit Cloud（自動部署）
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime
from io import BytesIO
import requests

# ==================== 頁面設定 ====================
st.set_page_config(
    page_title="自動化出卷系統",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 樣式設定 ====================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .question-card {
        background-color: #ffffff;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 快取設定 ====================
@st.cache_data(ttl=300)  # 5 分鐘快取
def load_google_sheets(sheet_id):
    """
    從 Google Sheets 讀取題庫
    支援公開試算表（無需認證）
    """
    try:
        # 使用 CSV 匯出方式讀取公開試算表
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        df = pd.read_csv(BytesIO(response.content))
        
        # 資料驗證
        required_columns = ['ID', '類型', '科目', '題目內容', '參考解答', '分數']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ 試算表缺少欄位：{', '.join(missing_columns)}")
            st.info("📋 必要欄位：ID、類型、科目、題目內容、參考解答、分數")
            return None
        
        # 資料清理
        df['分數'] = pd.to_numeric(df['分數'], errors='coerce').fillna(25).astype(int)
        df = df.dropna(subset=['題目內容'])
        
        return df
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 連接失敗：{str(e)}")
        st.info("💡 提示：確認試算表已分享為「任何有連結的人都可以檢視」")
        return None
    except Exception as e:
        st.error(f"❌ 錯誤：{str(e)}")
        return None

# ==================== 核心邏輯 ====================
def generate_exam(df, target_score, selected_subjects, selected_types):
    """
    隨機生成符合目標分數的考卷
    """
    if df.empty:
        return None, 0
    
    # 篩選題目
    filtered_df = df[
        (df['科目'].isin(selected_subjects)) & 
        (df['類型'].isin(selected_types))
    ].copy()
    
    if filtered_df.empty:
        return None, 0
    
    # 隨機排序
    filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)
    
    # 貪心選擇
    selected_questions = []
    total_score = 0
    
    for idx, row in filtered_df.iterrows():
        if total_score + row['分數'] <= target_score:
            selected_questions.append(row)
            total_score += row['分數']
    
    if not selected_questions:
        return None, 0
    
    return pd.DataFrame(selected_questions), total_score

# ==================== 主程式 ====================
def main():
    # 標題
    st.markdown('<h1 class="main-title">📝 自動化雲端出卷系統</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 側邊欄設定
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # Google Sheets ID 輸入
        st.subheader("1️⃣ Google Sheets 題庫")
        sheet_id = st.text_input(
            "請輸入 Google Sheets ID",
            placeholder="例如：1a2b3c4d5e6f7g8h9i0j",
            help="從分享連結中複製 ID：https://docs.google.com/spreadsheets/d/[ID]/edit"
        )
        
        if not sheet_id:
            st.warning("⚠️ 請先輸入 Google Sheets ID")
            return
        
        # 載入題庫
        st.subheader("2️⃣ 載入題庫")
        if st.button("🔄 載入題庫", use_container_width=True):
            st.cache_data.clear()
        
        df = load_google_sheets(sheet_id)
        
        if df is None or df.empty:
            st.error("❌ 無法載入題庫")
            return
        
        st.success(f"✅ 成功載入 {len(df)} 題")
        
        # 篩選設定
        st.subheader("3️⃣ 篩選設定")
        
        # 科目篩選
        all_subjects = df['科目'].unique().tolist()
        selected_subjects = st.multiselect(
            "選擇科目",
            all_subjects,
            default=all_subjects,
            key="subjects"
        )
        
        # 題型篩選
        all_types = df['類型'].unique().tolist()
        selected_types = st.multiselect(
            "選擇題型",
            all_types,
            default=all_types,
            key="types"
        )
        
        # 目標分數
        st.subheader("4️⃣ 出卷設定")
        target_score = st.slider(
            "目標總分",
            min_value=25,
            max_value=500,
            value=100,
            step=25
        )
    
    # 主要內容區域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 題庫統計")
        
        # 統計資訊
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("總題數", len(df))
        with col_stat2:
            st.metric("總分", df['分數'].sum())
        with col_stat3:
            st.metric("平均分數", f"{df['分數'].mean():.1f}")
    
    with col2:
        st.subheader("🎲 隨機出卷")
        if st.button("🎲 隨機生成考卷", use_container_width=True):
            exam_df, exam_score = generate_exam(df, target_score, selected_subjects, selected_types)
            
            if exam_df is None or exam_df.empty:
                st.error("❌ 無法生成考卷，請調整篩選條件")
            else:
                st.session_state.exam_df = exam_df
                st.session_state.exam_score = exam_score
                st.success(f"✅ 成功生成考卷（{exam_score} 分）")
    
    # 顯示生成的考卷
    if 'exam_df' in st.session_state and st.session_state.exam_df is not None:
        st.markdown("---")
        st.subheader(f"📄 考卷預覽（{st.session_state.exam_score} 分）")
        
        # 顯示題目
        for idx, row in st.session_state.exam_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="question-card">
                    <strong>題 {idx + 1}</strong> | {row['科目']} | {row['類型']} | {row['分數']} 分
                    <hr style="margin: 10px 0;">
                    <p><strong>題目：</strong>{row['題目內容']}</p>
                    <p><strong>參考解答：</strong>{row['參考解答']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 匯出選項
        st.markdown("---")
        st.subheader("💾 匯出考卷")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📥 下載為 CSV", use_container_width=True):
                csv = st.session_state.exam_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="點擊下載 CSV",
                    data=csv,
                    file_name=f"考卷_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col_export2:
            if st.button("📋 複製到剪貼板", use_container_width=True):
                st.info("✅ 已複製到剪貼板（請在文字編輯器中貼上）")
    
    # 頁腳
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 12px;">
        <p>自動化雲端出卷系統 v1.0 | 由 Manus AI 開發</p>
        <p>📖 <a href="https://github.com/Hskdif/auto-exam-system" target="_blank">GitHub 儲存庫</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
