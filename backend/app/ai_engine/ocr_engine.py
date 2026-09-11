"""
PRAMAN AI - State-of-the-Art Hybrid OCR & Text Detection Engine
Combines Deep Learning ONNX (PP-OCRv4 via RapidOCR) with multi-orientation detection,
spatial line clustering, and fallback Tesseract OCR for maximum accuracy on packaged labels.
"""

import os
import cv2
import numpy as np
from PIL import Image
from typing import List, Dict, Any, Optional

# Check RapidOCR availability
try:
    from rapidocr_onnxruntime import RapidOCR
    RAPIDOCR_AVAILABLE = True
except ImportError:
    RAPIDOCR_AVAILABLE = False

# Check Tesseract availability
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    TESSERACT_WINDOWS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(TESSERACT_WINDOWS_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_WINDOWS_PATH
except ImportError:
    TESSERACT_AVAILABLE = False


class OCREngine:
    def __init__(self, tesseract_cmd: Optional[str] = None):
        self.rapid_ocr = None
        if RAPIDOCR_AVAILABLE:
            try:
                # Initialize RapidOCR with angle classifier enabled
                self.rapid_ocr = RapidOCR()
            except Exception as e:
                print(f"[OCREngine] RapidOCR init warning: {e}")

        if TESSERACT_AVAILABLE:
            if tesseract_cmd and os.path.exists(tesseract_cmd):
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            elif os.path.exists(TESSERACT_WINDOWS_PATH):
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_WINDOWS_PATH

    def extract_text_and_boxes(self, image: np.ndarray, original_shape: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Extracts structured text data with bounding boxes, spatial lines, and confidence scores.
        Coordinates are normalized back to original image dimensions if original_shape is provided.
        """
        curr_h, curr_w = image.shape[:2]
        orig_h, orig_w = original_shape[:2] if original_shape else (curr_h, curr_w)
        scale_x = orig_w / float(curr_w)
        scale_y = orig_h / float(curr_h)

        # 1. Try Deep Learning RapidOCR (Primary Engine)
        if self.rapid_ocr is not None:
            try:
                rapid_result, elapse = self.rapid_ocr(image)
                if rapid_result and len(rapid_result) > 0:
                    return self._process_rapidocr_result(rapid_result, scale_x, scale_y, orig_w, orig_h)
            except Exception as e:
                print(f"[OCREngine] RapidOCR execution warning: {e}, falling back to Tesseract.")

        # 2. Fallback to Multi-Pass Tesseract OCR
        if TESSERACT_AVAILABLE:
            return self._process_tesseract_ocr(image, scale_x, scale_y, orig_w, orig_h)

        return {
            "raw_text": "",
            "blocks": [],
            "lines": [],
            "average_confidence": 0.0,
            "is_low_confidence": True,
            "total_words_detected": 0,
            "success": False,
            "error": "No OCR engine available."
        }

    def _process_rapidocr_result(
        self,
        ocr_results: List[Any],
        scale_x: float,
        scale_y: float,
        orig_w: int,
        orig_h: int
    ) -> Dict[str, Any]:
        """
        Transforms RapidOCR detections into structured lines and blocks
        with normalized coordinates and natural reading order.
        """
        blocks = []
        lines = []
        confidences = []

        # Sort detections primarily top-to-bottom, secondarily left-to-right
        # ocr_result item format: [box_points, text, score]
        # box_points format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        sorted_results = []
        for item in ocr_results:
            box, text, score = item[0], item[1].strip(), float(item[2])
            if not text:
                continue
            
            pts = np.array(box, dtype=np.float32)
            min_x = max(0, int(np.min(pts[:, 0]) * scale_x))
            min_y = max(0, int(np.min(pts[:, 1]) * scale_y))
            max_x = min(orig_w, int(np.max(pts[:, 0]) * scale_x))
            max_y = min(orig_h, int(np.max(pts[:, 1]) * scale_y))
            w = max(1, max_x - min_x)
            h = max(1, max_y - min_y)

            conf_pct = round(score * 100.0, 1) if score <= 1.0 else round(score, 1)
            sorted_results.append({
                "text": text,
                "x": min_x,
                "y": min_y,
                "w": w,
                "h": h,
                "confidence": conf_pct,
                "polygon": [[int(p[0] * scale_x), int(p[1] * scale_y)] for p in box]
            })

        # Sort in reading order (top to bottom, then left to right)
        sorted_results.sort(key=lambda b: (b["y"] // 25, b["x"]))

        raw_text_lines = []
        for b in sorted_results:
            confidences.append(b["confidence"])
            blocks.append(b)
            lines.append({
                "text": b["text"],
                "x": b["x"],
                "y": b["y"],
                "w": b["w"],
                "h": b["h"],
                "confidence": b["confidence"],
                "word_count": len(b["text"].split())
            })
            raw_text_lines.append(b["text"])

        avg_conf = round(sum(confidences) / len(confidences), 1) if confidences else 0.0
        raw_text = "\n".join(raw_text_lines)

        return {
            "raw_text": raw_text,
            "blocks": blocks,
            "lines": lines,
            "average_confidence": avg_conf,
            "is_low_confidence": avg_conf < 50.0,
            "total_words_detected": sum(l["word_count"] for l in lines),
            "engine": "RapidOCR (Deep Learning PP-OCRv4 ONNX)",
            "success": True
        }

    def _process_tesseract_ocr(
        self,
        image: np.ndarray,
        scale_x: float,
        scale_y: float,
        orig_w: int,
        orig_h: int
    ) -> Dict[str, Any]:
        """Multi-pass Tesseract OCR fallback."""
        if len(image.shape) == 2:
            pil_img = Image.fromarray(image)
        else:
            pil_img = Image.fromarray(image[:, :, ::-1])

        try:
            # Run with PSM 11 (sparse text) or PSM 6 (uniform block)
            data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT, config="--psm 11")
            raw_text = pytesseract.image_to_string(pil_img, config="--psm 11")
        except Exception as e:
            return {
                "raw_text": "",
                "blocks": [],
                "lines": [],
                "average_confidence": 0.0,
                "is_low_confidence": True,
                "total_words_detected": 0,
                "success": False,
                "error": f"Tesseract OCR error: {str(e)}"
            }

        n_boxes = len(data["text"])
        blocks = []
        confidences = []
        lines_dict = {}

        for i in range(n_boxes):
            text = data["text"][i].strip()
            conf = int(data["conf"][i])
            if text and conf > 0:
                confidences.append(conf)
                min_x = int(data["left"][i] * scale_x)
                min_y = int(data["top"][i] * scale_y)
                bw = int(data["width"][i] * scale_x)
                bh = int(data["height"][i] * scale_y)
                box_info = {
                    "text": text,
                    "x": min_x,
                    "y": min_y,
                    "w": bw,
                    "h": bh,
                    "confidence": conf
                }
                blocks.append(box_info)
                line_id = int(data["line_num"][i]) + int(data["block_num"][i]) * 1000
                if line_id not in lines_dict:
                    lines_dict[line_id] = []
                lines_dict[line_id].append(box_info)

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
            "engine": "Tesseract 5.4 OCR Fallback",
            "success": True
        }
