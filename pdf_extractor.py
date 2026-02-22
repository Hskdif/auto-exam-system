"""
法律題目 PDF 提取模組
使用 OCR 和智能解析提取法律題目、案例、解答
"""

import re
from typing import List, Dict, Tuple
import PyPDF2
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io

# 法律科目關鍵詞
LEGAL_SUBJECTS = {
    '民法': ['民法', '物權', '債權', '親屬', '繼承', '契約', '買賣', '租賃', '抵押', '質權'],
    '刑法': ['刑法', '犯罪', '故意', '過失', '搶劫', '竊盜', '詐欺', '傷害', '殺人', '強制'],
    '民訴': ['民訴', '民事訴訟', '管轄', '訴訟', '上訴', '再審', '和解', '調解', '證據', '舉證'],
    '刑訴': ['刑訴', '刑事訴訟', '偵查', '起訴', '審判', '證人', '被告', '檢察官', '法官'],
    '行政法': ['行政法', '行政處分', '行政程序', '行政救濟', '訴願', '行政訴訟', '公務員'],
    '商法': ['商法', '公司', '股份', '董事', '監察', '商人', '商業帳簿', '票據', '支票'],
    '智財法': ['智慧財產', '著作權', '專利', '商標', '營業秘密', '積體電路'],
    '勞動法': ['勞動法', '勞工', '雇主', '薪資', '工時', '休假', '工會', '爭議'],
    '環保法': ['環保', '環境', '污染', '廢棄物', '空氣', '水質', '環評'],
    '稅法': ['稅法', '所得稅', '營業稅', '關稅', '遺產稅', '贈與稅'],
}

# 題目和答案的分隔符號
QUESTION_SEPARATORS = [
    r'(?:^|\n)(?:【|＜|<)?(?:題目|問題|案例|例題)(?:】|＞|>)?[\s]*(?::|：)',
    r'(?:^|\n)(?:第\s*[一二三四五六七八九十\d]+\s*題)',
    r'(?:^|\n)(?:Q\d+|q\d+)',
]

ANSWER_SEPARATORS = [
    r'(?:^|\n)(?:【|＜|<)?(?:答案|解答|參考解答|說明)(?:】|＞|>)?[\s]*(?::|：)',
    r'(?:^|\n)(?:【|＜|<)?(?:解|答)(?:】|＞|>)?[\s]*(?::|：)',
]

class LegalPDFExtractor:
    """法律題目 PDF 提取器"""
    
    def __init__(self):
        self.subjects = LEGAL_SUBJECTS
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        從 PDF 提取文字
        優先使用 PyPDF2（快速），失敗則使用 OCR（準確）
        """
        text = ""
        
        # 方法 1：使用 PyPDF2（快速）
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # 如果提取成功且內容充足，直接返回
            if len(text.strip()) > 50:
                return text
        except Exception as e:
            print(f"PyPDF2 提取失敗：{e}")
        
        # 方法 2：使用 OCR（準確但較慢）
        try:
            images = convert_from_bytes(pdf_bytes)
            for image in images:
                text += pytesseract.image_to_string(image, lang='chi_tra') + "\n"
            return text
        except Exception as e:
            print(f"OCR 提取失敗：{e}")
            return ""
    
    def identify_subject(self, text: str) -> str:
        """
        自動識別法律科目
        """
        text_lower = text.lower()
        
        # 計算每個科目的關鍵詞匹配數
        subject_scores = {}
        
        for subject, keywords in self.subjects.items():
            score = 0
            for keyword in keywords:
                # 計算關鍵詞出現次數
                score += text.count(keyword)
            subject_scores[subject] = score
        
        # 返回分數最高的科目
        if subject_scores:
            best_subject = max(subject_scores, key=subject_scores.get)
            if subject_scores[best_subject] > 0:
                return best_subject
        
        return "法律"  # 預設科目
    
    def split_questions_and_answers(self, text: str) -> List[Tuple[str, str]]:
        """
        將文字分割為題目和答案對
        """
        # 移除多餘的空行
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        
        # 尋找題目和答案的邊界
        qa_pairs = []
        
        # 按照常見的題目分隔符分割
        questions = re.split(
            r'(?:^|\n)(?:【|＜|<)?(?:題目|問題|案例|例題|第\s*[一二三四五六七八九十\d]+\s*題|Q\d+)(?:】|＞|>)?[\s]*(?::|：)',
            text,
            flags=re.MULTILINE
        )
        
        # 處理每個題目
        for i, question_block in enumerate(questions[1:]):  # 跳過第一個空塊
            # 分割題目和答案
            answer_match = re.search(
                r'(?:【|＜|<)?(?:答案|解答|參考解答|說明|解|答)(?:】|＞|>)?[\s]*(?::|：)',
                question_block,
                flags=re.IGNORECASE
            )
            
            if answer_match:
                question = question_block[:answer_match.start()].strip()
                answer = question_block[answer_match.end():].strip()
            else:
                question = question_block.strip()
                answer = ""
            
            if question:  # 只保留有題目的項目
                qa_pairs.append((question, answer))
        
        return qa_pairs
    
    def extract_questions(self, pdf_bytes: bytes, filename: str = "") -> List[Dict]:
        """
        完整的題目提取流程
        """
        # 步驟 1：提取文字
        text = self.extract_text_from_pdf(pdf_bytes)
        
        if not text or len(text.strip()) < 50:
            return []
        
        # 步驟 2：識別科目
        subject = self.identify_subject(text)
        
        # 步驟 3：分割題目和答案
        qa_pairs = self.split_questions_and_answers(text)
        
        # 步驟 4：構建題目物件
        questions = []
        
        for idx, (question, answer) in enumerate(qa_pairs, 1):
            # 從檔名提取日期和題號
            date_match = re.search(r'(\d{1,2})月(\d{1,2})[號日]', filename)
            question_num_match = re.search(r'第(\d+)題', filename)
            
            month = date_match.group(1) if date_match else "未知"
            day = date_match.group(2) if date_match else "未知"
            file_question_num = question_num_match.group(1) if question_num_match else str(idx)
            
            # 決定題型（根據內容長度和特徵）
            if len(question) > 200 or '案例' in question or '情況' in question:
                question_type = '案例題'
            else:
                question_type = '申論題'
            
            # 計算分數（根據內容長度）
            score = min(50, 25 + (len(question) // 50) * 5)
            
            questions.append({
                'ID': f"{month}月{day}號_第{file_question_num}題",
                '類型': question_type,
                '科目': subject,
                '題目內容': question,
                '參考解答': answer if answer else '待補充',
                '分數': score
            })
        
        return questions


def extract_legal_questions(pdf_bytes: bytes, filename: str = "") -> List[Dict]:
    """
    便利函數：提取法律題目
    """
    extractor = LegalPDFExtractor()
    return extractor.extract_questions(pdf_bytes, filename)
