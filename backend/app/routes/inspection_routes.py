"""
PRAMAN AI - Inspection Management Routes
"""

import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import Inspection, ExtractedDeclaration, ComplianceResult, Violation, AuditLog, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/inspections", tags=["Inspections"])

@router.get("")
def list_inspections(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Inspection)
    if status and status != "ALL":
        query = query.filter(Inspection.compliance_status == status)
    if category and category != "ALL":
        query = query.filter(Inspection.category == category)
    if search:
        query = query.filter(
            (Inspection.product_name.ilike(f"%{search}%")) |
            (Inspection.inspection_id.ilike(f"%{search}%")) |
            (Inspection.inspector_name.ilike(f"%{search}%"))
        )
    
    inspections = query.order_by(Inspection.created_at.desc()).all()
    
    return [
        {
            "id": i.id,
            "inspection_id": i.inspection_id,
            "product_name": i.product_name,
            "category": i.category,
            "inspector_name": i.inspector_name,
            "overall_score": i.overall_score,
            "compliance_status": i.compliance_status,
            "decision_summary": i.decision_summary,
            "violation_count": i.violation_count,
            "warning_count": i.warning_count,
            "critical_violations_count": i.critical_violations_count,
            "image_url": i.image_url,
            "annotated_image_url": i.annotated_image_url,
            "created_at": i.created_at.strftime("%d-%b-%Y %H:%M"),
            "status": i.status
        }
        for i in inspections
    ]

@router.get("/{inspection_id}")
def get_inspection_details(
    inspection_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inspection = db.query(Inspection).filter(
        (Inspection.inspection_id == inspection_id) | (Inspection.id == int(inspection_id) if inspection_id.isdigit() else False)
    ).first()
    
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection record not found.")

    declarations = db.query(ExtractedDeclaration).filter(ExtractedDeclaration.inspection_id == inspection.id).all()
    results = db.query(ComplianceResult).filter(ComplianceResult.inspection_id == inspection.id).all()
    violations = db.query(Violation).filter(Violation.inspection_id == inspection.id).all()

    category_scores = []
    if inspection.category_scores_json:
        try:
            category_scores = json.loads(inspection.category_scores_json)
        except Exception:
            pass

    return {
        "id": inspection.id,
        "inspection_id": inspection.inspection_id,
        "product_name": inspection.product_name,
        "category": inspection.category,
        "inspector_name": inspection.inspector_name,
        "overall_score": inspection.overall_score,
        "compliance_status": inspection.compliance_status,
        "decision_summary": inspection.decision_summary,
        "recommended_action": inspection.recommended_action,
        "image_url": inspection.image_url,
        "annotated_image_url": inspection.annotated_image_url,
        "ocr_confidence": inspection.ocr_confidence,
        "raw_ocr_text": inspection.raw_ocr_text,
        "passed_count": inspection.passed_count,
        "warning_count": inspection.warning_count,
        "violation_count": inspection.violation_count,
        "critical_violations_count": inspection.critical_violations_count,
        "category_scores": category_scores,
        "status": inspection.status,
        "supervisor_notes": inspection.supervisor_notes,
        "created_at": inspection.created_at.strftime("%d-%b-%Y %H:%M"),
        "declarations": [
            {
                "id": d.id,
                "field_name": d.field_name,
                "detected_value": d.detected_value,
                "is_found": d.is_found,
                "confidence_score": d.confidence_score,
                "bbox": json.loads(d.bbox_json) if d.bbox_json else None
            }
            for d in declarations
        ],
        "results": [
            {
                "id": r.id,
                "rule_id": r.rule_id,
                "rule_name": r.rule_name,
                "category": r.category,
                "requirement": r.requirement,
                "detected_value": r.detected_value,
                "expected_condition": r.expected_condition,
                "status": r.status,
                "severity": r.severity,
                "explanation": r.explanation,
                "source_document": r.source_document,
                "source_section": r.source_section,
                "crop_url": r.crop_url,
                "bbox": json.loads(r.bbox_json) if r.bbox_json else None
            }
            for r in results
        ],
        "violations": [
            {
                "id": v.id,
                "rule_id": v.rule_id,
                "violation_title": v.violation_title,
                "severity": v.severity,
                "description": v.description,
                "legal_basis": v.legal_basis,
                "evidence_crop_url": v.evidence_crop_url,
                "detected_value": v.detected_value
            }
            for v in violations
        ]
    }

@router.post("/{inspection_id}/review")
def update_inspection_review(
    inspection_id: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inspection = db.query(Inspection).filter(
        (Inspection.inspection_id == inspection_id) | (Inspection.id == int(inspection_id) if inspection_id.isdigit() else False)
    ).first()
    
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection record not found.")

    new_status = payload.get("status", inspection.status)
    notes = payload.get("supervisor_notes", "")

    inspection.status = new_status
    if notes:
        inspection.supervisor_notes = notes

    # Log audit entry
    audit = AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="INSPECTION_REVIEWED",
        entity_type="INSPECTION",
        entity_id=inspection.inspection_id,
        details=f"Status changed to {new_status}. Notes: {notes}"
    )
    db.add(audit)
    db.commit()

    return {"message": "Inspection review recorded successfully.", "status": new_status}
