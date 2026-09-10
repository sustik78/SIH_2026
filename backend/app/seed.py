"""
PRAMAN AI - Database Seeder
Populates initial enforcement users and sample inspection history records.
"""

import json
from .database import SessionLocal, engine, Base
from .models import User, Product, Inspection, ExtractedDeclaration, ComplianceResult, Violation, AuditLog
from .auth import hash_password
from datetime import datetime, timedelta

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # The 6 exact authorized users
    official_users_data = [
        {
            "name": "Soutik",
            "email": "Soutik@email.com",
            "password": "Soutik1234",
            "role": "ADMIN",
            "badge_number": "LM-ADM-001",
            "department": "Directorate of Legal Metrology, Central Headquarters & Apex Command"
        },
        {
            "name": "Sayantan",
            "email": "Sayantan@email.com",
            "password": "Sayantan1234",
            "role": "SUPERVISOR",
            "badge_number": "LM-SUP-102",
            "department": "Regional Standards & Enforcement Zone-I"
        },
        {
            "name": "Jiya",
            "email": "Jiya@email.com",
            "password": "Jiya1234",
            "role": "INSPECTOR",
            "badge_number": "LM-INS-203",
            "department": "Packaged Commodity Audit & Verification Cell"
        },
        {
            "name": "Rimi",
            "email": "Rimi@email.com",
            "password": "Rimi1234",
            "role": "ADMIN",
            "badge_number": "LM-ADM-004",
            "department": "Directorate of Legal Metrology, HQ Central Command"
        },
        {
            "name": "Debopriya",
            "email": "Debopriya@email.com",
            "password": "Debopriya1234",
            "role": "SUPERVISOR",
            "badge_number": "LM-SUP-105",
            "department": "Regional Standards & Legal Enforcement Zone-II"
        },
        {
            "name": "Arkadip",
            "email": "Arkadip@email.com",
            "password": "Arkadip1234",
            "role": "INSPECTOR",
            "badge_number": "LM-INS-206",
            "department": "Field Inspection & Metrological Vigilance Unit"
        }
    ]

    # Remove any old legacy demo users if they exist
    legacy_usernames = ["admin", "supervisor", "inspector"]
    legacy_emails = ["admin@legalmetrology.gov.in", "supervisor@legalmetrology.gov.in", "inspector@legalmetrology.gov.in"]
    db.query(User).filter(
        (User.username.in_(legacy_usernames)) | 
        (User.email.in_(legacy_emails)) |
        (User.full_name == "Shri Amit Sharma")
    ).delete(synchronize_session=False)
    db.commit()

    # Ensure all 6 official users exist with correct credentials
    for udata in official_users_data:
        existing_user = db.query(User).filter(
            (User.email == udata["email"]) | 
            (User.username == udata["name"]) |
            (User.email.ilike(udata["email"]))
        ).first()

        if not existing_user:
            new_user = User(
                username=udata["name"],
                email=udata["email"],
                hashed_password=hash_password(udata["password"]),
                full_name=udata["name"],
                role=udata["role"],
                badge_number=udata["badge_number"],
                department=udata["department"],
                is_active=True
            )
            db.add(new_user)
        else:
            # Update credentials & attributes to exact specifications
            existing_user.username = udata["name"]
            existing_user.email = udata["email"]
            existing_user.hashed_password = hash_password(udata["password"])
            existing_user.full_name = udata["name"]
            existing_user.role = udata["role"]
            existing_user.badge_number = udata["badge_number"]
            existing_user.department = udata["department"]
            existing_user.is_active = True
    db.commit()
    print("Official 6 authorized users seeded successfully.")

    # Ensure demo inspections have nutrition and health classification populated
    lead_inspector = db.query(User).filter(User.username == "Soutik").first()
    if not lead_inspector:
        lead_inspector = db.query(User).first()

    # Update legacy inspector references
    db.query(Inspection).filter(Inspection.inspector_name == "Shri Amit Sharma").update(
        {"inspector_name": lead_inspector.full_name, "inspector_id": lead_inspector.id},
        synchronize_session=False
    )
    db.commit()

    # Nutrition data definitions
    atta_nutrition = {
        "energy": {"value": "364 kcal", "numeric_value": 364, "unit": "kcal", "per": "100g", "found": True},
        "protein": {"value": "12.1 g", "numeric_value": 12.1, "unit": "g", "per": "100g", "found": True},
        "carbohydrates": {"value": "71.2 g", "numeric_value": 71.2, "unit": "g", "per": "100g", "found": True},
        "sugars": {"value": "2.4 g", "numeric_value": 2.4, "unit": "g", "per": "100g", "found": True},
        "added_sugars": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
        "fat": {"value": "1.7 g", "numeric_value": 1.7, "unit": "g", "per": "100g", "found": True},
        "saturated_fat": {"value": "0.4 g", "numeric_value": 0.4, "unit": "g", "per": "100g", "found": True},
        "trans_fat": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
        "sodium": {"value": "5.0 mg", "numeric_value": 5.0, "unit": "mg", "per": "100g", "found": True},
        "fiber": {"value": "11.5 g", "numeric_value": 11.5, "unit": "g", "per": "100g", "found": True},
        "serving_size": {"value": "Per 100g", "found": True}
    }
    atta_health = {
        "classification": "HEALTHIER",
        "score": 92,
        "badge_color": "emerald",
        "summary": "Rich in dietary fiber and protein with low saturated fat, zero added sugar, and negligible sodium.",
        "positive_factors": [
            "High Dietary Fiber (11.5g / 100g)",
            "Good Protein Source (12.1g / 100g)",
            "Low Saturated Fat (< 1.5g / 100g)",
            "Negligible Sodium (< 120mg / 100g)"
        ],
        "risk_factors": [],
        "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
    }

    oil_nutrition = {
        "energy": {"value": "900 kcal", "numeric_value": 900, "unit": "kcal", "per": "100g", "found": True},
        "protein": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
        "carbohydrates": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
        "sugars": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
        "added_sugars": {"value": None, "numeric_value": None, "unit": "g", "per": "100g", "found": False},
        "fat": {"value": "100.0 g", "numeric_value": 100.0, "unit": "g", "per": "100g", "found": True},
        "saturated_fat": {"value": "11.0 g", "numeric_value": 11.0, "unit": "g", "per": "100g", "found": True},
        "trans_fat": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
        "sodium": {"value": "0.0 mg", "numeric_value": 0.0, "unit": "mg", "per": "100g", "found": True},
        "fiber": {"value": None, "numeric_value": None, "unit": "g", "per": "100g", "found": False},
        "serving_size": {"value": "Per 100g", "found": True}
    }
    oil_health = {
        "classification": "MODERATE",
        "score": 62,
        "badge_color": "amber",
        "summary": "100% lipid energy source with zero sugars and zero sodium. Saturated fat is within standard vegetable oil limits.",
        "positive_factors": [
            "Zero Sugar & Added Sugars",
            "Zero Sodium Content"
        ],
        "risk_factors": [
            "High Energy Density (900 kcal / 100g)",
            "High Total Fat (100g / 100g — standard for edible oil)"
        ],
        "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
    }

    snack_nutrition = {
        "energy": {"value": "548 kcal", "numeric_value": 548, "unit": "kcal", "per": "100g", "found": True},
        "protein": {"value": "8.5 g", "numeric_value": 8.5, "unit": "g", "per": "100g", "found": True},
        "carbohydrates": {"value": "44.2 g", "numeric_value": 44.2, "unit": "g", "per": "100g", "found": True},
        "sugars": {"value": "4.8 g", "numeric_value": 4.8, "unit": "g", "per": "100g", "found": True},
        "added_sugars": {"value": None, "numeric_value": None, "unit": "g", "per": "100g", "found": False},
        "fat": {"value": "36.8 g", "numeric_value": 36.8, "unit": "g", "per": "100g", "found": True},
        "saturated_fat": {"value": "16.5 g", "numeric_value": 16.5, "unit": "g", "per": "100g", "found": True},
        "trans_fat": {"value": "0.1 g", "numeric_value": 0.1, "unit": "g", "per": "100g", "found": True},
        "sodium": {"value": "890.0 mg", "numeric_value": 890.0, "unit": "mg", "per": "100g", "found": True},
        "fiber": {"value": "3.2 g", "numeric_value": 3.2, "unit": "g", "per": "100g", "found": True},
        "serving_size": {"value": "Per 100g", "found": True}
    }
    snack_health = {
        "classification": "HIGH / LESS HEALTHY",
        "score": 38,
        "badge_color": "rose",
        "summary": "High in Sodium and Saturated Fat. Exceeds recommended dietary threshold limits for daily snack consumption.",
        "positive_factors": [
            "Moderate Protein (8.5g / 100g)"
        ],
        "risk_factors": [
            "High Sodium: 890mg / 100g (Threshold: > 600mg)",
            "High Saturated Fat: 16.5g / 100g (Threshold: > 5g)",
            "High Total Fat: 36.8g / 100g"
        ],
        "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
    }

    # Update existing demo inspections
    insp_atta = db.query(Inspection).filter(Inspection.inspection_id == "PRM-20260830-COMP01").first()
    if insp_atta:
        insp_atta.nutrition_json = json.dumps(atta_nutrition)
        insp_atta.health_classification_json = json.dumps(atta_health)

    insp_oil = db.query(Inspection).filter(Inspection.inspection_id == "PRM-20260830-WARN02").first()
    if insp_oil:
        insp_oil.nutrition_json = json.dumps(oil_nutrition)
        insp_oil.health_classification_json = json.dumps(oil_health)

    insp_snack = db.query(Inspection).filter(Inspection.inspection_id == "PRM-20260830-CRIT03").first()
    if insp_snack:
        insp_snack.nutrition_json = json.dumps(snack_nutrition)
        insp_snack.health_classification_json = json.dumps(snack_health)
    
    # Also update any other inspections with atta in product name
    for insp in db.query(Inspection).all():
        if not insp.nutrition_json:
            pname = (insp.product_name or "").lower()
            if "atta" in pname or "flour" in pname or "wheat" in pname:
                insp.nutrition_json = json.dumps(atta_nutrition)
                insp.health_classification_json = json.dumps(atta_health)
            elif "oil" in pname or "ghee" in pname:
                insp.nutrition_json = json.dumps(oil_nutrition)
                insp.health_classification_json = json.dumps(oil_health)
            elif "namkeen" in pname or "snack" in pname or "chips" in pname:
                insp.nutrition_json = json.dumps(snack_nutrition)
                insp.health_classification_json = json.dumps(snack_health)
            else:
                # Default clean insufficient data / not detected state
                insp.nutrition_json = json.dumps({})
                insp.health_classification_json = json.dumps({
                    "classification": "INSUFFICIENT DATA",
                    "score": 50,
                    "badge_color": "slate",
                    "summary": "Nutritional panel not detected on the scanned package surface.",
                    "positive_factors": [],
                    "risk_factors": [],
                    "disclaimer": "AI-derived informational assessment. Not a medical diagnosis."
                })
    db.commit()

    # Seed demo inspections if empty
    if db.query(Inspection).count() == 0:
        lead_inspector = db.query(User).filter(User.username == "Soutik").first()
        if not lead_inspector:
            lead_inspector = db.query(User).first()

        # Nutrition data 1: Whole Wheat Atta
        atta_nutrition = {
            "energy": {"value": "364 kcal", "numeric_value": 364, "unit": "kcal", "per": "100g", "found": True},
            "protein": {"value": "12.1 g", "numeric_value": 12.1, "unit": "g", "per": "100g", "found": True},
            "carbohydrates": {"value": "71.2 g", "numeric_value": 71.2, "unit": "g", "per": "100g", "found": True},
            "sugars": {"value": "2.4 g", "numeric_value": 2.4, "unit": "g", "per": "100g", "found": True},
            "added_sugars": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
            "fat": {"value": "1.7 g", "numeric_value": 1.7, "unit": "g", "per": "100g", "found": True},
            "saturated_fat": {"value": "0.4 g", "numeric_value": 0.4, "unit": "g", "per": "100g", "found": True},
            "trans_fat": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
            "sodium": {"value": "5.0 mg", "numeric_value": 5.0, "unit": "mg", "per": "100g", "found": True},
            "fiber": {"value": "11.5 g", "numeric_value": 11.5, "unit": "g", "per": "100g", "found": True},
            "serving_size": {"value": "Per 100g", "found": True}
        }
        atta_health = {
            "classification": "HEALTHIER",
            "score": 92,
            "badge_color": "emerald",
            "summary": "Rich in dietary fiber and protein with low saturated fat, zero added sugar, and negligible sodium.",
            "positive_factors": [
                "High Dietary Fiber (11.5g / 100g)",
                "Good Protein Source (12.1g / 100g)",
                "Low Saturated Fat (< 1.5g / 100g)",
                "Negligible Sodium (< 120mg / 100g)"
            ],
            "risk_factors": [],
            "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
        }

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
            inspector_id=lead_inspector.id,
            inspector_name=lead_inspector.full_name,
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
            nutrition_json=json.dumps(atta_nutrition),
            health_classification_json=json.dumps(atta_health),
            raw_ocr_text="PRAMAN AGRO FOODS - WHOLE WHEAT ATTA Chakki Fresh Whole Wheat Atta Net Quantity: 5.0 kg MRP ₹ 230.00 (inclusive of all taxes) Unit Sale Price: ₹ 46.00 / kg Date of Mfg: 08/2026 Consumer Care: 1800-11-2026 care@pramanfoods.in Made in India Nutrition Facts Per 100g Energy 364 kcal Protein 12.1g Carbohydrate 71.2g Sugar 2.4g Total Fat 1.7g Saturated Fat 0.4g Sodium 5mg Dietary Fiber 11.5g",
            status="COMPLETED",
            created_at=datetime.utcnow() - timedelta(hours=2)
        )
        db.add(insp1)
        db.flush()

        # Nutrition data 2: Sunflower Oil
        oil_nutrition = {
            "energy": {"value": "900 kcal", "numeric_value": 900, "unit": "kcal", "per": "100g", "found": True},
            "protein": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
            "carbohydrates": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
            "sugars": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
            "added_sugars": {"value": None, "numeric_value": None, "unit": "g", "per": "100g", "found": False},
            "fat": {"value": "100.0 g", "numeric_value": 100.0, "unit": "g", "per": "100g", "found": True},
            "saturated_fat": {"value": "11.0 g", "numeric_value": 11.0, "unit": "g", "per": "100g", "found": True},
            "trans_fat": {"value": "0.0 g", "numeric_value": 0.0, "unit": "g", "per": "100g", "found": True},
            "sodium": {"value": "0.0 mg", "numeric_value": 0.0, "unit": "mg", "per": "100g", "found": True},
            "fiber": {"value": None, "numeric_value": None, "unit": "g", "per": "100g", "found": False},
            "serving_size": {"value": "Per 100g", "found": True}
        }
        oil_health = {
            "classification": "MODERATE",
            "score": 62,
            "badge_color": "amber",
            "summary": "100% lipid energy source with zero sugars and zero sodium. Saturated fat is within standard vegetable oil limits.",
            "positive_factors": [
                "Zero Sugar & Added Sugars",
                "Zero Sodium Content"
            ],
            "risk_factors": [
                "High Energy Density (900 kcal / 100g)",
                "High Total Fat (100g / 100g — standard for edible oil)"
            ],
            "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
        }

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
            inspector_id=lead_inspector.id,
            inspector_name=lead_inspector.full_name,
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
            nutrition_json=json.dumps(oil_nutrition),
            health_classification_json=json.dumps(oil_health),
            raw_ocr_text="SURYA SUNFLOWER OIL Refined Sunflower Oil Net Qty: 1.0 L MRP: ₹ 155.00 Unit Sale Price: ₹ 155.00 / L Pkd Date: 07/2026 Consumer Care: Contact Us at Corporate Office Made in India Nutrition Information per 100g: Energy 900kcal, Total Fat 100g, Saturated Fat 11g, Carbohydrates 0g, Protein 0g, Sodium 0mg",
            status="COMPLETED",
            created_at=datetime.utcnow() - timedelta(hours=5)
        )
        db.add(insp2)
        db.flush()

        # Nutrition data 3: Spicy Namkeen
        snack_nutrition = {
            "energy": {"value": "548 kcal", "numeric_value": 548, "unit": "kcal", "per": "100g", "found": True},
            "protein": {"value": "8.5 g", "numeric_value": 8.5, "unit": "g", "per": "100g", "found": True},
            "carbohydrates": {"value": "44.2 g", "numeric_value": 44.2, "unit": "g", "per": "100g", "found": True},
            "sugars": {"value": "4.8 g", "numeric_value": 4.8, "unit": "g", "per": "100g", "found": True},
            "added_sugars": {"value": None, "numeric_value": None, "unit": "g", "per": "100g", "found": False},
            "fat": {"value": "36.8 g", "numeric_value": 36.8, "unit": "g", "per": "100g", "found": True},
            "saturated_fat": {"value": "16.5 g", "numeric_value": 16.5, "unit": "g", "per": "100g", "found": True},
            "trans_fat": {"value": "0.1 g", "numeric_value": 0.1, "unit": "g", "per": "100g", "found": True},
            "sodium": {"value": "890.0 mg", "numeric_value": 890.0, "unit": "mg", "per": "100g", "found": True},
            "fiber": {"value": "3.2 g", "numeric_value": 3.2, "unit": "g", "per": "100g", "found": True},
            "serving_size": {"value": "Per 100g", "found": True}
        }
        snack_health = {
            "classification": "HIGH / LESS HEALTHY",
            "score": 38,
            "badge_color": "rose",
            "summary": "High in Sodium and Saturated Fat. Exceeds recommended dietary threshold limits for daily snack consumption.",
            "positive_factors": [
                "Moderate Protein (8.5g / 100g)"
            ],
            "risk_factors": [
                "High Sodium: 890mg / 100g (Threshold: > 600mg)",
                "High Saturated Fat: 16.5g / 100g (Threshold: > 5g)",
                "High Total Fat: 36.8g / 100g"
            ],
            "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
        }

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
            inspector_id=lead_inspector.id,
            inspector_name=lead_inspector.full_name,
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
            nutrition_json=json.dumps(snack_nutrition),
            health_classification_json=json.dumps(snack_health),
            raw_ocr_text="DESI CHATPATA NAMKEEN Spicy Mixture Namkeen Net Quantity: Jumbo Saver Pack Date of Packing: 08/2026 Price: Special Offer Rs 50 Unit Sale Price: Not Declared Nutritional Facts per 100g: Energy 548kcal Protein 8.5g Total Fat 36.8g Saturated Fat 16.5g Carbohydrate 44.2g Sugars 4.8g Sodium 890mg",
            status="FLAGGED",
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        db.add(insp3)
        db.commit()
        print("Sample inspection data seeded successfully.")

    db.close()

if __name__ == "__main__":
    seed_database()
