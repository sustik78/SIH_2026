"""
PRAMAN AI - Report Generation & Audit Logs Endpoints
"""

import os
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Inspection, ExtractedDeclaration, ComplianceResult, Violation, Report, AuditLog
from ..auth import get_current_user
from ..reports.pdf_report import PDFReportGenerator
from ..reports.docx_report import DOCXReportGenerator

report_router = APIRouter(prefix="/api/reports", tags=["Reports"])
audit_router = APIRouter(prefix="/api/audit", tags=["Audit Trail"])

REPORTS_DIR = os.path.abspath("backend/reports_out")
os.makedirs(REPORTS_DIR, exist_ok=True)

def _get_inspection_payload(inspection_id: str, db: Session) -> dict:
    inspection = db.query(Inspection).filter(
        (Inspection.inspection_id == inspection_id) | (Inspection.id == int(inspection_id) if inspection_id.isdigit() else False)
    ).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found.")

    declarations = db.query(ExtractedDeclaration).filter(ExtractedDeclaration.inspection_id == inspection.id).all()
    results = db.query(ComplianceResult).filter(ComplianceResult.inspection_id == inspection.id).all()
    violations = db.query(Violation).filter(Violation.inspection_id == inspection.id).all()

    return {
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
        "declarations": [
            {
                "field_name": d.field_name,
                "detected_value": d.detected_value,
                "is_found": d.is_found,
                "confidence_score": d.confidence_score
            }
            for d in declarations
        ],
        "results": [
            {
                "rule_id": r.rule_id,
                "rule_name": r.rule_name,
                "status": r.status,
                "severity": r.severity,
                "explanation": r.explanation,
                "source_document": r.source_document,
                "source_section": r.source_section,
                "crop_url": r.crop_url
            }
            for r in results
        ],
        "violations": [
            {
                "rule_id": v.rule_id,
                "violation_title": v.violation_title,
                "severity": v.severity,
                "description": v.description,
                "legal_basis": v.legal_basis
            }
            for v in violations
        ]
    }

@report_router.get("/{inspection_id}/pdf")
def download_pdf_report(
    inspection_id: str,
    db: Session = Depends(get_db)
):
    payload = _get_inspection_payload(inspection_id, db)
    out_filename = f"report_{inspection_id}.pdf"
    out_path = os.path.join(REPORTS_DIR, out_filename)
    
    PDFReportGenerator.generate(payload, out_path)

    return FileResponse(
        out_path,
        media_type="application/pdf",
        filename=f"PRAMAN_Inspection_Report_{inspection_id}.pdf"
    )

@report_router.get("/{inspection_id}/docx")
def download_docx_report(
    inspection_id: str,
    db: Session = Depends(get_db)
):
    payload = _get_inspection_payload(inspection_id, db)
    out_filename = f"report_{inspection_id}.docx"
    out_path = os.path.join(REPORTS_DIR, out_filename)
    
    DOCXReportGenerator.generate(payload, out_path)

    return FileResponse(
        out_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"PRAMAN_Inspection_Report_{inspection_id}.docx"
    )

# Audit logs endpoint
@audit_router.get("/logs")
def list_audit_logs(
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": l.id,
            "username": l.username,
            "action": l.action,
            "entity_type": l.entity_type,
            "entity_id": l.entity_id,
            "details": l.details,
            "ip_address": l.ip_address,
            "timestamp": l.timestamp.strftime("%d-%b-%Y %H:%M:%S")
        }
        for l in logs
    ]
