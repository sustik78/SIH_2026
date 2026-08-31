"""
PRAMAN AI - Product Scanning & AI Inspection Pipeline Route
Coordinates: Upload -> OpenCV Preprocessing -> OCR -> Extraction -> Compliance Engine -> Scoring -> Evidence Overlay.
"""

import os
import uuid
import shutil
import json
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import Inspection, ExtractedDeclaration, ComplianceResult, Violation, AuditLog, Product, User
from ..auth import get_current_user
from ..ai_engine.preprocessor import ImagePreprocessor
from ..ai_engine.ocr_engine import OCREngine
from ..ai_engine.declaration_extractor import DeclarationExtractor
from ..ai_engine.visual_evidence import VisualEvidenceGenerator
from ..compliance_engine.engine import ComplianceRuleEngine
from ..compliance_engine.scoring import ComplianceScorer

router = APIRouter(prefix="/api/scan", tags=["Scanning & Inspection"])

UPLOAD_DIR = os.path.abspath("backend/uploads")
SAMPLES_DIR = os.path.abspath("backend/samples")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)

ocr_engine = OCREngine()

@router.get("/demo-samples")
def get_demo_samples():
    """Returns curated demo scenarios for instant judge evaluation."""
    return [
        {
            "id": "sample_1",
            "title": "Chakki Fresh Atta (5 kg)",
            "category": "Packaged Food / Atta",
            "expected_outcome": "COMPLIANT (Score: 96/100)",
            "description": "Standard retail packaging with complete mandatory declarations: Metric Net Qty (5.0 kg), MRP with taxes, calculated USP (₹46.00/kg), Mfr address with Pincode, Helpline & Email.",
            "filename": "sample_compliant_atta.jpg",
            "image_url": "/api/static/samples/sample_compliant_atta.jpg"
        },
        {
            "id": "sample_2",
            "title": "Refined Sunflower Oil (1 Litre)",
            "category": "Edible Oils & Fats",
            "expected_outcome": "NON-COMPLIANT (Score: 68/100)",
            "description": "Packaging contains MRP without 'inclusive of all taxes' clause and omits statutory email/helpline under Rule 6(1)(f).",
            "filename": "sample_noncompliant_oil.jpg",
            "image_url": "/api/static/samples/sample_noncompliant_oil.jpg"
        },
        {
            "id": "sample_3",
            "title": "Desi Namkeen Snack Pack",
            "category": "Snack Foods",
            "expected_outcome": "CRITICAL VIOLATION (Score: 32/100)",
            "description": "Prohibited non-standard expression 'Jumbo Saver Pack' without metric weight, non-standard price without MRP, missing manufacturer full address and missing Country of Origin.",
            "filename": "sample_critical_snack.jpg",
            "image_url": "/api/static/samples/sample_critical_snack.jpg"
        }
    ]

@router.post("/upload")
async def scan_package_image(
    file: Optional[UploadFile] = File(None),
    sample_filename: Optional[str] = Form(None),
    product_name: Optional[str] = Form("Scanned Pre-Packaged Commodity"),
    category: Optional[str] = Form("General Packaged Commodity"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Full AI & Compliance Engine execution pipeline.
    """
    inspection_uuid = f"PRM-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    # 1. Save or locate image
    if sample_filename:
        src_path = os.path.join(SAMPLES_DIR, sample_filename)
        if not os.path.exists(src_path):
            raise HTTPException(status_code=404, detail="Sample image file not found.")
        dest_filename = f"scan_{uuid.uuid4().hex[:8]}_{sample_filename}"
        dest_path = os.path.join(UPLOAD_DIR, dest_filename)
        shutil.copyfile(src_path, dest_path)
    elif file:
        file_ext = os.path.splitext(file.filename)[1] or ".jpg"
        dest_filename = f"scan_{uuid.uuid4().hex[:8]}{file_ext}"
        dest_path = os.path.join(UPLOAD_DIR, dest_filename)
        with open(dest_path, "wb") as f:
            content = await file.read()
            f.write(content)
    else:
        raise HTTPException(status_code=400, detail="Must provide an uploaded image file or a valid sample_filename.")

    image_rel_url = f"/api/static/uploads/{dest_filename}"

    # 2. OpenCV Preprocessing
    try:
        raw_cv_img = ImagePreprocessor.load_image(dest_path)
        processed_img, img_metrics = ImagePreprocessor.preprocess_for_ocr(raw_cv_img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image preprocessing failed: {str(e)}")

    # 3. OCR Text & Bounding Box Extraction
    ocr_res = ocr_engine.extract_text_and_boxes(raw_cv_img)
    
    # 4. Declarations Extraction
    declarations_dict = DeclarationExtractor.extract_declarations(ocr_res)

    # 5. Deterministic Compliance Rule Engine
    eval_res = ComplianceRuleEngine.evaluate_compliance(
        declarations=declarations_dict,
        image_metrics=img_metrics,
        product_category=category
    )

    # 6. Scoring & Decision
    score_res = ComplianceScorer.calculate_score(eval_res)

    # 7. Visual Evidence & Overlay Generation
    evidence_res = VisualEvidenceGenerator.generate_annotated_evidence(
        original_image=raw_cv_img,
        compliance_results=eval_res["results"],
        output_dir=UPLOAD_DIR
    )

    annotated_rel_url = f"/api/static/uploads/{evidence_res['annotated_filename']}"

    # Derive clean product name if detected
    detected_comm = declarations_dict.get("commodity_name", {}).get("value")
    final_product_name = detected_comm if detected_comm else product_name

    # 8. Store in Database
    # Check or create product
    mfr_name = declarations_dict.get("manufacturer_details", {}).get("value")
    net_qty_val = declarations_dict.get("net_quantity", {}).get("value")
    mrp_val = declarations_dict.get("mrp", {}).get("value")

    product = Product(
        product_name=final_product_name,
        brand="Detected Brand" if mfr_name else "Unbranded",
        category=category,
        manufacturer_name=mfr_name,
        declared_net_qty=net_qty_val,
        declared_mrp=mrp_val
    )
    db.add(product)
    db.flush()

    inspection = Inspection(
        inspection_id=inspection_uuid,
        product_id=product.id,
        inspector_id=current_user.id,
        inspector_name=current_user.full_name,
        product_name=final_product_name,
        category=category,
        image_url=image_rel_url,
        annotated_image_url=annotated_rel_url,
        overall_score=score_res["overall_score"],
        compliance_status=score_res["decision"],
        decision_summary=score_res["decision_summary"],
        recommended_action=score_res["recommended_action"],
        passed_count=eval_res["passed_count"],
        warning_count=eval_res["warning_count"],
        violation_count=eval_res["violation_count"],
        critical_violations_count=eval_res["critical_violations_count"],
        category_scores_json=json.dumps(score_res["categories"]),
        raw_ocr_text=ocr_res.get("raw_text", ""),
        ocr_confidence=ocr_res.get("average_confidence", 0.0),
        status="COMPLETED"
    )
    db.add(inspection)
    db.flush()

    # Save extracted declarations
    for k, v in declarations_dict.items():
        if isinstance(v, dict):
            decl = ExtractedDeclaration(
                inspection_id=inspection.id,
                field_name=k.replace("_", " ").title(),
                detected_value=str(v.get("value") or ""),
                is_found=bool(v.get("found", False)),
                confidence_score=float(v.get("confidence", 0.0)),
                bbox_json=json.dumps(v.get("bbox")) if v.get("bbox") else None
            )
            db.add(decl)

    # Save rule results & violations
    for r in eval_res["results"]:
        crop_url = None
        # Find matching crop in evidence_res
        for ev in evidence_res["evidence_items"]:
            if ev["rule_id"] == r["rule_id"]:
                crop_url = f"/api/static/uploads/{ev['crop_filename']}"
                break

        res_obj = ComplianceResult(
            inspection_id=inspection.id,
            rule_id=r["rule_id"],
            rule_name=r["rule_name"],
            category=r["category"],
            requirement=r["requirement"],
            detected_value=r["detected_value"],
            expected_condition=r["expected_condition"],
            status=r["status"],
            severity=r["severity"],
            explanation=r["explanation"],
            source_document=r["source_document"],
            source_section=r["source_section"],
            crop_url=crop_url,
            bbox_json=json.dumps(r["bbox"]) if r["bbox"] else None
        )
        db.add(res_obj)

        if r["status"] in ["VIOLATION", "WARNING"]:
            violation_obj = Violation(
                inspection_id=inspection.id,
                rule_id=r["rule_id"],
                violation_title=f"{r['rule_name']} ({r['status']})",
                severity=r["severity"],
                description=r["explanation"],
                legal_basis=f"{r['source_section']} - {r['source_document']}",
                evidence_crop_url=crop_url,
                detected_value=r["detected_value"]
            )
            db.add(violation_obj)

    # Log audit entry
    audit = AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="PRODUCT_SCANNED",
        entity_type="INSPECTION",
        entity_id=inspection_uuid,
        details=f"Scanned {final_product_name}. Decision: {score_res['decision']}, Score: {score_res['overall_score']}/100"
    )
    db.add(audit)
    db.commit()

    return {
        "inspection_id": inspection_uuid,
        "product_name": final_product_name,
        "category": category,
        "overall_score": score_res["overall_score"],
        "compliance_status": score_res["decision"],
        "decision_summary": score_res["decision_summary"],
        "recommended_action": score_res["recommended_action"],
        "image_url": image_rel_url,
        "annotated_image_url": annotated_rel_url,
        "ocr_confidence": ocr_res.get("average_confidence", 0.0),
        "raw_ocr_text": ocr_res.get("raw_text", ""),
        "passed_count": eval_res["passed_count"],
        "warning_count": eval_res["warning_count"],
        "violation_count": eval_res["violation_count"],
        "critical_violations_count": eval_res["critical_violations_count"],
        "category_scores": score_res["categories"],
        "evidence_items": evidence_res["evidence_items"],
        "results": eval_res["results"],
        "declarations": declarations_dict
    }
