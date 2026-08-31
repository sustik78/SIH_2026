"""
PRAMAN AI - Database Models
Comprehensive Legal Metrology Inspection, Product, Rule, Result, Violation, and Audit Log models.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), default="INSPECTOR")  # ADMIN, SUPERVISOR, INSPECTOR
    badge_number = Column(String(50), nullable=True)
    department = Column(String(100), default="Legal Metrology Enforcement Wing")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    inspections = relationship("Inspection", back_populates="inspector")
    audit_logs = relationship("AuditLog", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), index=True, nullable=False)
    brand = Column(String(100), nullable=True)
    category = Column(String(100), default="General Packaged Commodity")
    manufacturer_name = Column(String(250), nullable=True)
    declared_net_qty = Column(String(50), nullable=True)
    declared_mrp = Column(String(50), nullable=True)
    barcode = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    inspections = relationship("Inspection", back_populates="product")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(String(50), unique=True, index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    inspector_name = Column(String(100), default="Designated Enforcement Officer")
    
    product_name = Column(String(200), nullable=False)
    category = Column(String(100), default="General Packaged Commodity")
    image_url = Column(String(300), nullable=False)
    annotated_image_url = Column(String(300), nullable=True)
    
    overall_score = Column(Integer, default=0)
    compliance_status = Column(String(50), default="PENDING")  # COMPLIANT, NON-COMPLIANT, PENDING REVIEW
    decision_summary = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    
    passed_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    violation_count = Column(Integer, default=0)
    critical_violations_count = Column(Integer, default=0)
    
    category_scores_json = Column(Text, nullable=True)
    raw_ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, default=0.0)
    
    status = Column(String(50), default="COMPLETED")  # COMPLETED, UNDER_REVIEW, APPROVED, FLAGGED
    supervisor_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="inspections")
    inspector = relationship("User", back_populates="inspections")
    declarations = relationship("ExtractedDeclaration", back_populates="inspection", cascade="all, delete-orphan")
    results = relationship("ComplianceResult", back_populates="inspection", cascade="all, delete-orphan")
    violations = relationship("Violation", back_populates="inspection", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="inspection", cascade="all, delete-orphan")


class ExtractedDeclaration(Base):
    __tablename__ = "extracted_declarations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    field_name = Column(String(100), nullable=False)
    detected_value = Column(Text, nullable=True)
    is_found = Column(Boolean, default=False)
    confidence_score = Column(Float, default=0.0)
    bbox_json = Column(Text, nullable=True)

    inspection = relationship("Inspection", back_populates="declarations")


class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    rule_id = Column(String(50), index=True, nullable=False)
    rule_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    requirement = Column(Text, nullable=False)
    detected_value = Column(Text, nullable=True)
    expected_condition = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)  # PASS, WARNING, VIOLATION, MANUAL_VERIFICATION_REQUIRED
    severity = Column(String(50), default="NONE")  # NONE, LOW, MEDIUM, HIGH, CRITICAL
    explanation = Column(Text, nullable=False)
    source_document = Column(String(200), nullable=False)
    source_section = Column(String(200), nullable=False)
    crop_url = Column(String(300), nullable=True)
    bbox_json = Column(Text, nullable=True)

    inspection = relationship("Inspection", back_populates="results")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    rule_id = Column(String(50), nullable=False)
    violation_title = Column(String(200), nullable=False)
    severity = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    legal_basis = Column(String(250), nullable=False)
    evidence_crop_url = Column(String(300), nullable=True)
    detected_value = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    inspection = relationship("Inspection", back_populates="violations")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    username = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)  # LOGIN, PRODUCT_SCANNED, REPORT_GENERATED, STATUS_CHANGED
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(100), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    report_number = Column(String(100), unique=True, nullable=False)
    file_path = Column(String(300), nullable=False)
    file_format = Column(String(20), default="PDF")  # PDF, DOCX
    generated_by = Column(String(100), default="Enforcement Officer")
    generated_at = Column(DateTime, default=datetime.utcnow)

    inspection = relationship("Inspection", back_populates="reports")
