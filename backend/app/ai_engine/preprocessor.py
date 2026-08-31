"""
PRAMAN AI - Image Preprocessing Module
Uses OpenCV for image enhancement, noise reduction, deskewing, and contrast optimization.
"""

import cv2
import numpy as np
import os
from typing import Tuple, Dict, Any

class ImagePreprocessor:
    @staticmethod
    def load_image(image_path: str) -> np.ndarray:
        """Loads image handling unicode paths."""
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
        Enhances image for text detection and OCR.
        Returns:
            processed_image: optimized grayscale/binary image for OCR
            metrics: image quality and contrast metrics
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate image brightness and contrast
        mean_brightness = float(np.mean(gray))
        contrast_std = float(np.std(gray))
        
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(gray)
        
        # Bilateral filter to smooth texture while preserving sharp text edges
        denoised = cv2.bilateralFilter(contrast_enhanced, d=9, sigmaColor=75, sigmaSpace=75)
        
        # Adaptive thresholding for high text clarity
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8
        )
        
        metrics = {
            "mean_brightness": round(mean_brightness, 2),
            "contrast_std": round(contrast_std, 2),
            "width": image.shape[1],
            "height": image.shape[0],
            "is_low_light": mean_brightness < 60,
            "is_low_contrast": contrast_std < 35,
            "quality_rating": "GOOD" if contrast_std >= 40 and 60 <= mean_brightness <= 210 else "FAIR" if contrast_std >= 25 else "LOW"
        }
        
        return denoised, metrics

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
                
        if abs(angle) > 0.5:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return corrected, angle
            
        return image, 0.0
