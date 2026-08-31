"""
PRAMAN AI - Analytics & Dashboard Metrics Route
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Inspection, Violation, ExtractedDeclaration
from ..auth import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Dashboard"])

@router.get("/summary")
def get_dashboard_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_inspections = db.query(Inspection).count()
    compliant_count = db.query(Inspection).filter(Inspection.compliance_status == "COMPLIANT").count()
    non_compliant_count = db.query(Inspection).filter(Inspection.compliance_status == "NON-COMPLIANT").count()
    pending_review_count = db.query(Inspection).filter(Inspection.compliance_status == "PENDING REVIEW").count()
    critical_violations_total = db.query(func.sum(Inspection.critical_violations_count)).scalar() or 0
    
    compliance_rate = round((compliant_count / total_inspections * 100), 1) if total_inspections > 0 else 0.0

    # Top violations breakdown
    violations = db.query(Violation.rule_id, func.count(Violation.id).label("count")).group_by(Violation.rule_id).order_by(func.count(Violation.id).desc()).limit(6).all()
    top_violations = [
        {"rule_id": v[0], "count": v[1]}
        for v in violations
    ]

    # Category distribution
    categories_stat = db.query(Inspection.category, func.count(Inspection.id)).group_by(Inspection.category).all()
    category_breakdown = [
        {"category": c[0], "count": c[1]}
        for c in categories_stat
    ]

    return {
        "total_scans": total_inspections,
        "compliant_count": compliant_count,
        "non_compliant_count": non_compliant_count,
        "pending_review_count": pending_review_count,
        "critical_violations_count": critical_violations_total,
        "compliance_rate": compliance_rate,
        "top_violations": top_violations,
        "category_breakdown": category_breakdown
    }
