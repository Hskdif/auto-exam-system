"""
使用 Google Gemini Vision API 提取法律題目
支援掃描 PDF 和複雜版面
"""

import google.generativeai as genai
import json
import re
from typing import List, Dict
import PyPDF2
from pdf2image import convert_from_bytes
import io
import os

class GeminiPDFExtractor:
    """使用 Google Gemini Vision API 提取法律題目"""
    
    def __init__(self, api_key: str = None):
        """初始化 Gemini 客戶端"""
        # 使用環境變數中的 API Key
        if api_key is None:
            api_key = os.environ.get('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("Gemini API Key 未設定。請設定 GEMINI_API_KEY 環境變數。")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def pdf_to_images(self, pdf_bytes: bytes) -> List[bytes]:
        """將 PDF 轉換為圖片"""
        try:
            images = convert_from_bytes(pdf_bytes, dpi=200)
            image_bytes_list = []
            
            for image in images:
                # 轉換為 JPEG 以減小檔案大小
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=95)
                image_bytes_list.append(img_byte_arr.getvalue())
            
            return image_bytes_list
        except Exception as e:
            print(f"PDF 轉換失敗：{e}")
            return []
    
    def extract_with_gemini(self, image_bytes: bytes, page_num: int = 1) -> List[Dict]:
        """使用 Gemini Vision 提取單頁圖片中的題目"""
        try:
            # 將圖片轉換為 PIL Image
            from PIL import Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # 構建提示詞
            prompt = """你是一位法律教授。請仔細分析這張圖片中的所有法律題目。

請以 JSON 格式返回提取的所有題目，格式如下：
{
    "questions": [
        {
            "question_text": "完整的題目內容（一字不漏）",
            "answer_text": "完整的解答內容（如果有的話，一字不漏）",
            "subject": "科目（民法/刑法/民訴/刑訴/行政法/商法/智財法/勞動法/環保法/稅法）",
            "type": "題型（申論題/案例題/選擇題）",
            "difficulty": "難度（簡單/中等/困難）"
        }
    ]
}

重要提示：
1. 完整保留原文，一字不漏，不要竄改
2. 如果有案例，請完整保留案例內容
3. 如果有解答，請完整保留解答內容
4. 自動判斷科目（根據題目內容）
5. 自動判斷題型
6. 只返回 JSON，不要其他文字
7. 如果找不到題目，返回空的 questions 陣列"""
            
            # 調用 Gemini API
            response = self.model.generate_content([prompt, image])
            response_text = response.text
            
            # 嘗試提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("questions", [])
            else:
                print(f"無法解析 Gemini 返回的 JSON（第 {page_num} 頁）")
                return []
        
        except Exception as e:
            print(f"Gemini 提取失敗（第 {page_num} 頁）：{e}")
            return []
    
    def extract_from_pdf(self, pdf_bytes: bytes, filename: str = "") -> List[Dict]:
        """從 PDF 提取所有題目"""
        # 轉換為圖片
        images = self.pdf_to_images(pdf_bytes)
        
        if not images:
            print("❌ 無法轉換 PDF 為圖片")
            return []
        
        all_questions = []
        
        # 處理每一頁
        for page_num, image_bytes in enumerate(images, 1):
            print(f"正在處理第 {page_num} 頁...")
            
            # 使用 Gemini 提取
            questions = self.extract_with_gemini(image_bytes, page_num)
            
            # 合併結果
            if questions:
                for q in questions:
                    q["page"] = page_num
                    q["source_file"] = filename
                    all_questions.append(q)
        
        # 轉換為標準格式
        formatted_questions = []
        for idx, q in enumerate(all_questions, 1):
            formatted_questions.append({
                'ID': f"{idx:03d}",
                '類型': q.get('type', '申論題'),
                '科目': q.get('subject', '法律'),
                '題目內容': q.get('question_text', ''),
                '參考解答': q.get('answer_text', '待補充'),
                '分數': self._calculate_score(q.get('difficulty', '中等'))
            })
        
        return formatted_questions
    
    def _calculate_score(self, difficulty: str) -> int:
        """根據難度計算分數"""
        difficulty_map = {
            '簡單': 25,
            '中等': 50,
            '困難': 100,
        }
        return difficulty_map.get(difficulty, 50)


def extract_legal_questions_with_gemini_vision(pdf_bytes: bytes, filename: str = "", api_key: str = None) -> List[Dict]:
    """
    便利函數：使用 Gemini Vision 提取法律題目
    """
    try:
        extractor = GeminiPDFExtractor(api_key=api_key)
        return extractor.extract_from_pdf(pdf_bytes, filename)
    except Exception as e:
        print(f"Gemini 初始化失敗：{e}")
        return []
