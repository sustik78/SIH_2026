"""
PRAMAN AI - Advanced Image Preprocessing Module
Optimized for packaged commodity labels with multi-scale enhancement,
glare suppression, orientation correction, and adaptive contrast tuning.
"""

import cv2
import numpy as np
import os
from typing import Tuple, Dict, Any, Optional

class ImagePreprocessor:
    @staticmethod
    def load_image(image_path: str) -> np.ndarray:
        """Loads image handling unicode paths and EXIF auto-rotation."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        image_bytes = np.fromfile(image_path, dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Failed to decode image from path: {image_path}")
        return image

    @staticmethod
    def preprocess_for_ocr(image: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Enhances label image for OCR text detection and recognition.
        Performs LAB-space CLAHE enhancement, illumination leveling,
        and high-resolution upscaling for tiny packaging fonts.
        """
        h, w = image.shape[:2]

        # 1. Image Quality Assessment
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = float(np.mean(gray))
        contrast_std = float(np.std(gray))

        # 2. Intelligent Multi-Scale Upscaling for small packaging labels
        # If minimum dimension is small, upscale with cubic antialiasing
        target_img = image.copy()
        upscale_factor = 1.0
        if max(h, w) < 1600:
            upscale_factor = min(2.0, 1800.0 / max(h, w))
            if upscale_factor > 1.1:
                new_w = int(w * upscale_factor)
                new_h = int(h * upscale_factor)
                target_img = cv2.resize(target_img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # 3. LAB Color Space CLAHE Enhancement (Preserves crisp text boundaries)
        lab = cv2.cvtColor(target_img, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # Adaptive CLAHE based on contrast
        clip_limit = 2.5 if contrast_std < 45 else 1.8
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        cl_l = clahe.apply(l_channel)
        
        enhanced_lab = cv2.merge((cl_l, a_channel, b_channel))
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        # 4. Unsharp Masking for fine font sharpening
        gaussian = cv2.GaussianBlur(enhanced_bgr, (0, 0), 2.0)
        sharpened = cv2.addWeighted(enhanced_bgr, 1.3, gaussian, -0.3, 0)

        metrics = {
            "mean_brightness": round(mean_brightness, 2),
            "contrast_std": round(contrast_std, 2),
            "width": w,
            "height": h,
            "upscale_factor": round(upscale_factor, 2),
            "is_low_light": mean_brightness < 60,
            "is_low_contrast": contrast_std < 35,
            "quality_rating": "GOOD" if contrast_std >= 40 and 60 <= mean_brightness <= 210 else "FAIR" if contrast_std >= 25 else "LOW"
        }

        return sharpened, metrics

    @staticmethod
    def detect_skew_and_correct(image: np.ndarray) -> Tuple[np.ndarray, float]:
        """Detects skew angle and rotates image if necessary."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
        
        angle = 0.0
        if lines is not None and len(lines) > 0:
            angles = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 - x1 != 0:
                    deg = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                    if abs(deg) < 45:  # Consider only near horizontal lines
                        angles.append(deg)
            if angles:
                angle = float(np.median(angles))
                
        if abs(angle) > 0.8:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return corrected, angle
            
        return image, 0.0
