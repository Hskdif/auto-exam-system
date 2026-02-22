"""
使用 Google Gemini Vision API 提取法律題目
支援圖片和 PDF 檔案
"""

import anthropic
import base64
import json
import re
from typing import List, Dict
import PyPDF2
from pdf2image import convert_from_bytes
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

class GeminiLegalExtractor:
    """使用 Gemini Vision API 提取法律題目"""
    
    def __init__(self, api_key: str = None):
        """初始化 Gemini 客戶端"""
        # 使用環境變數中的 API Key
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"  # 使用 Claude 而不是 Gemini（更穩定）
    
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
    
    def extract_with_ai(self, image_bytes: bytes, page_num: int = 1) -> Dict:
        """使用 AI 提取單頁圖片中的題目"""
        try:
            # 將圖片編碼為 Base64
            image_base64 = base64.standard_b64encode(image_bytes).decode("utf-8")
            
            # 構建 AI 提示詞
            prompt = """你是一位法律教授。請仔細分析這張圖片中的法律題目。

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
6. 只返回 JSON，不要其他文字"""
            
            # 調用 Claude API（支援圖片）
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            # 解析 AI 返回的 JSON
            response_text = message.content[0].text
            
            # 嘗試提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                print(f"無法解析 AI 返回的 JSON")
                return {"questions": []}
        
        except Exception as e:
            print(f"AI 提取失敗（第 {page_num} 頁）：{e}")
            return {"questions": []}
    
    def extract_from_pdf(self, pdf_bytes: bytes, filename: str = "") -> List[Dict]:
        """從 PDF 提取所有題目"""
        # 轉換為圖片
        images = self.pdf_to_images(pdf_bytes)
        
        if not images:
            return []
        
        all_questions = []
        
        # 處理每一頁
        for page_num, image_bytes in enumerate(images, 1):
            print(f"處理第 {page_num} 頁...")
            
            # 使用 AI 提取
            result = self.extract_with_ai(image_bytes, page_num)
            
            # 合併結果
            if result and "questions" in result:
                for q in result["questions"]:
                    # 新增頁碼和檔名信息
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


def extract_legal_questions_with_gemini(pdf_bytes: bytes, filename: str = "", api_key: str = None) -> List[Dict]:
    """
    便利函數：使用 Gemini/Claude 提取法律題目
    """
    extractor = GeminiLegalExtractor(api_key=api_key)
    return extractor.extract_from_pdf(pdf_bytes, filename)
