"""
PRAMAN AI - Product Catalog & Rule Library Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Product, Inspection
from ..auth import get_current_user
from ..compliance_engine.rule_definitions import COMPLIANCE_RULES

# Product Router
product_router = APIRouter(prefix="/api/products", tags=["Products"])

@product_router.get("")
def list_products(
    search: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if search:
        query = query.filter(
            (Product.product_name.ilike(f"%{search}%")) |
            (Product.brand.ilike(f"%{search}%")) |
            (Product.manufacturer_name.ilike(f"%{search}%"))
        )
    products = query.order_by(Product.created_at.desc()).all()
    
    results = []
    for p in products:
        insp_count = db.query(Inspection).filter(Inspection.product_id == p.id).count()
        last_insp = db.query(Inspection).filter(Inspection.product_id == p.id).order_by(Inspection.created_at.desc()).first()
        results.append({
            "id": p.id,
            "product_name": p.product_name,
            "brand": p.brand,
            "category": p.category,
            "manufacturer_name": p.manufacturer_name,
            "declared_net_qty": p.declared_net_qty,
            "declared_mrp": p.declared_mrp,
            "inspections_count": insp_count,
            "latest_score": last_insp.overall_score if last_insp else None,
            "latest_status": last_insp.compliance_status if last_insp else None,
            "created_at": p.created_at.strftime("%d-%b-%Y")
        })
    return results

# Rule Router
rule_router = APIRouter(prefix="/api/rules", tags=["Rule Library"])

@rule_router.get("")
def list_rules(category: Optional[str] = None):
    rules = COMPLIANCE_RULES
    if category and category != "ALL":
        rules = [r for r in rules if r["category"].lower() == category.lower()]
    return rules
