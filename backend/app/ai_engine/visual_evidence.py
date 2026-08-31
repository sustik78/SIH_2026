"""
PRAMAN AI - Visual Evidence Generator
Draws bounding boxes and regulatory violation overlays on packaging images.
Generates cropped evidence snippets for inspection reports.
"""

import cv2
import numpy as np
import os
import uuid
from typing import Dict, Any, List

class VisualEvidenceGenerator:
    @staticmethod
    def generate_annotated_evidence(
        original_image: np.ndarray,
        compliance_results: List[Dict[str, Any]],
        output_dir: str
    ) -> Dict[str, Any]:
        """
        Draws color-coded bounding boxes on the image and crops violation areas.
        """
        os.makedirs(output_dir, exist_ok=True)
        annotated = original_image.copy()
        h_img, w_img = annotated.shape[:2]

        evidence_items = []
        box_count = 0

        # Colors in BGR
        COLOR_PASS = (46, 174, 96)       # Green
        COLOR_WARN = (33, 145, 245)      # Amber / Orange
        COLOR_VIOLATION = (36, 36, 220)  # Red
        COLOR_INFO = (235, 130, 60)      # Blue

        for rule in compliance_results:
            bbox = rule.get("bbox")
            status = rule.get("status")
            rule_id = rule.get("rule_id")
            rule_name = rule.get("rule_name")
            val = rule.get("detected_value")

            if not bbox or not isinstance(bbox, dict):
                continue

            x = max(0, int(bbox.get("x", 0)))
            y = max(0, int(bbox.get("y", 0)))
            w = min(w_img - x, int(bbox.get("w", 0)))
            h = min(h_img - y, int(bbox.get("h", 0)))

            if w <= 5 or h <= 5:
                continue

            box_count += 1

            if status == "PASS":
                color = COLOR_PASS
                status_text = "PASS"
            elif status == "WARNING":
                color = COLOR_WARN
                status_text = "WARNING"
            elif status == "VIOLATION":
                color = COLOR_VIOLATION
                status_text = "VIOLATION"
            else:
                color = COLOR_INFO
                status_text = "MANUAL REVIEW"

            # Draw rectangle
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 3)

            # Draw badge background
            label = f"[{status_text}] {rule_id}: {val[:30]}"
            (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
            
            badge_y1 = max(0, y - text_h - 10)
            badge_y2 = y
            badge_x2 = min(w_img, x + text_w + 10)

            cv2.rectangle(annotated, (x, badge_y1), (badge_x2, badge_y2), color, -1)
            cv2.putText(
                annotated,
                label,
                (x + 5, badge_y2 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Crop snippet for evidence card
            pad_x = min(20, x)
            pad_y = min(20, y)
            crop_x2 = min(w_img, x + w + 20)
            crop_y2 = min(h_img, y + h + 20)

            crop = original_image[y - pad_y : crop_y2, x - pad_x : crop_x2]
            crop_filename = f"crop_{rule_id}_{uuid.uuid4().hex[:8]}.jpg"
            crop_path = os.path.join(output_dir, crop_filename)
            
            # Save crop safely
            cv2.imencode(".jpg", crop)[1].tofile(crop_path)

            evidence_items.append({
                "rule_id": rule_id,
                "rule_name": rule_name,
                "status": status,
                "label": label,
                "detected_text": val,
                "bbox": {"x": x, "y": y, "w": w, "h": h},
                "crop_filename": crop_filename,
                "explanation": rule.get("explanation"),
                "source_reference": f"{rule.get('source_section')} ({rule.get('source_document')})"
            })

        # Save annotated image
        annotated_filename = f"annotated_{uuid.uuid4().hex[:8]}.jpg"
        annotated_path = os.path.join(output_dir, annotated_filename)
        cv2.imencode(".jpg", annotated)[1].tofile(annotated_path)

        return {
            "annotated_filename": annotated_filename,
            "annotated_path": annotated_path,
            "total_boxes_drawn": box_count,
            "evidence_items": evidence_items
        }
