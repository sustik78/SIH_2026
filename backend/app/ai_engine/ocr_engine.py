"""
PRAMAN AI - OCR & Text Detection Engine
Uses Tesseract OCR with Bounding Box detection and confidence estimation.
"""

import os
import pytesseract
from PIL import Image
import numpy as np
from typing import List, Dict, Any, Optional

# Set Tesseract executable path if standard Windows path exists
TESSERACT_WINDOWS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_WINDOWS_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_WINDOWS_PATH

class OCREngine:
    def __init__(self, tesseract_cmd: Optional[str] = None):
        if tesseract_cmd and os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        elif os.path.exists(TESSERACT_WINDOWS_PATH):
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_WINDOWS_PATH

    def extract_text_and_boxes(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extracts structured text data with bounding boxes and confidence scores.
        """
        # Convert numpy array to PIL Image
        if len(image.shape) == 2:
            pil_img = Image.fromarray(image)
        else:
            pil_img = Image.fromarray(image[:, :, ::-1])  # BGR to RGB

        try:
            # Get detailed OCR data
            data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
            raw_text = pytesseract.image_to_string(pil_img)
        except Exception as e:
            # Fallback in case of Tesseract error
            return {
                "raw_text": "",
                "blocks": [],
                "lines": [],
                "average_confidence": 0.0,
                "error": f"OCR Engine Error: {str(e)}",
                "success": False
            }

        n_boxes = len(data["text"])
        blocks = []
        confidences = []
        
        # Group words by line
        lines_dict: Dict[int, List[Dict[str, Any]]] = {}

        for i in range(n_boxes):
            text = data["text"][i].strip()
            conf = int(data["conf"][i])
            if text and conf > 0:
                confidences.append(conf)
                box_info = {
                    "text": text,
                    "x": int(data["left"][i]),
                    "y": int(data["top"][i]),
                    "w": int(data["width"][i]),
                    "h": int(data["height"][i]),
                    "confidence": conf,
                    "line_num": int(data["line_num"][i]),
                    "block_num": int(data["block_num"][i])
                }
                blocks.append(box_info)
                
                line_id = int(data["line_num"][i]) + int(data["block_num"][i]) * 1000
                if line_id not in lines_dict:
                    lines_dict[line_id] = []
                lines_dict[line_id].append(box_info)

        # Aggregate lines with merged bounding boxes
        aggregated_lines = []
        for line_id, words in lines_dict.items():
            if not words:
                continue
            line_text = " ".join([w["text"] for w in words])
            min_x = min(w["x"] for w in words)
            min_y = min(w["y"] for w in words)
            max_x = max(w["x"] + w["w"] for w in words)
            max_y = max(w["y"] + w["h"] for w in words)
            avg_conf = sum(w["confidence"] for w in words) / len(words)
            
            aggregated_lines.append({
                "text": line_text,
                "x": min_x,
                "y": min_y,
                "w": max_x - min_x,
                "h": max_y - min_y,
                "confidence": round(avg_conf, 1),
                "word_count": len(words)
            })

        avg_confidence = round(sum(confidences) / len(confidences), 1) if confidences else 0.0

        return {
            "raw_text": raw_text.strip(),
            "blocks": blocks,
            "lines": aggregated_lines,
            "average_confidence": avg_confidence,
            "is_low_confidence": avg_confidence < 50.0,
            "total_words_detected": len(blocks),
            "success": True
        }
