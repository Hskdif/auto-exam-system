"""
使用 Claude API 直接從 PDF 文字提取法律題目
不需要轉換為圖片，更適合 Streamlit Cloud
"""

import anthropic
import json
import re
from typing import List, Dict
import PyPDF2
import io

class ClaudeTextExtractor:
    """使用 Claude 從 PDF 文字提取法律題目"""
    
    def __init__(self, api_key: str = None):
        """初始化 Claude 客戶端"""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """從 PDF 提取所有文字"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- 第 {page_num} 頁 ---\n{page_text}"
            
            return text
        except Exception as e:
            print(f"PDF 文字提取失敗：{e}")
            return ""
    
    def extract_with_claude(self, text: str) -> List[Dict]:
        """使用 Claude 分析文字並提取題目"""
        try:
            # 構建提示詞
            prompt = f"""你是一位法律教授。請仔細分析以下 PDF 文字內容中的所有法律題目。

【PDF 內容】
{text}

【任務】
請提取所有的法律題目、案例和解答。對於每個題目，請以 JSON 格式返回：

{{
    "questions": [
        {{
            "question_text": "完整的題目內容（一字不漏保留原文）",
            "answer_text": "完整的解答內容（如果有的話，一字不漏保留原文）",
            "subject": "科目（民法/刑法/民訴/刑訴/行政法/商法/智財法/勞動法/環保法/稅法）",
            "type": "題型（申論題/案例題/選擇題）",
            "difficulty": "難度（簡單/中等/困難）",
            "score": "分數（如果有的話）"
        }}
    ]
}}

【重要提示】
1. 完整保留原文，一字不漏，不要竄改、簡化或重新組織
2. 如果有案例說明，請完整保留案例內容
3. 如果有解答，請完整保留解答內容
4. 自動判斷科目（根據題目內容）
5. 自動判斷題型
6. 只返回 JSON，不要其他文字
7. 如果找不到題目，返回空的 questions 陣列"""
            
            # 調用 Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            
            # 解析返回的 JSON
            response_text = message.content[0].text
            
            # 嘗試提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("questions", [])
            else:
                print(f"無法解析 Claude 返回的 JSON")
                return []
        
        except Exception as e:
            print(f"Claude 提取失敗：{e}")
            return []
    
    def extract_from_pdf(self, pdf_bytes: bytes, filename: str = "") -> List[Dict]:
        """從 PDF 提取所有題目"""
        # 步驟 1：提取文字
        text = self.extract_text_from_pdf(pdf_bytes)
        
        if not text or len(text.strip()) < 100:
            print("❌ 無法從 PDF 提取足夠的文字")
            return []
        
        print(f"✅ 已提取 {len(text)} 個字元的文字")
        
        # 步驟 2：使用 Claude 分析
        questions = self.extract_with_claude(text)
        
        # 步驟 3：格式化結果
        formatted_questions = []
        
        for idx, q in enumerate(questions, 1):
            # 從檔名提取日期和題號
            date_match = re.search(r'(\d{1,2})月(\d{1,2})[號日]', filename)
            question_num_match = re.search(r'第(\d+)題', filename)
            
            month = date_match.group(1) if date_match else ""
            day = date_match.group(2) if date_match else ""
            file_question_num = question_num_match.group(1) if question_num_match else str(idx)
            
            # 生成 ID
            if month and day:
                question_id = f"{month}月{day}號_第{file_question_num}題"
            else:
                question_id = f"{idx:03d}"
            
            # 計算分數
            score = q.get('score', '')
            if not score:
                difficulty = q.get('difficulty', '中等')
                difficulty_map = {'簡單': 25, '中等': 50, '困難': 100}
                score = difficulty_map.get(difficulty, 50)
            
            formatted_questions.append({
                'ID': question_id,
                '類型': q.get('type', '申論題'),
                '科目': q.get('subject', '法律'),
                '題目內容': q.get('question_text', ''),
                '參考解答': q.get('answer_text', '待補充'),
                '分數': score
            })
        
        return formatted_questions


def extract_legal_questions_from_text(pdf_bytes: bytes, filename: str = "", api_key: str = None) -> List[Dict]:
    """
    便利函數：使用 Claude 從 PDF 文字提取法律題目
    """
    extractor = ClaudeTextExtractor(api_key=api_key)
    return extractor.extract_from_pdf(pdf_bytes, filename)
