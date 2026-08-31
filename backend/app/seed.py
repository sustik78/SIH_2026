"""
PRAMAN AI - Database Seeder
Populates initial enforcement users and sample inspection history records.
"""

from .database import SessionLocal, engine, Base
from .models import User, Product, Inspection, ExtractedDeclaration, ComplianceResult, Violation, AuditLog
from .auth import hash_password
from datetime import datetime, timedelta

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if users exist
    if db.query(User).count() == 0:
        users = [
            User(
                username="admin",
                email="admin@legalmetrology.gov.in",
                hashed_password=hash_password("Admin@123"),
                full_name="Dr. Rajesh Kumar Verma",
                role="ADMIN",
                badge_number="LM-ADM-001",
                department="Directorate of Legal Metrology, HQ"
            ),
            User(
                username="supervisor",
                email="supervisor@legalmetrology.gov.in",
                hashed_password=hash_password("Super@123"),
                full_name="Smt. Ananya Sen",
                role="SUPERVISOR",
                badge_number="LM-SUP-014",
                department="Regional Standards & Enforcement Zone-II"
            ),
            User(
                username="inspector",
                email="inspector@legalmetrology.gov.in",
                hashed_password=hash_password("Inspect@123"),
                full_name="Shri Amit Sharma",
                role="INSPECTOR",
                badge_number="LM-INS-108",
                department="Field Inspection & Packaged Commodity Cell"
            )
        ]
        db.add_all(users)
        db.commit()
        print("Default users seeded successfully.")

    # Seed demo inspections if empty
    if db.query(Inspection).count() == 0:
        inspector = db.query(User).filter(User.username == "inspector").first()
        
        # Product 1: Compliant Atta
        p1 = Product(
            product_name="Chakki Fresh Whole Wheat Atta",
            brand="PRAMAN Agro Foods",
            category="Packaged Food / Atta",
            manufacturer_name="PRAMAN Agro Foods Pvt. Ltd., Okhla Phase-III, New Delhi - 110020",
            declared_net_qty="5.0 kg",
            declared_mrp="₹ 230.00"
        )
        db.add(p1)
        db.flush()

        insp1 = Inspection(
            inspection_id="PRM-20260830-COMP01",
            product_id=p1.id,
            inspector_id=inspector.id,
            inspector_name=inspector.full_name,
            product_name=p1.product_name,
            category=p1.category,
            image_url="/api/static/samples/sample_compliant_atta.jpg",
            annotated_image_url="/api/static/samples/sample_compliant_atta.jpg",
            overall_score=96,
            compliance_status="COMPLIANT",
            decision_summary="Package satisfies statutory Legal Metrology requirements under PCR 2011 and amendments.",
            recommended_action="Approve for retail distribution. No enforcement action required.",
            passed_count=10,
            warning_count=1,
            violation_count=0,
            critical_violations_count=0,
            ocr_confidence=92.5,
            raw_ocr_text="PRAMAN AGRO FOODS - WHOLE WHEAT ATTA Chakki Fresh Whole Wheat Atta Net Quantity: 5.0 kg MRP ₹ 230.00 (inclusive of all taxes) Unit Sale Price: ₹ 46.00 / kg Date of Mfg: 08/2026 Consumer Care: 1800-11-2026 care@pramanfoods.in Made in India",
            status="COMPLETED",
            created_at=datetime.utcnow() - timedelta(hours=2)
        )
        db.add(insp1)
        db.flush()

        # Product 2: Non-compliant Oil
        p2 = Product(
            product_name="Refined Sunflower Oil",
            brand="Surya Agro Mills",
            category="Edible Oils & Fats",
            manufacturer_name="Surya Agro Mills, Industrial Area, Sector 5, Haryana",
            declared_net_qty="1.0 L",
            declared_mrp="₹ 155.00"
        )
        db.add(p2)
        db.flush()

        insp2 = Inspection(
            inspection_id="PRM-20260830-WARN02",
            product_id=p2.id,
            inspector_id=inspector.id,
            inspector_name=inspector.full_name,
            product_name=p2.product_name,
            category=p2.category,
            image_url="/api/static/samples/sample_noncompliant_oil.jpg",
            annotated_image_url="/api/static/samples/sample_noncompliant_oil.jpg",
            overall_score=68,
            compliance_status="NON-COMPLIANT",
            decision_summary="Regulatory non-compliance detected: MRP lacks statutory tax wording and Consumer Care helpline/email omitted.",
            recommended_action="Issue Statutory Show Cause Notice under Legal Metrology (Packaged Commodities) Rules, 2011.",
            passed_count=7,
            warning_count=1,
            violation_count=2,
            critical_violations_count=0,
            ocr_confidence=88.0,
            raw_ocr_text="SURYA SUNFLOWER OIL Refined Sunflower Oil Net Qty: 1.0 L MRP: ₹ 155.00 Unit Sale Price: ₹ 155.00 / L Pkd Date: 07/2026 Consumer Care: Contact Us at Corporate Office Made in India",
            status="COMPLETED",
            created_at=datetime.utcnow() - timedelta(hours=5)
        )
        db.add(insp2)
        db.flush()

        # Product 3: Critical Violation Snack
        p3 = Product(
            product_name="Desi Chatpata Namkeen",
            brand="Local Snacks Unit",
            category="Snack Foods",
            manufacturer_name="Local Snacks Unit, Delhi",
            declared_net_qty="Jumbo Saver Pack",
            declared_mrp="Rs 50"
        )
        db.add(p3)
        db.flush()

        insp3 = Inspection(
            inspection_id="PRM-20260830-CRIT03",
            product_id=p3.id,
            inspector_id=inspector.id,
            inspector_name=inspector.full_name,
            product_name=p3.product_name,
            category=p3.category,
            image_url="/api/static/samples/sample_critical_snack.jpg",
            annotated_image_url="/api/static/samples/sample_critical_snack.jpg",
            overall_score=32,
            compliance_status="NON-COMPLIANT",
            decision_summary="Critical metrology infractions: Prohibited expression 'Jumbo Saver Pack' in place of standard SI unit, missing MRP format, missing COO.",
            recommended_action="Issue immediate Notice under Section 36(1) of Legal Metrology Act, 2009. Seizure of non-standard pre-packaged commodity recommended.",
            passed_count=3,
            warning_count=2,
            violation_count=4,
            critical_violations_count=2,
            ocr_confidence=82.0,
            raw_ocr_text="DESI CHATPATA NAMKEEN Spicy Mixture Namkeen Net Quantity: Jumbo Saver Pack Date of Packing: 08/2026 Price: Special Offer Rs 50 Unit Sale Price: Not Declared",
            status="FLAGGED",
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        db.add(insp3)
        db.commit()
        print("Sample inspection data seeded successfully.")

    db.close()

if __name__ == "__main__":
    seed_database()
