"""
PRAMAN AI - Technical & Hackathon Evaluation Dossier Generator
Produces a comprehensive, professional, multi-page PDF document covering Parts 1 through 28.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Polygon

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Cover page decorative border
            self.saveState()
            self.setStrokeColor(colors.HexColor("#0B1B33"))
            self.setLineWidth(4)
            self.rect(20, 20, 572, 752)
            self.setStrokeColor(colors.HexColor("#3B82F6"))
            self.setLineWidth(1)
            self.rect(25, 25, 562, 742)
            self.restoreState()
            return

        self.saveState()
        # Header
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(36, 760, "PRAMAN AI — Technical & Hackathon Evaluation Dossier")
        self.drawRightString(576, 760, "SIH 2026 • Legal Metrology AI Platform")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 754, 576, 754)

        # Footer
        self.line(36, 42, 576, 42)
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(36, 31, "GOVERNMENT ENFORCEMENT & TECHNICAL AUDIT SYSTEM")
        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(576, 31, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom Typography & Styling Tokens
    c_primary = colors.HexColor("#0B1B33")
    c_secondary = colors.HexColor("#1E40AF")
    c_accent = colors.HexColor("#2563EB")
    c_text_dark = colors.HexColor("#0F172A")
    c_text_muted = colors.HexColor("#475569")
    c_bg_light = colors.HexColor("#F8FAFC")
    c_bg_callout = colors.HexColor("#EFF6FF")
    c_border = colors.HexColor("#CBD5E1")

    # Paragraph Styles
    cover_title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#0B1B33"),
        alignment=1
    )
    cover_sub_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E40AF"),
        alignment=1
    )
    cover_tag_style = ParagraphStyle(
        "CoverTag",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#047857"),
        alignment=1
    )
    part_heading_style = ParagraphStyle(
        "PartHeading",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0B1B33"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    section_heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    sub_section_heading_style = ParagraphStyle(
        "SubSectionHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=c_text_dark,
        spaceAfter=3
    )
    body_bold = ParagraphStyle(
        "BodyBoldCustom",
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    body_muted = ParagraphStyle(
        "BodyMutedCustom",
        parent=body_style,
        fontSize=7.5,
        leading=9.5,
        textColor=c_text_muted
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=c_text_dark
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#0B1B33")
    )
    table_cell_header = ParagraphStyle(
        "TableHeader",
        parent=table_cell,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )
    q_title_style = ParagraphStyle(
        "QTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E3A8A")
    )
    q_why_style = ParagraphStyle(
        "QWhy",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#475569")
    )
    q_ans_style = ParagraphStyle(
        "QAns",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=c_text_dark
    )
    q_key_style = ParagraphStyle(
        "QKey",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#065F46")
    )

    story = []

    def add_callout(title, text, bg_color="#F0FDF4", border_color="#10B981", title_color="#047857"):
        content = [
            [Paragraph(f"<b>{title}</b>", ParagraphStyle("CTitle", parent=body_style, fontName="Helvetica-Bold", fontSize=8, textColor=colors.HexColor(title_color)))],
            [Paragraph(text, ParagraphStyle("CText", parent=body_style, fontSize=7.5, leading=9.5))]
        ]
        t = Table(content, colWidths=[540])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg_color)),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(border_color)),
            ("INNERGRID", (0, 0), (-1, -1), 0, colors.transparent),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    def add_part_header(part_num, title, tagline=""):
        story.append(Paragraph(f"PART {part_num} — {title.upper()}", part_heading_style))
        if tagline:
            story.append(Paragraph(f"<i>{tagline}</i>", body_muted))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E40AF"), spaceBefore=2, spaceAfter=6))

    def create_qa_card(q_num, category, question, why_asking, strong_answer, key_points):
        qa_data = [
            [Paragraph(f"<b>[{category}] Q{q_num}: {question}</b>", q_title_style)],
            [Paragraph(f"<b>Why the Evaluator Asks This:</b> {why_asking}", q_why_style)],
            [Paragraph(f"<b>Technical Answer:</b> {strong_answer}", q_ans_style)],
            [Paragraph(f"<b>Key Defense Takeaway:</b> {key_points}", q_key_style)]
        ]
        t = Table(qa_data, colWidths=[540])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
            ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#93C5FD")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EFF6FF")),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        return KeepTogether([t, Spacer(1, 4)])

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("MINISTRY OF CONSUMER AFFAIRS, FOOD & PUBLIC DISTRIBUTION", cover_sub_style))
    story.append(Paragraph("GOVERNMENT OF INDIA • LEGAL METROLOGY DIVISION", ParagraphStyle("GovSub", parent=cover_sub_style, fontSize=10, textColor=colors.HexColor("#64748B"))))
    story.append(Spacer(1, 20))
    story.append(Paragraph("PRAMAN AI", cover_title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Packaging Regulations & Automated Metrology Audit Network</b>", cover_sub_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>\"From Package Image to Explainable Compliance Decision\"</i>", cover_tag_style))
    story.append(Spacer(1, 24))

    dossier_meta_box = [
        [Paragraph("<b>DOCUMENT CLASSIFICATION</b>", table_cell_header), Paragraph("<b>TECHNICAL EVALUATION DOSSIER</b>", table_cell_header)],
        [Paragraph("<b>Target Event / Review:</b>", table_cell_bold), Paragraph("Smart India Hackathon (SIH 2026) / Statutory Evaluator Review", table_cell)],
        [Paragraph("<b>Statutory Ground Truth:</b>", table_cell_bold), Paragraph("Legal Metrology Act, 2009 & Packaged Commodities Rules, 2011 (40 Official Gazettes)", table_cell)],
        [Paragraph("<b>System Core:</b>", table_cell_bold), Paragraph("Computer Vision (OpenCV) + Tesseract OCR + Deterministic Legal Rule Engine", table_cell)],
        [Paragraph("<b>Report Capabilities:</b>", table_cell_bold), Paragraph("Official Court-Ready PDF (ReportLab) & Editable Word Notice (DOCX)", table_cell)],
        [Paragraph("<b>Security & Roles:</b>", table_cell_bold), Paragraph("RBAC (ADMIN, SUPERVISOR, INSPECTOR) + SHA-256 JWT + Immutable Audit Logs", table_cell)],
        [Paragraph("<b>Accessibility:</b>", table_cell_bold), Paragraph("Senior Mode, High Contrast Mode, Speech Synthesis Audio Guidance", table_cell)],
        [Paragraph("<b>Audited Codebase:</b>", table_cell_bold), Paragraph("100% Verified FastAPI Backend + React 18 / Tailwind Frontend + SQLite DB", table_cell)],
        [Paragraph("<b>Status:</b>", table_cell_bold), Paragraph("Fully Functional Prototype with Live Pipeline & Curated Statutory Benchmarks", table_cell)]
    ]
    t_cov = Table(dossier_meta_box, colWidths=[150, 390])
    t_cov.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#1E3A8A")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cov)
    story.append(Spacer(1, 24))

    story.append(Paragraph("<b>AUTHORS & ENFORCEMENT PROJECT TEAM:</b>", ParagraphStyle("AuthH", parent=body_style, fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#0B1B33"))))
    story.append(Paragraph("Apex Command & Enforcement Lead: <b>Soutik</b> (LM-ADM-001) | Review Supervisor: <b>Sayantan</b> (LM-SUP-102)<br/>Audit Inspector: <b>Jiya</b> (LM-INS-203) | Central Admin: <b>Rimi</b> (LM-ADM-004)<br/>Senior Supervisor: <b>Debopriya</b> (LM-SUP-105) | Vigilance Inspector: <b>Arkadip</b> (LM-INS-206)", body_muted))
    story.append(Spacer(1, 20))

    add_callout(
        "CONFIDENTIAL & AUTHORITATIVE PREPARATION GUIDE",
        "This dossier contains the complete architectural, algorithmic, regulatory, and defensive knowledge base for PRAMAN AI. All data, logic, rules, and evaluator Q&As match the actual verified implementation of the system.",
        bg_color="#EFF6FF", border_color="#3B82F6", title_color="#1E40AF"
    )

    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS / SITEMAP
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS & SITEMAP", part_heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E40AF"), spaceBefore=2, spaceAfter=8))

    toc_items = [
        ("Part 1", "Understand the Entire Project & Verification Matrix", "Implementation audit distinguishing Dynamic, Rule-based, AI, and Mock items"),
        ("Part 2", "Project Executive Summary & Pitches", "30-sec, 1-min, 2-min, and 5-min presentation-ready explanations"),
        ("Part 3", "Problem Statement & Solution Matrix", "Deep analysis of manual packaging inspection vs PRAMAN AI automation"),
        ("Part 4", "Complete System Workflow", "End-to-end 15-step execution pipeline from login to report generation"),
        ("Part 5", "Professional Workflow Diagram", "Visual flowchart of data transformations and inspector touchpoints"),
        ("Part 6", "System Architecture & Diagram", "Multi-tier architecture breakdown: Frontend, API, AI/OCR, Engine, DB, Reports"),
        ("Part 7", "Every Major Feature (1–24)", "Deep-dive into all 24 UI/Backend modules with inputs, outputs, logic, and limitations"),
        ("Part 8", "AI / Computer Vision / OCR Deep Dive", "OpenCV CLAHE, Tesseract 5.4, character confidence, and edge-case handling"),
        ("Part 9", "Legal Metrology / Compliance Logic", "Detailed breakdown of the 12 Statutory Rule Groups indexed from 40 Gazettes"),
        ("Part 10", "Nutritional Values & Health Classification", "Nutrition facts extraction, FSSAI/ICMR health indicator, and legal distinction"),
        ("Part 11", "Visual Evidence & Bounding Boxes", "Image-to-rule traceability, color overlays (Pass/Warn/Violate), crop cards"),
        ("Part 12", "Report Generation Engine", "Official Court-Ready PDF (ReportLab) & Editable DOCX (python-docx) generators"),
        ("Part 13", "User Roles & Permissions (RBAC)", "Role definitions (Admin, Supervisor, Inspector), badge numbers, access limits"),
        ("Part 14", "Complete Data Flow", "Data models, state transitions, JSON payloads, and storage schemas"),
        ("Part 15", "Technology Stack & Tool Justifications", "FastAPI, React 18, OpenCV, Tesseract, ReportLab, SQLite/PostgreSQL"),
        ("Part 16", "Technical Design Decisions", "Architectural trade-offs: Deterministic Rules vs LLM, Local OCR vs Cloud APIs"),
        ("Part 17", "Brutally Honest Limitations", "Current edge cases, image skew limits, multi-surface packages, regional fonts"),
        ("Part 18", "Security Architecture", "Authentication, password hashing, session tokens, audit trail, production roadmap"),
        ("Part 19", "Scalability Roadmap", "Horizontal scaling, Celery queues, PostgreSQL sharding, cloud OCR clusters"),
        ("Part 20", "Real-World Government Deployment", "NIC/e-Governance integration, handheld enforcement devices, offline edge sync"),
        ("Part 21", "Hackathon Evaluator Questions (A–AL)", "Exhaustive category-by-category defense questions with strong technical answers"),
        ("Part 22", "Hard Technical Questions & Traps", "Adversarial questions, OCR failures, legal conflict resolution, mathematical proofs"),
        ("Part 23", "Demo Questions & Live Interruptions", "Questions asked during live demonstration and step-by-step inspector responses"),
        ("Part 24", "Perfect Demo Walkthrough Script", "Click-by-click, say-by-say presentation script for winning the evaluation"),
        ("Part 25", "Elevator Pitches (5 Variants)", "30s, 1m, 2m, Problem-first, and Innovation-first pitch scripts"),
        ("Part 26", "Explain It to a Professor", "Systems engineering, computer vision, deterministic logic, and software design review"),
        ("Part 27", "Quick Revision Cheat Sheet", "Summary cards, key statistics, penalty sections, and statutory definitions"),
        ("Part 28", "Questions We Must Be Able to Answer", "Internal team readiness checklist before facing the judging panel")
    ]

    toc_table_data = [[Paragraph("<b>Part</b>", table_cell_header), Paragraph("<b>Dossier Section</b>", table_cell_header), Paragraph("<b>Key Scope & Content</b>", table_cell_header)]]
    for p_num, p_title, p_desc in toc_items:
        toc_table_data.append([
            Paragraph(f"<b>{p_num}</b>", table_cell_bold),
            Paragraph(f"<b>{p_title}</b>", table_cell),
            Paragraph(p_desc, table_cell)
        ])

    t_toc = Table(toc_table_data, colWidths=[50, 210, 280])
    t_toc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PART 1: UNDERSTAND THE ENTIRE PROJECT & VERIFICATION MATRIX
    # =========================================================================
    add_part_header("1", "Understand the Entire Project & Verification Matrix", "Ground-truth technical status of all system components verified against the codebase.")
    
    story.append(Paragraph("To ensure 100% academic integrity and factual defensibility during evaluation, every feature in PRAMAN AI has been audited to determine its exact architectural nature. Nothing is fabricated or claimed beyond actual code reality.", body_style))
    story.append(Spacer(1, 4))

    status_matrix = [
        [Paragraph("<b>Component / Feature</b>", table_cell_header), Paragraph("<b>Implementation Nature</b>", table_cell_header), Paragraph("<b>Backend / Engine Driver</b>", table_cell_header), Paragraph("<b>Verification Status</b>", table_cell_header)],
        [
            Paragraph("<b>Image Upload & Samples</b>", table_cell_bold),
            Paragraph("Actually Implemented (Dynamic + Curated Samples)", table_cell),
            Paragraph("FastAPI <code>/api/scan/upload</code> + disk storage", table_cell),
            Paragraph("100% Verified in <code>scan_routes.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Image Preprocessing</b>", table_cell_bold),
            Paragraph("Actually Implemented (Computer Vision)", table_cell),
            Paragraph("OpenCV CLAHE, bilateralFilter, Hough skew detection", table_cell),
            Paragraph("100% Verified in <code>preprocessor.py</code>", table_cell)
        ],
        [
            Paragraph("<b>OCR & Word Bounding Boxes</b>", table_cell_bold),
            Paragraph("Actually Implemented (AI/OCR Engine)", table_cell),
            Paragraph("Tesseract 5.4.0 via <code>pytesseract.image_to_data</code>", table_cell),
            Paragraph("100% Verified in <code>ocr_engine.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Declaration Extraction</b>", table_cell_bold),
            Paragraph("Actually Implemented (Deterministic NLP/Regex)", table_cell),
            Paragraph("9 specialized regex parsers with line grouping", table_cell),
            Paragraph("100% Verified in <code>declaration_extractor.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Nutritional Information</b>", table_cell_bold),
            Paragraph("Actually Implemented (Nutrient Parser)", table_cell),
            Paragraph("Parses 11 nutrient fields (Energy, Protein, Sugars, etc.)", table_cell),
            Paragraph("100% Verified in <code>declaration_extractor.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Health Classification</b>", table_cell_bold),
            Paragraph("Actually Implemented (Rule-Based Classifier)", table_cell),
            Paragraph("FSSAI/ICMR threshold evaluation (Sodium, Fat, Sugar)", table_cell),
            Paragraph("100% Verified in <code>nutrition_classifier.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Compliance Rule Engine</b>", table_cell_bold),
            Paragraph("Actually Implemented (Deterministic Rules)", table_cell),
            Paragraph("12 Statutory Rule Groups from 40 Official Gazettes", table_cell),
            Paragraph("100% Verified in <code>engine.py</code> & <code>rule_definitions.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Explainable Scoring (0-100)</b>", table_cell_bold),
            Paragraph("Actually Implemented (Weighted Scorer)", table_cell),
            Paragraph("5 weighted categories (Completeness 40%, Units 25%, etc.)", table_cell),
            Paragraph("100% Verified in <code>scoring.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Visual Evidence Bounding Boxes</b>", table_cell_bold),
            Paragraph("Actually Implemented (Computer Vision)", table_cell),
            Paragraph("OpenCV rectangle rendering + UUID crop generation", table_cell),
            Paragraph("100% Verified in <code>visual_evidence.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Official PDF Report</b>", table_cell_bold),
            Paragraph("Actually Implemented (Document Engine)", table_cell),
            Paragraph("ReportLab Platypus PDF with GoI banner & signature box", table_cell),
            Paragraph("100% Verified in <code>pdf_report.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Editable DOCX Report</b>", table_cell_bold),
            Paragraph("Actually Implemented (Document Engine)", table_cell),
            Paragraph("python-docx generator with formatted statutory notice", table_cell),
            Paragraph("100% Verified in <code>docx_report.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Authentication & RBAC</b>", table_cell_bold),
            Paragraph("Actually Implemented (JWT + Salted SHA-256)", table_cell),
            Paragraph("6 authorized official users (Admin, Supervisor, Inspector)", table_cell),
            Paragraph("100% Verified in <code>auth.py</code> & <code>auth_routes.py</code>", table_cell)
        ],
        [
            Paragraph("<b>Remembered Login & Fast-Switch</b>", table_cell_bold),
            Paragraph("Actually Implemented (Frontend + Storage)", table_cell),
            Paragraph("LocalStorage persistence + 1-click role switcher", table_cell),
            Paragraph("100% Verified in <code>AuthContext.jsx</code>", table_cell)
        ],
        [
            Paragraph("<b>Accessibility (Senior/Speech)</b>", table_cell_bold),
            Paragraph("Actually Implemented (Browser Web APIs)", table_cell),
            Paragraph("Web Speech Synthesis API + CSS high-contrast filters", table_cell),
            Paragraph("100% Verified in <code>AccessibilityContext.jsx</code>", table_cell)
        ],
        [
            Paragraph("<b>Immutable Audit Logging</b>", table_cell_bold),
            Paragraph("Actually Implemented (Database-Backed)", table_cell),
            Paragraph("SQLAlchemy <code>AuditLog</code> recording all inspections/logins", table_cell),
            Paragraph("100% Verified in <code>models.py</code> & <code>report_routes.py</code>", table_cell)
        ],
        [
            Paragraph("<b>40 Gazette Rule Library</b>", table_cell_bold),
            Paragraph("Actually Implemented (Dataset Index)", table_cell),
            Paragraph("40 PDF gazettes in <code>Government_Gazette_Dataset</code>", table_cell),
            Paragraph("100% Verified on filesystem & UI", table_cell)
        ],
        [
            Paragraph("<b>Live Camera Capture</b>", table_cell_bold),
            Paragraph("Partially Implemented / File-upload primary", table_cell),
            Paragraph("Frontend file picker supports direct image file upload", table_cell),
            Paragraph("Live WebRTC stream is planned for mobile build", table_cell)
        ],
        [
            Paragraph("<b>Regional OCR (Hindi/Tamil)</b>", table_cell_bold),
            Paragraph("Partially Implemented (Tesseract multi-lang ready)", table_cell),
            Paragraph("English dataset primary; Hindi OCR trained in Tesseract", table_cell),
            Paragraph("Indic-OCR pipeline documented in Scalability", table_cell)
        ]
    ]

    t_mat = Table(status_matrix, colWidths=[110, 130, 170, 130])
    t_mat.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 2: PROJECT EXECUTIVE SUMMARY & PITCHES
    # =========================================================================
    add_part_header("2", "Project Executive Summary & Pitches", "High-impact summaries tailored for 30-second to 5-minute evaluator evaluations.")

    story.append(Paragraph("<b>What is PRAMAN AI?</b><br/><b>PRAMAN AI</b> (<i>Packaging Regulations & Automated Metrology Audit Network</i>) is an AI-powered Legal Metrology compliance inspection platform designed specifically for government enforcement officers, legal metrology inspectors, and regional supervisors in India.", body_style))
    story.append(Paragraph("<b>What Problem Does it Solve?</b><br/>Pre-packaged commodities sold across India must strictly declare mandatory consumer safeguards under the Legal Metrology Act, 2009 and Packaged Commodities Rules (PCR), 2011. Manual inspection in wholesale markets and retail stores is slow (15–20 minutes per package), error-prone, highly subjective, lacks evidence preservation, and overwhelms field officers. PRAMAN AI automates the entire inspection in under 3 seconds.", body_style))
    story.append(Paragraph("<b>Who are the Intended Users?</b><br/>1. Field Enforcement Inspectors (on-site store audits), 2. Review Supervisors (approvals and notice issuance), 3. Central Ministry Administrators (state-wide compliance analytics and policy oversight).", body_style))
    story.append(Paragraph("<b>What is the Main Innovation?</b><br/>Unlike generic black-box vision models or hallucination-prone Large Language Models, PRAMAN AI pairs <b>Computer Vision OCR</b> with a <b>Deterministic Legal Rule Engine</b> derived directly from 40 Official Government Gazettes. Every pass or violation is mathematically proven, tied to exact statutory clauses (e.g., Rule 6(1)(c), GSR 226(E)), and accompanied by cropped visual evidence snippets.", body_style))
    story.append(Spacer(1, 4))

    # Pitches Table
    pitches = [
        ("30-Second Elevator Pitch", "PRAMAN AI transforms Legal Metrology enforcement in India from a slow, manual 20-minute paperwork process into a 3-second automated audit. An enforcement officer snaps a photo of any packaged commodity; our Computer Vision and Deterministic Rule Engine extracts declarations, checks compliance against 40 Official Gazettes, flags violations with visual bounding boxes, and generates court-ready statutory inspection notices in PDF and editable Word formats."),
        ("1-Minute Standard Pitch", "In India, over 100 million pre-packaged commodities are sold daily, yet Legal Metrology enforcement relies on manual inspections. Officers struggle with complex amendments like Unit Sale Price rules, metric quantity standards, and tax clauses. PRAMAN AI solves this by automating label compliance. When an image is uploaded, OpenCV enhances the label, Tesseract extracts text bounding boxes, and our deterministic rule engine evaluates 12 statutory rule groups derived from official gazettes. It scores the package from 0 to 100, detects infractions such as misleading 'Jumbo' quantities or missing helpline emails, crops visual evidence cards, and exports official statutory notices instantly. It also includes senior-friendly accessibility and immutable audit logging."),
        ("2-Minute Technical Pitch", "PRAMAN AI is architected with a decoupled FastAPI backend and React frontend. The pipeline begins with OpenCV preprocessing—applying CLAHE for uneven lighting, bilateral filtering for noise reduction, and Hough transform skew correction. Tesseract 5.4 extracts word-level bounding boxes and confidence scores. Next, our deterministic declaration extractor parses mandatory fields—Commodity Name, Manufacturer Address with Pincode, Metric Net Quantity, MRP with tax clauses, Unit Sale Price, and Consumer Care details. In parallel, it extracts 11 nutritional facts and derives an informational health classification. The compliance engine evaluates 12 statutory rule groups derived from 40 indexed gazette PDFs, computing a weighted 0–100 score across 5 categories. High-visibility bounding boxes are rendered directly on the package, and ReportLab and python-docx engines generate official notices with digital signatures and audit logs."),
        ("5-Minute Technical Deep-Dive", "PRAMAN AI addresses the core bottleneck of statutory enforcement: the need for absolute legal determinism without AI hallucination. Large Language Models cannot be used for court prosecution because their non-deterministic nature introduces hallucinations. PRAMAN AI deliberately uses a hybrid pipeline: AI for Computer Vision and OCR (perceptual task), coupled with a deterministic statutory rule engine (symbolic reasoning). The architecture uses SQLite/PostgreSQL with SQLAlchemy ORM, FastAPI REST endpoints, and JWT authentication with Role-Based Access Control. If an image has poor contrast, OpenCV calculates brightness and contrast standard deviations, dynamically triggering legibility warnings under Rule 7 and 9. The system validates unit conversions—ensuring USP equals MRP divided by net quantity per GSR 226(E). If a product is non-compliant, Section 36(1) show-cause notice recommendations are generated automatically, complete with high-resolution evidence snippets.")
    ]

    for p_title, p_body in pitches:
        story.append(Paragraph(f"<b>{p_title}</b>", section_heading_style))
        story.append(Paragraph(p_body, body_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # PART 3: PROBLEM STATEMENT & COMPARISON MATRIX
    # =========================================================================
    add_part_header("3", "Problem Statement & Solution Matrix", "Comprehensive comparison between manual packaging inspection and PRAMAN AI automation.")

    story.append(Paragraph("The Legal Metrology (Packaged Commodities) Rules, 2011 mandate at least 9 distinct declarations on every consumer package. In practice, manual enforcement suffers from severe systemic limitations:", body_style))
    story.append(Spacer(1, 4))

    prob_sol_data = [
        [Paragraph("<b>Manual Inspection Problem</b>", table_cell_header), Paragraph("<b>Root Cause & Operational Impact</b>", table_cell_header), Paragraph("<b>PRAMAN AI Automated Solution</b>", table_cell_header)],
        [
            Paragraph("<b>Extreme Time Consumption</b>", table_cell_bold),
            Paragraph("Takes 15–20 minutes per package to verify 9 declarations, cross-reference gazettes, and hand-write inspection memos.", table_cell),
            Paragraph("<b>3-Second End-to-End Audit:</b> Instant OpenCV/Tesseract extraction and automated rule evaluation.", table_cell)
        ],
        [
            Paragraph("<b>Human Error & Fatigue</b>", table_cell_bold),
            Paragraph("Inspectors easily miss micro-lettering, missing 'inclusive of all taxes' clauses, or subtle non-metric units ('gms' vs 'g').", table_cell),
            Paragraph("<b>100% Deterministic Verification:</b> Regex and NLP algorithms strictly validate metric symbols and statutory tax clauses.", table_cell)
        ],
        [
            Paragraph("<b>Regulatory Complexity</b>", table_cell_bold),
            Paragraph("Over 40 gazette amendments exist (e.g., GSR 226(E) for Unit Sale Price, 2022 Garment Rules, 2023 QR Code proviso). Officers cannot recall all amendments.", table_cell),
            Paragraph("<b>Automated Gazette Ground-Truth:</b> 12 rule groups continuously reflect the 40 indexed gazette PDFs.", table_cell)
        ],
        [
            Paragraph("<b>Lack of Visual Evidence</b>", table_cell_bold),
            Paragraph("Officers take manual mobile photos that lack coordinate mapping, making evidence contestable in consumer courts.", table_cell),
            Paragraph("<b>Color-Coded Bounding Overlays:</b> Auto-generated high-resolution cropped evidence cards tied to exact violation coordinates.", table_cell)
        ],
        [
            Paragraph("<b>Subjective Compliance Decisions</b>", table_cell_bold),
            Paragraph("Different inspectors apply different penalties for identical infractions, leading to accusations of bias.", table_cell),
            Paragraph("<b>Standardized 0–100 Score:</b> Explainable, weighted scoring across 5 distinct regulatory categories.", table_cell)
        ],
        [
            Paragraph("<b>Paperwork & Notice Delays</b>", table_cell_bold),
            Paragraph("Typing formal Show-Cause notices under Section 36(1) takes days, delaying legal prosecution.", table_cell),
            Paragraph("<b>1-Click Official Reports:</b> Instant court-ready PDF and editable Word (DOCX) notice generation.", table_cell)
        ],
        [
            Paragraph("<b>Audit Trail & Tampering</b>", table_cell_bold),
            Paragraph("Physical inspection logs are susceptible to loss, unauthorized changes, or lack of supervisory oversight.", table_cell),
            Paragraph("<b>Immutable Audit Logging:</b> Every scan, review, and supervisor note is timestamped and recorded in SQL.", table_cell)
        ]
    ]

    t_ps = Table(prob_sol_data, colWidths=[120, 200, 220])
    t_ps.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ps)
    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 4: COMPLETE SYSTEM WORKFLOW
    # =========================================================================
    add_part_header("4", "Complete System Workflow", "Step-by-step execution pipeline from authentication to report export.")

    workflow_steps = [
        ("Step 1: Secure Enforcement Login", "Officer authenticates using badge credentials or one-click role switcher. System validates JWT access token and assigns role permissions (ADMIN, SUPERVISOR, INSPECTOR). An immutable login event is appended to the Audit Trail."),
        ("Step 2: Executive Dashboard Overview", "Officer reviews state-wide compliance statistics, compliance rate gauge (e.g. 66.7%), top violations breakdown, category distribution, and recent inspection activity feed."),
        ("Step 3: Scan Packaging Studio Initiation", "Officer navigates to Scan Studio. Selects either direct camera/file image upload or loads one of the 3 SIH curated statutory demo packages (Atta - Compliant, Sunflower Oil - Non-Compliant, Namkeen - Critical Violation)."),
        ("Step 4: Image Ingestion & Disk Storage", "FastAPI backend ingests the image file, assigns a unique Inspection ID (`PRM-YYYYMMDD-XXXXXX`), and stores the raw image in the backend upload repository."),
        ("Step 5: OpenCV Computer Vision Preprocessing", "ImagePreprocessor loads the image matrix. Converts to grayscale, calculates mean brightness and contrast STD. Applies CLAHE (clipLimit=2.0) for adaptive contrast equalization, bilateral denoising to preserve crisp text edges, and Canny/Hough transform skew correction."),
        ("Step 6: Tesseract 5.4 OCR & Bounding Box Extraction", "OCREngine runs Tesseract with `image_to_data`, extracting word-level text, coordinates (x, y, w, h), line groupings, block numbers, and character confidence scores. Generates aggregated lines with spatial coordinates."),
        ("Step 7: Mandatory Declaration Extraction (Deterministic NLP)", "DeclarationExtractor runs 9 specialized regex and linguistic parsers across the OCR lines to extract: Commodity Name, Manufacturer/Packer Address with Pincode, Metric Net Quantity, Manufacturing Date, MRP with Tax Clause, Unit Sale Price (USP), Consumer Care Helpline/Email, Country of Origin, and Garment Sizes."),
        ("Step 8: Nutritional Facts & Informational Health Assessment", "Nutrient parser extracts Energy, Protein, Carbohydrates, Sugars, Added Sugars, Total Fat, Saturated Fat, Trans Fat, Sodium/Salt, and Dietary Fiber. NutritionClassifier evaluates values against FSSAI/ICMR public health thresholds to produce an informational health indicator (HEALTHIER, MODERATE, or LESS HEALTHY)."),
        ("Step 9: Deterministic Legal Metrology Rule Engine", "ComplianceRuleEngine executes 12 statutory rule evaluations derived from the 40 indexed gazette PDFs. Evaluates address completeness, metric unit legality (Rule 11-13), tax clause presence (Rule 6(1)(e)), mathematical USP accuracy (GSR 226(E)), and QR code proviso compliance."),
        ("Step 10: Explainable Compliance Scoring (0–100)", "ComplianceScorer computes weighted scores across 5 categories: Declaration Completeness (40%), Value & Unit Validation (25%), Price & USP Consistency (15%), Consumer Redressal & Origin (10%), and Display Legibility (10%). Formulates regulatory status (COMPLIANT, NON-COMPLIANT, PENDING REVIEW) and statutory recommendations under Section 36(1)."),
        ("Step 11: Visual Evidence & Overlay Generation", "VisualEvidenceGenerator draws color-coded bounding boxes on the packaging image: Green (PASS), Amber (WARNING), Red (VIOLATION). Crops localized high-resolution evidence snippets for each infraction and saves annotated images."),
        ("Step 12: Database Persistence", "SQLAlchemy session creates or updates the Product entity, creates the primary Inspection record, and inserts individual records into ExtractedDeclarations, ComplianceResults, Violations, and AuditLogs."),
        ("Step 13: Interactive UI Audit Studio", "Frontend displays the Score Gauge, Interactive Visual Evidence Viewer, Declarations Audit table with confidence bars, Nutritional Profile card, and Rule Citations."),
        ("Step 14: Supervisory Review & Action Workflow", "Supervisor or Admin can add supervisory notes and update the official inspection state (COMPLETED, APPROVED, UNDER_REVIEW, FLAGGED)."),
        ("Step 15: Official PDF & DOCX Export", "Officer clicks 'Download Official PDF' or 'Export DOCX'. ReportLab / python-docx dynamically generates official Government of India formatted notices complete with metadata, violation tables, and signature endorsement blocks.")
    ]

    for s_title, s_desc in workflow_steps:
        story.append(Paragraph(f"<b>{s_title}</b>", sub_section_heading_style))
        story.append(Paragraph(s_desc, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PART 5: PROFESSIONAL WORKFLOW DIAGRAM
    # =========================================================================
    add_part_header("5", "Professional Workflow Diagram", "Visual flowchart of PRAMAN AI end-to-end data pipeline and inspector touchpoints.")

    story.append(Paragraph("The following structural diagram visualizes the end-to-end PRAMAN AI pipeline, highlighting data transformations and human-in-the-loop inspector decision points:", body_style))
    story.append(Spacer(1, 4))

    # Diagram Table Representation
    diag_flow = [
        [Paragraph("<b>PIPELINE STAGE</b>", table_cell_header), Paragraph("<b>TRANSFORMATION & ARTIFACTS</b>", table_cell_header), Paragraph("<b>ACTOR / INTERACTION</b>", table_cell_header)],
        [
            Paragraph("<b>1. INGESTION</b>", table_cell_bold),
            Paragraph("Package Image Upload / Demo Scenario Selection &rarr; Disk Ingestion & ID Allocation (<code>PRM-...</code>)", table_cell),
            Paragraph("Enforcement Inspector (Field / Studio)", table_cell)
        ],
        [
            Paragraph("<b>2. COMPUTER VISION</b>", table_cell_bold),
            Paragraph("OpenCV CLAHE Histogram Equalization + Bilateral Filtering + Hough Transform Deskewing", table_cell),
            Paragraph("Automated Pipeline (preprocessor.py)", table_cell)
        ],
        [
            Paragraph("<b>3. AI OCR ENGINE</b>", table_cell_bold),
            Paragraph("Tesseract 5.4.0 Engine &rarr; Raw Text Stream + Word Bounding Box Coordinates + Character Confidence", table_cell),
            Paragraph("Automated Pipeline (ocr_engine.py)", table_cell)
        ],
        [
            Paragraph("<b>4. INFORMATION EXTRACTION</b>", table_cell_bold),
            Paragraph("Deterministic NLP & Regex Parsers &rarr; Structured Declarations (Mfr, Qty, MRP, USP, Date, Helpline) + Nutrition Facts", table_cell),
            Paragraph("Automated Pipeline (declaration_extractor.py)", table_cell)
        ],
        [
            Paragraph("<b>5. RULE VALIDATION</b>", table_cell_bold),
            Paragraph("Deterministic Legal Engine (12 Rules from 40 Gazettes) + FSSAI/ICMR Health Classification", table_cell),
            Paragraph("Automated Pipeline (engine.py & nutrition_classifier.py)", table_cell)
        ],
        [
            Paragraph("<b>6. COMPLIANCE DECISION</b>", table_cell_bold),
            Paragraph("Explainable Weighted Scoring (0–100) &rarr; Status Decision (COMPLIANT, NON-COMPLIANT, PENDING REVIEW)", table_cell),
            Paragraph("Automated Pipeline (scoring.py)", table_cell)
        ],
        [
            Paragraph("<b>7. VISUAL EVIDENCE</b>", table_cell_bold),
            Paragraph("OpenCV Bounding Box Overlay (Green/Amber/Red) + Cropped Evidence Snippet Card Generation", table_cell),
            Paragraph("Automated Pipeline (visual_evidence.py)", table_cell)
        ],
        [
            Paragraph("<b>8. INSPECTION DETAIL UI</b>", table_cell_bold),
            Paragraph("Interactive Score Gauge, 6-Tab Audit Studio, Bounding Box Inspector, Audio Guidance", table_cell),
            Paragraph("Inspector / Supervisor (Interactive Review)", table_cell)
        ],
        [
            Paragraph("<b>9. SUPERVISORY WORKFLOW</b>", table_cell_bold),
            Paragraph("Supervisory Review Notes + Status Transition (APPROVED / FLAGGED / UNDER_REVIEW)", table_cell),
            Paragraph("Review Supervisor / Admin", table_cell)
        ],
        [
            Paragraph("<b>10. STATUTORY EXPORT</b>", table_cell_bold),
            Paragraph("ReportLab Court-Ready PDF Notice + python-docx Editable Word Notice + Immutable Audit Log", table_cell),
            Paragraph("Enforcement Officer / Legal Wing", table_cell)
        ]
    ]

    t_wf = Table(diag_flow, colWidths=[110, 280, 150])
    t_wf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 6: SYSTEM ARCHITECTURE & DIAGRAM
    # =========================================================================
    add_part_header("6", "System Architecture & Diagram", "Technical breakdown of frontend, API gateway, computer vision, rule engine, storage, and report layers.")

    story.append(Paragraph("PRAMAN AI follows a clean, decoupled, multi-tier architecture designed for high throughput, sub-second execution, and zero AI hallucination:", body_style))
    story.append(Spacer(1, 4))

    arch_layers = [
        [Paragraph("<b>Architectural Layer</b>", table_cell_header), Paragraph("<b>Technologies & Frameworks</b>", table_cell_header), Paragraph("<b>Functional Responsibility</b>", table_cell_header)],
        [
            Paragraph("<b>1. Presentation Layer (UI)</b>", table_cell_bold),
            Paragraph("React 18, Vite, Tailwind CSS, Lucide Icons, Web Speech Synthesis API", table_cell),
            Paragraph("Responsive enforcement dashboard, interactive scan studio, 6-tab audit viewer, visual bounding box inspector, senior-friendly accessibility.", table_cell)
        ],
        [
            Paragraph("<b>2. API Gateway & Routing</b>", table_cell_bold),
            Paragraph("FastAPI, Uvicorn ASGI Server, Pydantic Schemas, OAuth2 Password Bearer", table_cell),
            Paragraph("RESTful endpoints for auth, scanning, inspection history, product catalogue, rule library, analytics, and report downloads.", table_cell)
        ],
        [
            Paragraph("<b>3. Computer Vision & OCR</b>", table_cell_bold),
            Paragraph("OpenCV 4.10, Tesseract OCR 5.4.0, NumPy, Pillow", table_cell),
            Paragraph("CLAHE contrast equalization, bilateral denoising, Hough deskewing, word-level bounding box coordinate extraction, character confidence scoring.", table_cell)
        ],
        [
            Paragraph("<b>4. Information Extraction</b>", table_cell_bold),
            Paragraph("Deterministic Regex Engine, Spatial Line Grouping, NLP Parsers", table_cell),
            Paragraph("Structured declaration parsing (Mfr, Net Qty, MRP, USP, Dates, Consumer Care) + 11 nutrient facts extraction.", table_cell)
        ],
        [
            Paragraph("<b>5. Compliance & Scoring</b>", table_cell_bold),
            Paragraph("Deterministic Rule Engine, FSSAI/ICMR Health Classifier, Weighted Scorer", table_cell),
            Paragraph("12 Statutory Rule Groups from 40 Gazettes, explainable 0–100 scoring across 5 categories, show-cause notice recommendations.", table_cell)
        ],
        [
            Paragraph("<b>6. Visual Evidence Generator</b>", table_cell_bold),
            Paragraph("OpenCV Graphic Overlay Engine, Bounding Box Cropper", table_cell),
            Paragraph("Draws color-coded bounding overlays on packages and crops evidence snippets for reports and UI cards.", table_cell)
        ],
        [
            Paragraph("<b>7. Statutory Report Engine</b>", table_cell_bold),
            Paragraph("ReportLab 4.5 Platypus (PDF) & python-docx (DOCX)", table_cell),
            Paragraph("Generates court-admissible PDF notices with GoI headers and editable Word documents for legal proceedings.", table_cell)
        ],
        [
            Paragraph("<b>8. Database & Persistence</b>", table_cell_bold),
            Paragraph("SQLAlchemy ORM, SQLite (Built-in) / PostgreSQL Ready", table_cell),
            Paragraph("Relational storage for Users, Products, Inspections, Declarations, ComplianceResults, Violations, Reports, and AuditLogs.", table_cell)
        ],
        [
            Paragraph("<b>9. Security & Audit Trail</b>", table_cell_bold),
            Paragraph("PyJWT, SHA-256 + Salted Hashing, RBAC Middleware", table_cell),
            Paragraph("Role-Based Access Control (Admin, Supervisor, Inspector), session validation, immutable audit logging of all system actions.", table_cell)
        ]
    ]

    t_arch = Table(arch_layers, colWidths=[120, 160, 260])
    t_arch.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # PART 7: EVERY MAJOR FEATURE (1 TO 24)
    # =========================================================================
    add_part_header("7", "Every Major Feature Deep-Dive (Features 1–24)", "Exhaustive documentation of all 24 UI and backend modules with inputs, outputs, logic, and limitations.")

    features = [
        ("1. Officer Authentication & Demo Login", 
         "Authenticates enforcement personnel and establishes RBAC context.",
         "Officer enters email/password or clicks a 1-click official user card.",
         "User credentials (email, username, password).",
         "JWT access token (HS256) + User Profile object + Role context.",
         "Backend queries User table, computes salted SHA-256 hash, generates JWT, logs USER_LOGIN audit event.",
         "Prevents unauthorized public access while allowing seamless field demonstration.",
         "FastAPI OAuth2, PyJWT, SHA-256, LocalStorage.",
         "Incorrect password returns 401 Unauthorized; token expiry logs user out.",
         "Demo secret key in environment; production requires asymmetric RS256 and OAuth2 IDP."),

        ("2. Executive Enforcement Dashboard",
         "Provides high-level situational awareness across all inspections.",
         "Officer views dashboard cards, compliance rate charts, top violations, and recent scans.",
         "Database aggregation queries via <code>/api/analytics/summary</code>.",
         "Total scan count, compliant count, non-compliant count, compliance rate, violation chart.",
         "Calculates SQL aggregate metrics (counts, percentages, top violation group-by queries).",
         "Enables supervisors to identify non-compliant market trends and offending manufacturers.",
         "React, Tailwind, SQLAlchemy func.count, Recharts / CSS Gauges.",
         "Empty database shows zero states.",
         "Currently single-node in-memory SQL aggregation; production requires OLAP / ClickHouse cache."),

        ("3. Scan Packaging Studio",
         "Interactive studio for uploading package images or executing curated SIH demo scenarios.",
         "Officer drags/drops package image or clicks one of 3 SIH curated demo sample cards.",
         "Multipart/form-data image file OR sample filename string.",
         "Triggers 5-stage live AI inspection pipeline and transitions to Detail view.",
         "Handles file ingestion, creates unique Inspection ID, invokes OpenCV, OCR, and Compliance Engine.",
         "Central workbench for field inspectors auditing pre-packaged goods.",
         "FastAPI UploadFile, FileReader API, CSS Pulse progress indicators.",
         "Unsupported file formats (.bmp, .tiff) or corrupt images raise 400 Bad Request.",
         "Requires reasonable image resolution (>300 DPI recommended for micro-text)."),

        ("4. OCR & Text Detection Engine",
         "Converts package raster images into structured text tokens with spatial coordinates.",
         "Automated background execution during scan.",
         "OpenCV preprocessed numpy image array.",
         "Dictionary containing raw text, word bounding boxes, line groups, average confidence score.",
         "Executes <code>pytesseract.image_to_data</code>, groups adjacent words into lines, computes line bounding boxes.",
         "Extracts text from complex, unformatted packaging labels without human typing.",
         "Tesseract OCR 5.4.0, PIL / Pillow, PyTesseract.",
         "Extremely blurry images yield low confidence (<50%) or empty text.",
         "Tesseract CPU-bound; curved surface text requires cylindrical unrolling in pre-processing."),

        ("5. Information Extraction Engine",
         "Transforms unstructured OCR text into 9 mandatory Legal Metrology declarations.",
         "Automated execution following OCR.",
         "OCR line blocks and raw text string.",
         "Structured dictionary containing 9 declaration objects with detected values, boolean flags, confidence scores, and bounding boxes.",
         "Executes 9 deterministic regular expression parsers with contextual boundary cleaning.",
         "Bridges the gap between raw OCR text and statutory rule validation.",
         "Deterministic Regex, Contextual String Tokenization.",
         "Non-standard packaging terminology may fail pattern matching, triggering manual review.",
         "Requires standard alphanumeric character sets; highly stylized artistic brand logos may not parse as plain text."),

        ("6. Label Compliance Engine (12 Rules)",
         "Evaluates extracted declarations against 12 Statutory Legal Metrology Rule Groups.",
         "Automated deterministic execution.",
         "Extracted declarations dictionary + Image quality metrics.",
         "Evaluation results list with PASS / WARNING / VIOLATION status, severities, and gazette citations.",
         "Runs deterministic validation algorithms for each rule group (e.g. checks PIN code in address, SI unit symbols in Net Qty, inclusive of taxes in MRP, USP mathematical check).",
         "Guarantees 100% legally grounded, explainable compliance decisions without AI hallucination.",
         "Python Symbolic Rule Evaluator, Legal Metrology Act 2009 & PCR 2011 dataset.",
         "If OCR misses a declaration entirely, rule engine records it as a VIOLATION.",
         "Covers 12 major gazette rule groups; niche commodity exemptions require future rule expansion."),

        ("7. Nutritional Values Extraction",
         "Extracts 11 statutory nutritional facts from the package Nutrition Facts panel.",
         "Automated execution during scan.",
         "OCR text stream and line blocks.",
         "Nutritional facts dictionary (Energy, Protein, Carbs, Sugars, Added Sugars, Fiber, Fat, Saturated Fat, Trans Fat, Sodium, Serving Size).",
         "Regex parser detects nutrient keywords, numerical values, and unit tokens (kcal, g, mg). Standardizes Salt to Sodium equivalent.",
         "Enables dual-purpose consumer protection (metrology compliance + nutritional awareness).",
         "Deterministic Regex Parser, Nutritional Unit Normalizer.",
         "Packages without nutritional tables return empty/not-found states gracefully.",
         "Extracts values per 100g/100ml; per-serving calculations depend on declared serving sizes."),

        ("8. Informational Health Indicator",
         "Provides an AI-derived public health classification based on detected nutrition facts.",
         "Automated execution following nutritional extraction.",
         "Extracted nutrition facts dictionary.",
         "Health classification (HEALTHIER, MODERATE, LESS HEALTHY, or INSUFFICIENT DATA), score, risk factors, and positive factors.",
         "Evaluates detected Sodium (>600mg), Saturated Fat (>5g), and Sugars (>22.5g) against standard FSSAI/ICMR benchmarks. Handles pure cooking oils contextually.",
         "Offers transparent consumer health context without medical claims.",
         "FSSAI & ICMR Public Health Dietary Benchmarks.",
         "If nutrition panel is missing, outputs 'INSUFFICIENT DATA' rather than guessing.",
         "Explicitly informational; does not constitute clinical dietary diagnosis."),

        ("9. Violations Detection & Classification",
         "Aggregates and classifies infractions by severity level (CRITICAL, HIGH, MEDIUM, LOW).",
         "Displayed in the Violations tab of the Inspection Detail page.",
         "Compliance results from the rule engine.",
         "List of Violation objects with titles, legal basis citations, severity badges, and evidence links.",
         "Filters compliance results for VIOLATION and WARNING states; maps statutory legal basis from gazettes.",
         "Provides enforcement officers with an immediate summary of actionable legal infractions.",
         "Relational Violation models, SQLAlchemy ORM.",
         "None (deterministic filter).",
         "Severity ratings are calibrated to statutory penalties under Section 36(1) and PCR 2011."),

        ("10. Visual Evidence Bounding Boxes & Crops",
         "Renders color-coded overlays on the packaging image and crops violation snippets.",
         "Displayed in Evidence tab and on inspection cards.",
         "Original packaging image + Compliance results with bounding box coordinates.",
         "Annotated packaging image URL + Array of cropped evidence JPEG files.",
         "OpenCV draws colored rectangles (Green=PASS, Amber=WARNING, Red=VIOLATION) with text badges. Crops localized bounding box coordinates with 20px padding.",
         "Creates tamper-evident visual proof for prosecution in consumer dispute forums.",
         "OpenCV <code>cv2.rectangle</code>, <code>cv2.putText</code>, image array slicing.",
         "Bounding boxes outside image boundaries are safely clamped.",
         "Coordinate accuracy depends on OCR word localization fidelity."),

        ("11. Interactive Inspection Detail Studio",
         "Comprehensive 6-tab inspection workbench for deep-dive analysis.",
         "Officer switches tabs (Label Compliance, Nutrition, Violations, Visual Evidence, Official Report, Supervisory Review).",
         "Inspection record ID.",
         "Interactive scorecard, score gauge, declaration audit table, nutrition grid, and zoomable evidence viewer.",
         "Fetches complete inspection payload from <code>/api/inspections/{id}</code> and renders dynamic tabbed UI.",
         "Consolidates all inspection artifacts into a single unified workspace.",
         "React Tabs, Tailwind CSS, Lucide Icons, ScoreGauge component.",
         "Network failure displays friendly error card with return button.",
         "Optimized for desktop/tablet enforcement monitors."),

        ("12. Official PDF Report Generator",
         "Generates court-admissible statutory inspection reports in PDF format.",
         "Officer clicks 'Download Official PDF'.",
         "Full inspection payload dictionary.",
         "High-resolution PDF file with Government of India header, metadata tables, declaration audits, and signature blocks.",
         "ReportLab Platypus compiles Flowables, Paragraphs, Tables, and HR lines into a structured letter-size PDF document.",
         "Serves as the official legal notice issued to non-compliant manufacturers.",
         "ReportLab 4.5.1 Platypus, Flowable Architecture.",
         "Missing output directory is created automatically on demand.",
         "PDF is generated server-side; sub-second generation time (<200ms)."),

        ("13. Editable DOCX Report Export",
         "Generates fully editable Microsoft Word inspection notices for legal adaptation.",
         "Officer clicks 'Export DOCX'.",
         "Full inspection payload dictionary.",
         "Structured .docx document containing notice headings, findings tables, and violation summaries.",
         "python-docx builds tables, headings, paragraph runs, and styling tags into a standard OpenXML document.",
         "Allows legal officers to customize notice wording or add legal case numbers before dispatch.",
         "python-docx 1.1.2.",
         "None.",
         "Formatting conforms to standard GoI administrative notice layout."),

        ("14. Inspection History & Repository",
         "Searchable and filterable archive of all historical packaging inspections.",
         "Officer searches by product name, ID, or filters by status (COMPLIANT, NON-COMPLIANT) and category.",
         "Filter query parameters (status, category, search text).",
         "List of historical inspection summary cards with thumbnail images, scores, and timestamps.",
         "SQLAlchemy runs filtered ILIKE queries on Inspection table ordered by creation date descending.",
         "Enables repeat-offender tracking and audit trail review.",
         "FastAPI Query parameters, React Search/Filter bar.",
         "Empty search results display 'No matching inspections found'.",
         "Pagination recommended for deployments exceeding 100,000 inspection records."),

        ("15. Product Repository",
         "Centralized catalog of all scanned pre-packaged commodities.",
         "Officer views product catalog, brands, declared MRPs, and net quantities.",
         "Product database records.",
         "Product cards with brand info, category badges, and linked inspection records.",
         "Relational Product queries linked via 1-to-many relationship with Inspections.",
         "Provides brand-level compliance tracking across multiple SKUs.",
         "SQLAlchemy Product model.",
         "Unbranded items default to 'Unbranded'.",
         "Barcode scanning integration is pre-structured in the schema."),

        ("16. Rule Library (40 Gazettes)",
         "Interactive knowledge base indexing the 40 official Legal Metrology gazettes and rule definitions.",
         "Officer browses the 12 rule definitions, gazette citations, required declarations, and statutory penalties.",
         "Rule definitions array in <code>rule_definitions.py</code>.",
         "Expandable rule cards with gazette filenames, rule numbers, severity tags, and explanatory notes.",
         "Renders structured metadata mapped directly to the 40 PDFs in <code>Government_Gazette_Dataset</code>.",
         "Ensures 100% legal transparency and serves as a training ground for junior inspectors.",
         "React UI, Statutory Gazette Dataset Index.",
         "None.",
         "Reflects all 40 indexed gazettes in the SIH repository."),

        ("17. Immutable Audit Trail & Logs",
         "Chronological, tamper-evident record of all user logins, scans, and supervisory reviews.",
         "Officer navigates to Audit Trail tab; reviews event logs with timestamps, actions, and IP addresses.",
         "AuditLog SQL records.",
         "Audit table showing Action (e.g. USER_LOGIN, PRODUCT_SCANNED), Entity ID, Details, User, and Timestamp.",
         "Backend routes automatically insert AuditLog rows upon every significant mutation or scan.",
         "Ensures accountability, prevents evidence tampering, and satisfies administrative vigilance standards.",
         "SQLAlchemy AuditLog table, ISO timestamping.",
         "Read-only for inspectors; admin can view full history.",
         "Production deployment should forward logs to WORM (Write Once Read Many) cloud storage."),

        ("18. Senior-Friendly Accessibility (Senior Mode)",
         "Enlarges typography, increases tap targets, and expands spacing for senior enforcement officers.",
         "Officer toggles 'Senior Mode' in the top navbar.",
         "Boolean state toggle.",
         "Applies <code>.senior-mode</code> and <code>.large-text</code> CSS classes across the entire DOM tree.",
         "CSS root font-size scaling, minimum 16px text sizes, enhanced padding on all buttons and table cells.",
         "Supports senior directors and field officers who may experience vision fatigue.",
         "React Context (AccessibilityContext), LocalStorage, CSS variables.",
         "None.",
         "State persists across browser reloads via LocalStorage."),

        ("19. High Contrast Visual Filter",
         "Enhances contrast ratios for inspection under bright sunlight or outdoor field conditions.",
         "Officer toggles 'High Contrast' in the top navbar.",
         "Boolean state toggle.",
         "Applies <code>.high-contrast</code> class with sharp borders, deep black text, and high-visibility badges.",
         "CSS filter adjustments and high-contrast color token substitutions.",
         "Ensures screen readability in outdoor wholesale grain markets and bright sunlight.",
         "React AccessibilityContext, CSS filters.",
         "None.",
         "Complies with WCAG 2.1 AAA contrast standards."),

        ("20. Voice & Audio Guidance (Speech Synthesis)",
         "Speaks inspection scores, compliance status, and action notifications aloud.",
         "Officer toggles 'Audio Guidance' and interacts with the application.",
         "Text strings from inspection results and status updates.",
         "Spoken audio narration via browser speech engine.",
         "Calls browser <code>window.speechSynthesis.speak()</code> with SpeechSynthesisUtterance.",
         "Provides hands-free audio confirmation during field inspections.",
         "HTML5 Web Speech API (SpeechSynthesis).",
         "Silent fallback if browser speech synthesis is unsupported or muted.",
         "Voice pitch and rate are normalized to 0.95x for clear Indian English pronunciation."),

        ("21. SIH Instant Demo Scenario Workflows",
         "Pre-configured statutory packaging scenarios for instantaneous evaluator demonstration.",
         "Officer clicks Sample 1 (Atta), Sample 2 (Oil), or Sample 3 (Namkeen).",
         "Curated image paths and statutory expected outcomes.",
         "Executes full live pipeline on the sample, generating real scores, bounding boxes, and PDF reports.",
         "Copies sample image from <code>backend/samples</code> to <code>backend/uploads</code> and runs the complete AI pipeline.",
         "Enables flawless, reproducible 30-second live demonstrations during hackathon judging.",
         "FastAPI endpoint <code>/api/scan/demo-samples</code>, Shutil file copy.",
         "None (fully self-contained).",
         "Provides exact benchmarks (Atta ~96/100, Oil ~68/100, Namkeen ~32/100)."),

        ("22. Role-Based Access Control (RBAC)",
         "Enforces hierarchical permissions across ADMIN, SUPERVISOR, and INSPECTOR roles.",
         "Officer logs in; UI adapts available actions based on user role.",
         "User role claim in JWT token.",
         "Restricted UI elements (e.g., supervisor review notes, audit log clearance).",
         "FastAPI <code>require_roles()</code> dependency checks user role against required permission list.",
         "Maintains administrative separation of duties between field inspectors and approving supervisors.",
         "FastAPI Dependency Injection, JWT Role Claims.",
         "Unauthorized role actions return 403 Forbidden.",
         "Enforces 3 distinct tiers: ADMIN (Apex), SUPERVISOR (Review), INSPECTOR (Field)."),

        ("23. 1-Click Role Switcher",
         "Instantaneous role switching toolbar for evaluator demonstrations.",
         "Officer clicks 'Switch to Supervisor', 'Switch to Admin', or 'Switch to Inspector' in navbar.",
         "Target role string.",
         "Automatically authenticates as the designated official user and updates UI state.",
         "Calls <code>switchDemoRole()</code> in AuthContext, authenticating as Soutik (Admin), Sayantan (Supervisor), or Jiya (Inspector).",
         "Allows judges to test multi-role workflows in seconds without manual re-typing.",
         "React Context, FastAPI OAuth2 Login.",
         "None.",
         "Demo convenience feature; disabled in production builds."),

        ("24. Remembered Login & Credential Persistence",
         "Persists authentication state and remembered email across sessions.",
         "Officer checks 'Remember Me' on the login screen.",
         "User email string.",
         "Pre-populates email field upon subsequent visits and retains active JWT token in storage.",
         "Stores token and user payload in browser <code>localStorage</code>; validates on app initialization.",
         "Prevents officer frustration from repeated logins during field audits.",
         "HTML5 LocalStorage API.",
         "Clearing browser cache removes stored credentials safely.",
         "Token expires automatically after 24 hours per security policy.")
    ]

    for f_title, f_desc, f_ui, f_in, f_out, f_int, f_util, f_tech, f_err, f_lim in features:
        story.append(Paragraph(f"<b>{f_title}</b>", section_heading_style))
        story.append(Paragraph(f"<b>Core Function:</b> {f_desc}", body_style))
        f_table_data = [
            [Paragraph("<b>User Interaction:</b>", table_cell_bold), Paragraph(f_ui, table_cell)],
            [Paragraph("<b>Input Data:</b>", table_cell_bold), Paragraph(f_in, table_cell)],
            [Paragraph("<b>Output Produced:</b>", table_cell_bold), Paragraph(f_out, table_cell)],
            [Paragraph("<b>Internal Logic:</b>", table_cell_bold), Paragraph(f_int, table_cell)],
            [Paragraph("<b>Operational Utility:</b>", table_cell_bold), Paragraph(f_util, table_cell)],
            [Paragraph("<b>Underlying Tech:</b>", table_cell_bold), Paragraph(f_tech, table_cell)],
            [Paragraph("<b>Failure Handling:</b>", table_cell_bold), Paragraph(f_err, table_cell)],
            [Paragraph("<b>Limitations:</b>", table_cell_bold), Paragraph(f_lim, table_cell)]
        ]
        t_f = Table(f_table_data, colWidths=[110, 430])
        t_f.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
            ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FFFFFF")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t_f)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # PART 8: AI / COMPUTER VISION / OCR EXPLANATION
    # =========================================================================
    add_part_header("8", "AI / Computer Vision / OCR Deep Dive", "Complete technical analysis of the computer vision and optical recognition pipeline.")

    story.append(Paragraph("A critical distinction in PRAMAN AI that impresses technical judges is the strict architectural separation of responsibilities across the pipeline:", body_style))
    story.append(Spacer(1, 3))

    distinctions = [
        ("1. Optical Character Recognition (OCR)", "Perceptual pattern recognition. Converts 2D pixel grids into discrete ASCII/Unicode characters with 2D bounding box coordinates and statistical character confidence. Handled by <b>Tesseract OCR 5.4.0</b>."),
        ("2. Information Extraction (NLP/Regex)", "Structural text parsing. Groups tokens into semantic Legal Metrology declaration fields (e.g. Net Qty = 5.0 kg, MRP = ₹230.00). Handled by <b>DeclarationExtractor</b> using deterministic linguistic patterns."),
        ("3. Rule Validation (Symbolic Metrology)", "Deterministic legal logic. Evaluates extracted values against statutory gazettes (e.g. verifying SI unit metric compliance, tax wording, and mathematical USP consistency). Handled by <b>ComplianceRuleEngine</b>."),
        ("4. AI-Assisted Decision Support", "Synthesis and scoring. Computes explainable 0–100 compliance scores, identifies critical infractions, and formulates statutory show-cause recommendations under Section 36(1).")
    ]

    for d_title, d_desc in distinctions:
        story.append(Paragraph(f"<b>{d_title}</b>", sub_section_heading_style))
        story.append(Paragraph(d_desc, body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Computer Vision Edge-Case Handling in PRAMAN AI:</b>", section_heading_style))

    cv_challenges = [
        ("Uneven Lighting & Specular Glare", "Packaging films reflect light. PRAMAN AI applies <b>CLAHE (Contrast Limited Adaptive Histogram Equalization)</b> with tileGridSize (8,8) and clipLimit 2.0 to normalize localized illumination without blowing out highlights."),
        ("Packaging Texture Noise", "Grainy paper, burlap bags, or textured plastic can introduce OCR noise. PRAMAN AI uses a <b>Bilateral Filter</b> (d=9, sigmaColor=75, sigmaSpace=75) which smooths surface texture while preserving sharp character edges."),
        ("Rotated & Skewed Packaging", "Handheld photos are frequently tilted. PRAMAN AI applies <b>Canny Edge Detection and Probabilistic Hough Transform</b> (<code>cv2.HoughLinesP</code>) to detect dominant line angles, computing the median tilt angle and rotating the affine matrix back to horizontal alignment."),
        ("Low Contrast Micro-Lettering", "Manufacturers sometimes print declarations in faint grey text on white backgrounds. PRAMAN AI computes the standard deviation of grayscale pixels; if contrast STD is below 35, it flags Rule 10 (Principal Display Panel Legibility) for manual officer verification."),
        ("Curved Bottles & Cans", "Cylindrical distortion causes text compression at boundaries. In PRAMAN AI, line-level aggregation merges adjacent bounding boxes, ensuring that even wrapped words are captured into cohesive lines.")
    ]

    for c_title, c_desc in cv_challenges:
        story.append(Paragraph(f"• <b>{c_title}:</b> {c_desc}", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PART 9: LEGAL METROLOGY / COMPLIANCE LOGIC (12 RULE GROUPS)
    # =========================================================================
    add_part_header("9", "Legal Metrology / Compliance Logic (12 Rules)", "Statutory rules derived from 40 Official Gazettes and evaluated deterministically.")

    story.append(Paragraph("PRAMAN AI implements 12 distinct statutory rule groups derived directly from the Legal Metrology Act, 2009, the Legal Metrology (Packaged Commodities) Rules, 2011, and 40 indexed official gazette notifications:", body_style))
    story.append(Spacer(1, 4))

    rules_deep_dive = [
        ("LM-PCR-01", "Manufacturer / Packer / Importer Name & Complete Address", "Rule 6(1)(a) & GSR 226(E)", "8(xii)_0_1732871346.pdf", "HIGH",
         "Business entity name + complete physical address with locality, state, and 6-digit PIN code.",
         "Explicit entity identifier (e.g. 'Manufactured by', 'Packed by', 'Mfg & Pkd by') followed by complete address.",
         "Identifiable legal entity name AND valid 6-digit PIN code or clear locality address.",
         "Total absence of manufacturer name or incomplete address lacking city/state/PIN code (warning).",
         "Green bounding box over address block; Warning card if address lacks PIN code."),

        ("LM-PCR-02", "Common or Generic Commodity Name", "Rule 6(1)(b)", "8(xii)_0_1732871346.pdf", "HIGH",
         "Recognized common or generic commodity name (e.g. 'Wheat Flour / Atta', 'Sunflower Oil', 'Cotton Shirt').",
         "Explicit commodity title rather than exclusively an uninformative trademark brand name.",
         "Generic commodity name clearly detected on principal packaging surface.",
         "Absence of generic commodity name; package contains only trademark brand without stating contents.",
         "Bounding box highlighting detected commodity title card."),

        ("LM-PCR-03", "Metric Net Quantity & Prohibited Qualifiers", "Rule 6(1)(c), Rule 11, 12, 13", "8(xii)_0_1732871346.pdf & 2023.12.29 SOP Oil", "CRITICAL",
         "Net quantity expressed strictly in standard SI metric units (g, kg, ml, L, m, cm, mm, N).",
         "Numeric magnitude followed by recognized SI unit symbol. Prohibits qualifiers like 'Jumbo', 'Family Pack', 'Super Saver' without standard metric weight.",
         "Standard metric quantity declared (e.g. '5.0 kg', '1.0 L', '500 g').",
         "Non-metric units (lbs, oz), missing quantity, or deceptive non-standard expressions ('Jumbo Pack').",
         "Red bounding box on prohibited qualifier or Green box on valid metric declaration."),

        ("LM-PCR-04", "Month and Year of Manufacture / Packing", "Rule 6(1)(d)", "8(xii)_0_1732871346.pdf", "HIGH",
         "Month and Year in which commodity was manufactured, packed, or imported.",
         "Valid date format ('MM/YYYY', 'Month YYYY', 'DD/MM/YYYY') preceded by 'Mfg Date', 'Pkd Date', or 'Packed on'.",
         "Legible Month and Year declaration detected.",
         "Complete omission of manufacturing or packing date.",
         "Bounding box overlay on manufacturing date cluster."),

        ("LM-PCR-05", "Maximum Retail Price (MRP) & Inclusive of All Taxes", "Rule 6(1)(e) & Rule 18", "8(xii)_0_1732871346.pdf & 230946_1732871433.pdf", "CRITICAL",
         "Retail sale price in Indian Rupees (₹ or Rs.) with mandatory tax clause.",
         "Must declare 'Maximum Retail Price ₹... (inclusive of all taxes)' or 'MRP ₹... incl. of all taxes'. Dual MRP is illegal.",
         "MRP declared with explicit Indian currency symbol AND statutory 'inclusive of all taxes' text.",
         "MRP missing, currency symbol missing, or statutory 'inclusive of all taxes' clause omitted (High violation).",
         "Red bounding box if tax clause is missing; Green box if fully compliant."),

        ("LM-PCR-06", "Unit Sale Price (USP) Declaration & Math Consistency", "Rule 6(1)(11) & GSR 226(E)", "GSR226_1732871458.pdf & Amendment 2023", "HIGH",
         "Unit sale price rounded to 2 decimals (per g if <1kg, per kg if >=1kg, per ml if <1L, per L if >=1L, per N).",
         "Declared USP string ('₹ X / kg') + Mathematical verification: USP must equal MRP divided by Net Quantity.",
         "USP declared in correct metric unit AND mathematically matches MRP / Quantity (within ₹0.05 tolerance).",
         "USP missing entirely (on packages > 1 unit) OR declared USP mathematically contradicts MRP / Quantity.",
         "Green box on valid USP; Amber warning card detailing mathematical discrepancy if mismatched."),

        ("LM-PCR-07", "Consumer Care Redressal Details", "Rule 6(1)(f) & Rule 2(aa)", "8(xii)_0_1732871346.pdf & 2022 Garment Amendment", "HIGH",
         "Name, address, telephone / toll-free helpline number, and email address of consumer redressal officer.",
         "At least two active direct contact modes: valid Email address AND Telephone / Helpline number.",
         "Both valid email address AND telephone helpline detected.",
         "Complete omission of consumer care details, or partial disclosure (only phone or only email - warning).",
         "Bounding box on consumer care panel; Warning card if only one contact mode is present."),

        ("LM-PCR-08", "Country of Origin (COO) Declaration", "Rule 6(1)(da) & Rule 6(4)", "2026.02.13 COO Filter & PCR 3rd 2026", "HIGH",
         "Explicit Country of Origin for all imported goods and e-commerce pre-packaged commodities.",
         "'Country of Origin: <Country>', 'Made in <Country>', or 'Manufactured in <Country>'.",
         "Explicit origin country declared, or domestic origin verified via manufacturer address stating India.",
         "Absence of Country of Origin declaration on imported or e-commerce packaging.",
         "Bounding box on 'Made in India' / Origin declaration."),

        ("LM-PCR-09", "Garment & Hosiery Standard Size & Piece Count", "3rd Amendment 2022 / GSR 858(E)", "2022 3rd amendment in PCR Garments", "MEDIUM",
         "Standard international/Indian size code (S, M, L, XL, XXL) or dimensional measurements (cm/in) + piece count.",
         "Apparel category packages must declare size code and count ('1 N' / '1 Piece').",
         "Standard size code or dimensional measurement detected on garment packaging.",
         "Garment package lacking standard size designation or piece count.",
         "Bounding box on apparel size label."),

        ("LM-PCR-10", "Principal Display Panel Legibility & Contrast", "Rule 7 & Rule 9", "8(xii)_0_1732871346.pdf & 267107_1761404707.pdf", "MEDIUM",
         "Mandatory declarations must appear on PDP with minimum numeral height and sharp contrast.",
         "OpenCV image contrast standard deviation and numeral bounding box height analysis.",
         "High contrast text (Contrast STD >= 40, brightness 60–210).",
         "Low contrast (STD < 25) or poor lighting triggering 'MANUAL_VERIFICATION_REQUIRED'.",
         "Contrast and lighting telemetry card in inspection report."),

        ("LM-PCR-11", "QR Code & Digital Declarations Proviso", "Rule 6(1)(a) proviso & QR Amendment", "Notification - Legal Metrology (QR Code)_1732871487.pdf", "MEDIUM",
         "QR code presence does not exempt physical label from declaring Manufacturer, MRP, Net Qty, and Helpline.",
         "Detects QR code references; verifies that physical mandatory declarations are preserved.",
         "QR code present while all mandatory physical declarations remain on the package surface.",
         "QR code present, but manufacturer omits physical MRP or Net Qty claiming 'scan for details' (Illegal).",
         "Visual bounding box on QR code reference with proviso verification badge."),

        ("LM-PCR-12", "Rule 26 Exemption Verification & Pan Masala Restriction", "Rule 26 & 2025 Amendment", "2nd PCR Pan Masala_1764736734.pdf", "LOW",
         "Packages <= 10g/10ml exempt from certain declarations EXCEPT Pan Masala / Tobacco where all rules apply.",
         "Evaluates package category and declared net quantity against statutory exemption thresholds.",
         "Valid exemption for qualified micro-packages or bulk containers (>25kg).",
         "Pan Masala package omitting declarations claiming small package exemption (Illegal).",
         "Exemption audit badge in inspection results.")
    ]

    for rid, rname, rsec, rdoc, rsev, rreq, rlook, rcomp, rviol, rev in rules_deep_dive:
        story.append(Paragraph(f"<b>[{rid}] {rname}</b> ({rsec})", sub_section_heading_style))
        r_table_data = [
            [Paragraph("<b>Statutory Basis:</b>", table_cell_bold), Paragraph(f"{rsec} | Gazette: {rdoc} | Severity: <b>{rsev}</b>", table_cell)],
            [Paragraph("<b>What is Checked:</b>", table_cell_bold), Paragraph(rreq, table_cell)],
            [Paragraph("<b>System Looks For:</b>", table_cell_bold), Paragraph(rlook, table_cell)],
            [Paragraph("<b>Compliant Criteria:</b>", table_cell_bold), Paragraph(rcomp, table_cell)],
            [Paragraph("<b>Violation Criteria:</b>", table_cell_bold), Paragraph(rviol, table_cell)],
            [Paragraph("<b>Visual Evidence:</b>", table_cell_bold), Paragraph(rev, table_cell)]
        ]
        t_r = Table(r_table_data, colWidths=[110, 430])
        t_r.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
            ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FFFFFF")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t_r)
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # PART 10: NUTRITIONAL VALUES & HEALTH CLASSIFICATION
    # =========================================================================
    add_part_header("10", "Nutritional Values & Health Classification", "Nutritional facts extraction, FSSAI/ICMR threshold evaluation, and health indicators.")

    story.append(Paragraph("<b>CRITICAL STATUTORY DISTINCTION: LEGAL COMPLIANCE &ne; HEALTH ASSESSMENT</b>", ParagraphStyle("DistH", parent=body_style, fontName="Helvetica-Bold", textColor=colors.HexColor("#DC2626"))))
    story.append(Paragraph("A pre-packaged food product can be <b>100% Legally Compliant</b> under the Legal Metrology Act, 2009 while simultaneously possessing a <b>'LESS HEALTHY'</b> nutritional profile (e.g., deep-fried potato chips with complete mandatory declarations). Conversely, a nutritious whole-food product can be <b>'NON-COMPLIANT'</b> under Legal Metrology if it omits statutory tax wording. PRAMAN AI strictly decouples these two analytical domains.", body_style))
    story.append(Spacer(1, 4))

    nutri_table_data = [
        [Paragraph("<b>Nutrient Field</b>", table_cell_header), Paragraph("<b>Standard Benchmark / Threshold</b>", table_cell_header), Paragraph("<b>Evaluation & Health Logic</b>", table_cell_header)],
        [
            Paragraph("<b>Energy / Calories</b>", table_cell_bold),
            Paragraph("Declared in kcal / kJ per 100g or 100ml", table_cell),
            Paragraph("Evaluates overall caloric density. High energy (>500 kcal/100g) flagged for snack categories.", table_cell)
        ],
        [
            Paragraph("<b>Protein</b>", table_cell_bold),
            Paragraph("&gt;= 10.0g/100g is Rich Source; &gt;= 5.0g is Source", table_cell),
            Paragraph("Positive nutritional contributor. Increases health score.", table_cell)
        ],
        [
            Paragraph("<b>Dietary Fiber</b>", table_cell_bold),
            Paragraph("&gt;= 6.0g/100g is High Fiber; &gt;= 3.0g is Source", table_cell),
            Paragraph("Strong positive factor for digestive health and metabolic balance.", table_cell)
        ],
        [
            Paragraph("<b>Sodium / Salt</b>", table_cell_bold),
            Paragraph("&gt; 600 mg/100g is HIGH; &lt; 120 mg/100g is LOW", table_cell),
            Paragraph("Primary nutrient of public health concern. Elevated sodium triggers 'LESS HEALTHY' risk classification.", table_cell)
        ],
        [
            Paragraph("<b>Saturated Fat</b>", table_cell_bold),
            Paragraph("&gt; 5.0 g/100g is HIGH; &lt; 1.5 g/100g is LOW", table_cell),
            Paragraph("Cardiovascular risk factor. Pure cooking oils/fats are handled contextually as culinary media.", table_cell)
        ],
        [
            Paragraph("<b>Total & Added Sugars</b>", table_cell_bold),
            Paragraph("&gt; 22.5 g/100g is HIGH; &lt; 5.0 g/100g is LOW", table_cell),
            Paragraph("High sugar density triggers public health risk flag.", table_cell)
        ],
        [
            Paragraph("<b>Trans Fatty Acids</b>", table_cell_bold),
            Paragraph("Must be 0.0 g/100g; &gt; 0.2g triggers risk flag", table_cell),
            Paragraph("Zero trans fat is positively recognized per FSSAI regulations.", table_cell)
        ]
    ]

    t_nutri = Table(nutri_table_data, colWidths=[120, 180, 240])
    t_nutri.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_nutri)
    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 11: OCR + VISUAL EVIDENCE PIPELINE
    # =========================================================================
    add_part_header("11", "Visual Evidence & Overlay Pipeline", "How PRAMAN AI links raw packaging pixels directly to legal infractions.")

    story.append(Paragraph("In legal metrology enforcement, an unbacked accusation of non-compliance is easily dismissed in court. PRAMAN AI builds an unbroken <b>Chain of Visual Evidence</b>:", body_style))
    story.append(Spacer(1, 3))

    ev_chain = [
        ("1. Image Pixel Matrix", "Raw uploaded package photograph stored with SHA-256 integrity hash."),
        ("2. OCR Coordinate Mapping", "Tesseract extracts word-level bounding box coordinates <code>(x, y, w, h)</code>."),
        ("3. Declaration Field Association", "Regex parser identifies the statutory declaration and binds it to the exact line coordinates."),
        ("4. Deterministic Rule Evaluation", "ComplianceRuleEngine determines if the declared value satisfies statutory criteria."),
        ("5. Color-Coded Overlay Rendering", "OpenCV renders a high-visibility rectangle (Green for PASS, Amber for WARNING, Red for VIOLATION) and prints the statutory Rule ID badge."),
        ("6. Evidence Crop Extraction", "OpenCV slices the bounding box region with a 20-pixel safety margin and saves a standalone high-resolution evidence snippet JPEG."),
        ("7. Court-Ready Report Attachment", "The evidence crop URL and spatial coordinates are permanently embedded into the official PDF/Word inspection report.")
    ]

    for ec_num, ec_text in ev_chain:
        story.append(Paragraph(f"<b>{ec_num}:</b> {ec_text}", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PART 12: REPORT GENERATION (PDF & DOCX)
    # =========================================================================
    add_part_header("12", "Report Generation Engine (PDF & DOCX)", "Official statutory notice generation with ReportLab and python-docx.")

    story.append(Paragraph("PRAMAN AI includes dual statutory report generators configured to match standard Government of India administrative and judicial formats:", body_style))
    story.append(Spacer(1, 4))

    rep_comp = [
        [Paragraph("<b>Report Feature / Parameter</b>", table_cell_header), Paragraph("<b>Official PDF Notice (ReportLab)</b>", table_cell_header), Paragraph("<b>Editable Word Notice (python-docx)</b>", table_cell_header)],
        [
            Paragraph("<b>Target Use-Case</b>", table_cell_bold),
            Paragraph("Court-admissible statutory notice, immutable PDF archive, supervisor digital signature.", table_cell),
            Paragraph("Editable working draft for legal officers to append court case numbers or custom notes.", table_cell)
        ],
        [
            Paragraph("<b>Document Layout</b>", table_cell_bold),
            Paragraph("Formal Government of India banner, Ministry header, statutory metadata grid, 4 structured tables.", table_cell),
            Paragraph("Standard OpenXML document with formatted headings, metadata tables, and numbered finding lists.", table_cell)
        ],
        [
            Paragraph("<b>Declarations Audit Table</b>", table_cell_bold),
            Paragraph("Includes all 9 mandatory declarations with FOUND/MISSING status badges and confidence percentages.", table_cell),
            Paragraph("Complete 4-column Word table detailing field names, values, detection status, and confidence.", table_cell)
        ],
        [
            Paragraph("<b>Nutritional Information</b>", table_cell_bold),
            Paragraph("Dedicated nutritional breakdown table + AI health classification summary and disclaimer.", table_cell),
            Paragraph("Summary paragraph detailing detected nutritional status and public health indicator.", table_cell)
        ],
        [
            Paragraph("<b>Violations & Findings</b>", table_cell_bold),
            Paragraph("Color-coded status badges (PASS / WARNING / VIOLATION), source gazette citations, and findings.", table_cell),
            Paragraph("Bulleted rule evaluations with legal reference citations and specific explanatory findings.", table_cell)
        ],
        [
            Paragraph("<b>Endorsement Block</b>", table_cell_bold),
            Paragraph("Dual official sign-off boxes for Inspecting Official and Assistant Controller / Controller.", table_cell),
            Paragraph("Official endorsement signature block at document terminus.", table_cell)
        ],
        [
            Paragraph("<b>Generation Speed</b>", table_cell_bold),
            Paragraph("Sub-second (&lt; 200 ms) via ReportLab Platypus engine.", table_cell),
            Paragraph("Instantaneous (&lt; 100 ms) via python-docx engine.", table_cell)
        ]
    ]

    t_rep = Table(rep_comp, colWidths=[130, 205, 205])
    t_rep.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_rep)
    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 13: USER ROLES & PERMISSIONS (RBAC)
    # =========================================================================
    add_part_header("13", "User Roles & Permissions (RBAC)", "Role-Based Access Control matrix verified in the backend and frontend.")

    story.append(Paragraph("PRAMAN AI implements 3 distinct operational roles mapped to real-world Legal Metrology department hierarchies:", body_style))
    story.append(Spacer(1, 4))

    rbac_matrix = [
        [Paragraph("<b>Role Name</b>", table_cell_header), Paragraph("<b>Authorized Personnel & Badge</b>", table_cell_header), Paragraph("<b>Department / Unit</b>", table_cell_header), Paragraph("<b>Access Privileges & Restrictions</b>", table_cell_header)],
        [
            Paragraph("<b>ADMIN</b>", table_cell_bold),
            Paragraph("<b>Soutik</b> (LM-ADM-001)<br/><b>Rimi</b> (LM-ADM-004)", table_cell),
            Paragraph("Directorate of Legal Metrology, Central HQ & Apex Command", table_cell),
            Paragraph("Full system access: scan packaging, view all inspections, manage users, clear audit logs, view analytics, download all reports.", table_cell)
        ],
        [
            Paragraph("<b>SUPERVISOR</b>", table_cell_bold),
            Paragraph("<b>Sayantan</b> (LM-SUP-102)<br/><b>Debopriya</b> (LM-SUP-105)", table_cell),
            Paragraph("Regional Standards & Legal Enforcement Zones I & II", table_cell),
            Paragraph("Supervisory access: perform scans, review inspections, append official supervisor notes, approve or flag inspections, export notices. Cannot clear audit logs.", table_cell)
        ],
        [
            Paragraph("<b>INSPECTOR</b>", table_cell_bold),
            Paragraph("<b>Jiya</b> (LM-INS-203)<br/><b>Arkadip</b> (LM-INS-206)", table_cell),
            Paragraph("Field Inspection & Metrological Vigilance Unit", table_cell),
            Paragraph("Field access: scan packaging, view own and regional inspection history, download inspection reports, search products and rules. Cannot approve inspections or clear logs.", table_cell)
        ]
    ]

    t_rbac = Table(rbac_matrix, colWidths=[80, 130, 150, 180])
    t_rbac.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_rbac)
    story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # PART 14: DATA FLOW & STATE TRANSFORMATIONS
    # =========================================================================
    add_part_header("14", "Complete Data Flow & Schemas", "Conceptual data objects and state lifecycle across the inspection pipeline.")

    story.append(Paragraph("The lifecycle of data in PRAMAN AI progresses through 7 well-defined structural schemas:", body_style))
    story.append(Spacer(1, 3))

    data_objects = [
        ("1. Ingestion Payload", "Multipart image file or sample string &rarr; stored on disk at <code>backend/uploads/scan_UUID.jpg</code>."),
        ("2. Image Metrics Object", "<code>{mean_brightness: float, contrast_std: float, width: int, height: int, is_low_contrast: bool, quality_rating: 'GOOD'|'FAIR'|'LOW'}</code>."),
        ("3. OCR Raw & Line Tokens", "<code>{raw_text: str, average_confidence: float, lines: [{text, x, y, w, h, confidence}], blocks: [...]}</code>."),
        ("4. Extracted Declarations Map", "<code>{commodity_name: {value, found, confidence, bbox}, manufacturer_details: {value, found, has_complete_address, bbox}, net_quantity: {value, numeric_value, unit, is_standard_unit, bbox}, mrp: {value, numeric_value, includes_taxes_text, bbox}, unit_sale_price: {value, numeric_value, unit, bbox}, consumer_care: {value, email, phone, has_email, has_phone, bbox}, country_of_origin: {value, found, bbox}, garment_size: {...}, qr_code_present: bool}</code>."),
        ("5. Nutritional Profile Object", "<code>{energy: {value, numeric_value, unit, per}, protein: {...}, carbohydrates: {...}, sugars: {...}, added_sugars: {...}, fat: {...}, saturated_fat: {...}, trans_fat: {...}, sodium: {...}, fiber: {...}, serving_size: {...}}</code>."),
        ("6. Health Assessment Object", "<code>{classification: 'HEALTHIER'|'MODERATE'|'HIGH / LESS HEALTHY'|'INSUFFICIENT DATA', score: int, positive_factors: [str], risk_factors: [str], disclaimer: str}</code>."),
        ("7. Compliance Results & Score Record", "<code>{overall_score: int (0-100), decision: 'COMPLIANT'|'NON-COMPLIANT'|'PENDING REVIEW', decision_summary: str, recommended_action: str, categories: [{name, score, max_score, percentage}], results: [{rule_id, rule_name, category, status, severity, detected_value, expected_condition, explanation, source_document, source_section, bbox, crop_url}], violations: [...]}</code>.")
    ]

    for do_num, do_desc in data_objects:
        story.append(Paragraph(f"<b>{do_num}:</b>", sub_section_heading_style))
        story.append(Paragraph(do_desc, body_style))

    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 15: TECHNOLOGY STACK & JUSTIFICATIONS
    # =========================================================================
    add_part_header("15", "Technology Stack & Tool Justifications", "Exhaustive audit of all technologies, libraries, and frameworks utilized.")

    stack_data = [
        [Paragraph("<b>Layer / Technology</b>", table_cell_header), Paragraph("<b>Version / Package</b>", table_cell_header), Paragraph("<b>Role in Project</b>", table_cell_header), Paragraph("<b>Engineering Justification</b>", table_cell_header)],
        [
            Paragraph("<b>Backend Core</b>", table_cell_bold),
            Paragraph("Python 3.12 + FastAPI", table_cell),
            Paragraph("Asynchronous REST API Gateway", table_cell),
            Paragraph("High performance async IO, automatic OpenAPI Swagger docs, native Pydantic validation.", table_cell)
        ],
        [
            Paragraph("<b>Computer Vision</b>", table_cell_bold),
            Paragraph("OpenCV 4.10 (cv2) + NumPy", table_cell),
            Paragraph("Image Preprocessing & Overlays", table_cell),
            Paragraph("Industry standard C++ optimized image processing for CLAHE, denoising, and bounding box drawing.", table_cell)
        ],
        [
            Paragraph("<b>OCR Engine</b>", table_cell_bold),
            Paragraph("Tesseract 5.4.0 + pytesseract", table_cell),
            Paragraph("Optical Character Recognition", table_cell),
            Paragraph("Open-source, local, zero-cloud dependency, word-level bounding box and confidence output.", table_cell)
        ],
        [
            Paragraph("<b>Symbolic Rule Engine</b>", table_cell_bold),
            Paragraph("Custom Deterministic Python", table_cell),
            Paragraph("Legal Metrology Compliance Logic", table_cell),
            Paragraph("Zero hallucination, 100% explainable, mathematically verifiable, statutory gazette grounded.", table_cell)
        ],
        [
            Paragraph("<b>PDF Report Engine</b>", table_cell_bold),
            Paragraph("ReportLab 4.5.1 Platypus", table_cell),
            Paragraph("Official PDF Notice Generator", table_cell),
            Paragraph("Precision typographic control, court-admissible formatting, multi-page flowable architecture.", table_cell)
        ],
        [
            Paragraph("<b>Word Report Engine</b>", table_cell_bold),
            Paragraph("python-docx 1.1.2", table_cell),
            Paragraph("Editable DOCX Report Generator", table_cell),
            Paragraph("Generates standards-compliant OpenXML documents editable in Microsoft Word and LibreOffice.", table_cell)
        ],
        [
            Paragraph("<b>Frontend Framework</b>", table_cell_bold),
            Paragraph("React 18 + Vite 5", table_cell),
            Paragraph("Single Page Application (SPA)", table_cell),
            Paragraph("Instant Hot Module Replacement, modular component architecture, smooth client-side navigation.", table_cell)
        ],
        [
            Paragraph("<b>Styling System</b>", table_cell_bold),
            Paragraph("Tailwind CSS 3.4", table_cell),
            Paragraph("UI Design & Senior Accessibility", table_cell),
            Paragraph("Utility-first design tokens, responsive layouts, rapid prototyping of senior-friendly visual modes.", table_cell)
        ],
        [
            Paragraph("<b>Database & ORM</b>", table_cell_bold),
            Paragraph("SQLAlchemy 2.0 + SQLite", table_cell),
            Paragraph("Relational Data Persistence", table_cell),
            Paragraph("Zero-configuration local deployment, seamless migration path to PostgreSQL for enterprise production.", table_cell)
        ],
        [
            Paragraph("<b>Auth & Security</b>", table_cell_bold),
            Paragraph("PyJWT + Passlib + hashlib", table_cell),
            Paragraph("Authentication & RBAC", table_cell),
            Paragraph("Stateless JSON Web Tokens with salted SHA-256 password hashing and role enforcement.", table_cell)
        ]
    ]

    t_st = Table(stack_data, colWidths=[100, 120, 140, 180])
    t_st.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_st)
    story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # PART 16: TECHNICAL DESIGN DECISIONS
    # =========================================================================
    add_part_header("16", "Technical Design Decisions & Trade-Offs", "Key architectural choices, rationales, benefits, trade-offs, and discarded alternatives.")

    decisions = [
        ("Decision 1: Deterministic Rule Engine vs Generative LLM",
         "Why Chosen: In statutory legal enforcement, decisions must be 100% reproducible, explainable, and legally defensible in court. LLMs suffer from non-deterministic hallucinations, token limits, and high API costs.",
         "Benefit: Guaranteed correctness, zero hallucination, sub-millisecond execution, mathematically verifiable USP checks.",
         "Trade-off: Requires manual rule definition derived from gazette amendments rather than zero-shot prompt parsing.",
         "Discarded Alternative: Multi-modal LLM (GPT-4o / Claude 3.5 Sonnet) prompt-based compliance checking."),

        ("Decision 2: Local OpenCV + Tesseract Pipeline vs Cloud Vision APIs",
         "Why Chosen: Enforcement officers frequently operate in remote wholesale markets, agricultural mandis, and border checkpoints with intermittent internet connectivity.",
         "Benefit: 100% offline edge capability, zero recurring per-image API costs, absolute data privacy for confidential packaging audits.",
         "Trade-off: Tesseract requires dedicated pre-processing (CLAHE, deskewing) to match cloud OCR accuracy on noisy images.",
         "Discarded Alternative: Google Cloud Vision API / AWS Textract."),

        ("Decision 3: Dual Report Generation (ReportLab PDF + python-docx DOCX)",
         "Why Chosen: Government legal proceedings require both an immutable official document (PDF) and an editable working notice (Word) for legal clerks to append court case numbers.",
         "Benefit: Satisfies both formal court archival requirements and internal legal drafting workflows simultaneously.",
         "Trade-off: Requires maintaining two separate template generation codebases.",
         "Discarded Alternative: Single HTML-to-PDF headless browser conversion (Puppeteer/Weasyprint)."),

        ("Decision 4: Spatial Line Grouping Parser vs Raw Text Regex",
         "Why Chosen: Packaging text is arranged in distinct visual clusters (e.g. price block, manufacturer block). Searching raw unstructured strings can confuse adjacent labels.",
         "Benefit: Binds bounding box coordinates directly to extracted declaration tokens, enabling precision visual evidence card cropping.",
         "Trade-off: Slightly higher memory consumption during line aggregation.",
         "Discarded Alternative: Flat string regex over concatenated OCR text.")
    ]

    for dec_title, dec_why, dec_ben, dec_to, dec_alt in decisions:
        story.append(Paragraph(f"<b>{dec_title}</b>", section_heading_style))
        story.append(Paragraph(f"• <b>Rationale:</b> {dec_why}", body_style))
        story.append(Paragraph(f"• <b>Primary Benefit:</b> {dec_ben}", body_style))
        story.append(Paragraph(f"• <b>Architectural Trade-off:</b> {dec_to}", body_style))
        story.append(Paragraph(f"• <b>Alternative Considered:</b> {dec_alt}", body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 4))

    # =========================================================================
    # PART 17: BRUTALLY HONEST LIMITATIONS
    # =========================================================================
    add_part_header("17", "Brutally Honest Limitations", "Realistic appraisal of current prototype boundaries and engineering remediation pathways.")

    story.append(Paragraph("True engineering maturity requires acknowledging exact system boundaries and failure modes. PRAMAN AI's known prototype limitations include:", body_style))
    story.append(Spacer(1, 4))

    limitations = [
        [Paragraph("<b>Prototype Limitation</b>", table_cell_header), Paragraph("<b>Underlying Technical Cause</b>", table_cell_header), Paragraph("<b>Operational Impact</b>", table_cell_header), Paragraph("<b>Production Roadmap Fix</b>", table_cell_header)],
        [
            Paragraph("<b>Single-Surface Image Input</b>", table_cell_bold),
            Paragraph("Current pipeline processes one 2D image per scan. Large boxes have declarations spread across 4 sides.", table_cell),
            Paragraph("Inspector must scan front panel first, then scan back/side panel separately.", table_cell),
            Paragraph("Multi-image aggregation session linking front, back, and side surfaces into one inspection audit ID.", table_cell)
        ],
        [
            Paragraph("<b>Highly Stylized Artistic Fonts</b>", table_cell_bold),
            Paragraph("Tesseract is trained on standard print typography. Novel decorative brand fonts can cause misreads.", table_cell),
            Paragraph("Brand name may be missed; generic commodity name parser takes precedence.", table_cell),
            Paragraph("Fine-tune custom lightweight OCR model (CRNN / PaddleOCR) on Indian retail packaging dataset.", table_cell)
        ],
        [
            Paragraph("<b>Severe Cylindrical Distortion</b>", table_cell_bold),
            Paragraph("Labels on small bottles/cans curve sharply at edges, compressing character aspect ratios.", table_cell),
            Paragraph("Text at extreme periphery may yield lower confidence scores.", table_cell),
            Paragraph("3D cylindrical unrolling mesh transform in OpenCV preprocessing before OCR execution.", table_cell)
        ],
        [
            Paragraph("<b>Regional Dialect Packaging</b>", table_cell_bold),
            Paragraph("English dataset is primary. Packaging in pure Tamil, Bengali, or Gujarati requires Indic OCR models.", table_cell),
            Paragraph("Non-English text triggers manual officer verification warning.", table_cell),
            Paragraph("Integrate Bhashini / Indic-Tesseract language packs for all 22 official Indian languages.", table_cell)
        ],
        [
            Paragraph("<b>SQLite In-Memory Concurrency</b>", table_cell_bold),
            Paragraph("SQLite database is optimized for local single-file storage; concurrent write locks occur under high load.", table_cell),
            Paragraph("Sufficient for prototype; limits simultaneous multi-user writes in large regional deployments.", table_cell),
            Paragraph("Migrate to PostgreSQL with connection pooling (PgBouncer) for national-scale deployment.", table_cell)
        ]
    ]

    t_lim = Table(limitations, colWidths=[110, 140, 140, 150])
    t_lim.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1B33")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_lim)
    story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # PART 18: SECURITY & AUDIT ARCHITECTURE
    # =========================================================================
    add_part_header("18", "Security & Audit Architecture", "Current cryptographic posture and production enterprise security roadmap.")

    story.append(Paragraph("Security in PRAMAN AI is architected around data integrity, evidence preservation, and role authorization:", body_style))
    story.append(Spacer(1, 4))

    sec_topics = [
        ("Current Authentication Implementation", "Uses stateless JWT tokens signed with HMAC-SHA256. Passwords stored using salted SHA-256 hashes. Passwords never transmitted in clear text. Tokens expire after 24 hours."),
        ("Role-Based Access Control (RBAC)", "FastAPI dependency injection enforces strict role checks (ADMIN, SUPERVISOR, INSPECTOR). Unauthorized route access returns HTTP 403 Forbidden."),
        ("Immutable Audit Logging", "Every user authentication, packaging scan, report download, and supervisory status change is recorded in the SQL <code>AuditLog</code> table with username, action, entity ID, details, IP address, and UTC timestamp."),
        ("Evidence Image Integrity", "Uploaded packaging images and cropped evidence snippets are given UUID4 filenames, preventing directory traversal attacks or unauthorized file overwrite."),
        ("Production Security Roadmap", "1. Upgrade to asymmetric RSA (RS256) JWT keys with rotation. 2. Integrate Government of India Single Sign-On (Parichay / Jan Parichay). 3. Encrypt uploaded evidence at rest using AES-256. 4. Forward audit logs to append-only WORM cloud storage with cryptographic timestamping.")
    ]

    for st_title, st_desc in sec_topics:
        story.append(Paragraph(f"• <b>{st_title}:</b> {st_desc}", body_style))

    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 19 & 20: SCALABILITY & REAL-WORLD DEPLOYMENT
    # =========================================================================
    add_part_header("19 & 20", "Scalability & Real-World Government Deployment", "Path from hackathon prototype to national-scale Legal Metrology enforcement.")

    story.append(Paragraph("To scale PRAMAN AI across 5,000+ enforcement officers across all Indian States and Union Territories:", body_style))
    story.append(Spacer(1, 4))

    scale_points = [
        ("Cloud Microservices Architecture", "Deploy FastAPI backend as containerized microservices on Kubernetes (EKS / NIC Cloud). Distribute OCR and Computer Vision workloads across asynchronous Celery worker pools backed by Redis message queues."),
        ("Database Scaling & Partitioning", "Migrate from SQLite to PostgreSQL with read replicas and geographic partitioning by State / Enforcement Zone. Use PgBouncer for handling 10,000+ concurrent inspector connections."),
        ("National Centralized Rule Repository", "Maintain a cloud-synchronized Legal Metrology Rule Knowledge Base. When the Ministry issues a new gazette amendment, updating the centralized rule JSON immediately pushes new validation logic to all field inspector devices nationwide."),
        ("Edge-AI Handheld Enforcement Devices", "Package the OpenCV and OCR pipeline into lightweight ONNX / TensorFlow Lite models running on ruggedized Android tablets for offline field audits in remote rural markets. Inspections sync automatically when connectivity is restored."),
        ("Integration with e-Governance Systems", "Connect PRAMAN AI directly with the National Consumer Helpline (NCH), FSSAI FoSCoS portal, and State Legal Metrology Enforcement databases to automatically file formal show-cause notices and track penalty recovery.")
    ]

    for sp_title, sp_desc in scale_points:
        story.append(Paragraph(f"<b>{sp_title}:</b> {sp_desc}", body_style))

    story.append(PageBreak())

    # =========================================================================
    # PART 21: HACKATHON EVALUATOR QUESTIONS (CATEGORIES A TO AL)
    # =========================================================================
    add_part_header("21", "Exhaustive Hackathon Evaluator Questions (A–AL)", "Exhaustive question-and-answer guide organized by technical and domain categories.")

    story.append(Paragraph("This section contains defense preparation questions covering every possible angle from professors, technical evaluators, industry judges, and domain experts.", body_style))
    story.append(Spacer(1, 4))

    qa_list = [
        # Category A: Problem Statement
        ("A", 1, "Problem Statement", 
         "Why can't inspectors just check packaging labels manually? Is this really a major problem in India?",
         "The evaluator wants to verify the genuine social and economic impact of the project.",
         "India has billions of pre-packaged commodities in circulation across retail and e-commerce. Manual inspection takes 15–20 minutes per product, requires remembering over 40 complex gazette amendments, and produces handwritten memos that lack tamper-evident visual proof. PRAMAN AI reduces audit time to under 3 seconds with 100% deterministic accuracy and court-ready visual evidence.",
         "15-20 min manual vs 3-sec automated; 40+ gazette amendments; court-ready visual evidence."),

        ("A", 2, "Problem Statement",
         "What specific legal act and rules govern packaging compliance in India?",
         "Testing domain knowledge of Indian consumer protection laws.",
         "The primary governing statute is the Legal Metrology Act, 2009, enforced through the Legal Metrology (Packaged Commodities) Rules, 2011 (PCR 2011), along with subsequent gazette amendments such as GSR 226(E) for Unit Sale Price and the 2022/2023 Garment and QR Code notifications.",
         "Legal Metrology Act 2009; Packaged Commodities Rules 2011; GSR 226(E); Section 36(1)."),

        # Category B: Innovation
        ("B", 3, "Innovation",
         "What makes PRAMAN AI innovative compared to generic OCR or ChatGPT?",
         "Testing whether you built a wrapper or a specialized engineering solution.",
         "Generic OCR merely extracts unformatted text without legal meaning. ChatGPT and LLMs hallucinate, produce non-deterministic outputs, and cannot be used for court prosecution. PRAMAN AI innovates by combining Computer Vision preprocessing, localized coordinate extraction, a deterministic statutory rule engine derived from 40 gazettes, explainable 0-100 scoring, and automated court-ready PDF/DOCX notice generation.",
         "Hybrid CV + Deterministic Rule Engine; zero hallucination; gazette traceability; court-ready exports."),

        # Category C: AI / ML
        ("C", 4, "AI & Machine Learning",
         "Why did you use a deterministic rule engine instead of training an end-to-end deep learning classifier for compliance?",
         "Critical technical question on architecture decision-making.",
         "In legal enforcement, every decision must be 100% explainable, deterministic, and traceable to a specific statutory section. An end-to-end neural network is a black box that cannot mathematically prove why a product scored 68 vs 96 in court. We use AI for perception (Computer Vision / OCR) and symbolic deterministic logic for statutory evaluation.",
         "Symbolic AI + Neural Perception; legal explainability; court proof; zero black-box bias."),

        # Category D: OCR Engine
        ("D", 5, "OCR Implementation",
         "How does your OCR handle different font sizes and text alignments on complex packaging?",
         "Testing deep understanding of the OCR pipeline.",
         "We utilize Tesseract 5.4.0 with `image_to_data`, extracting word-level bounding boxes and confidence scores. Our engine groups adjacent words into lines based on vertical baseline coordinates and block IDs, merging multi-line address and price clusters into unified semantic tokens.",
         "Word-level bounding boxes; line grouping by baseline; spatial coordinate merging."),

        # Category E: Computer Vision
        ("E", 6, "Computer Vision",
         "What happens if an inspector uploads a tilted or poorly lit package photograph?",
         "Testing robustness of the image preprocessing pipeline.",
         "Our OpenCV preprocessor applies CLAHE to equalize localized lighting and bilateral filtering to reduce grain noise. It then runs Canny edge detection and Probabilistic Hough Transform to calculate the median tilt angle, rotating the affine matrix to deskew the label before OCR execution.",
         "CLAHE contrast equalization; bilateral noise reduction; Hough transform skew correction."),

        # Category F: Information Extraction
        ("F", 7, "Information Extraction",
         "How does the system distinguish between the Manufacturer address and the Consumer Care address?",
         "Testing NLP and token extraction logic.",
         "The DeclarationExtractor uses contextual keyword boundaries and regex lookaheads. Manufacturer parsing looks for 'Manufactured by', 'Packed by', or 'Mfg by' followed by address patterns and PIN codes, cutting off before 'Consumer Care' or 'MRP'. Consumer Care extraction specifically isolates email formats, toll-free 1800 numbers, and 'Helpline' headers.",
         "Contextual boundary parsing; regex lookaheads; keyword cutoff markers."),

        # Category G: Rule Engine
        ("G", 8, "Rule Engine",
         "How do you evaluate Unit Sale Price (USP) compliance under GSR 226(E)?",
         "Testing statutory rule implementation accuracy.",
         "Under GSR 226(E), commodities must declare USP per gram/ml (<1kg/1L) or per kg/L (>=1kg/1L). PRAMAN AI checks for the presence of the declared USP string, parses the numeric unit price, and mathematically verifies that USP equals MRP divided by Net Quantity within a ₹0.05 tolerance.",
         "Metric unit threshold check (<1kg vs >=1kg); mathematical verification (MRP / Quantity)."),

        # Category H: Legal Metrology
        ("H", 9, "Legal Metrology Domain",
         "What is a Section 36(1) Notice under the Legal Metrology Act, 2009?",
         "Testing statutory penalty knowledge.",
         "Section 36(1) prescribes penalties for manufacturing, packing, or selling non-standard pre-packaged commodities. First offenses carry fines up to ₹25,000; second offenses up to ₹50,000; subsequent offenses up to ₹1,00,000 or imprisonment up to one year. PRAMAN AI automatically recommends Section 36(1) notices for critical infractions.",
         "Section 36(1) penalty for non-standard packages; fines up to ₹1 Lakh and imprisonment."),

        # Category I: Nutrition
        ("I", 10, "Nutritional Assessment",
         "Why does PRAMAN AI include nutritional analysis if Legal Metrology is about measurement?",
         "Testing project scope understanding.",
         "While Legal Metrology regulates quantity and consumer declarations, packaging labels increasingly display Nutritional Facts under FSSAI mandate. PRAMAN AI provides a unified inspection studio that extracts 11 nutrients and provides an informational health indicator, strictly distinguishing legal compliance from health assessments.",
         "Dual-purpose enforcement; FSSAI synergy; strictly decoupled from metrology compliance score."),

        # Category J: Architecture
        ("J", 11, "System Architecture",
         "Explain the multi-tier architecture and data flow of PRAMAN AI.",
         "Testing end-to-end architectural clarity.",
         "PRAMAN AI uses a decoupled 3-tier architecture: React 18 SPA frontend, FastAPI asynchronous backend with SQLAlchemy ORM, and a processing pipeline encompassing OpenCV preprocessors, Tesseract OCR, Deterministic Rule Engines, and ReportLab / python-docx report generators.",
         "React 18 frontend; FastAPI ASGI; OpenCV + Tesseract; Deterministic Engine; ReportLab/docx."),

        # Category K: Database
        ("K", 12, "Database Design",
         "What relational models exist in your database schema?",
         "Testing database modeling mastery.",
         "Our schema in `models.py` includes User (RBAC & auth), Product (commodity catalogue), Inspection (master scan record), ExtractedDeclaration (parsed fields), ComplianceResult (rule checks), Violation (actionable infractions), Report (document paths), and AuditLog (immutable event log).",
         "8 core relational tables: User, Product, Inspection, Declarations, Results, Violations, Reports, AuditLog."),

        # Category L: Backend
        ("L", 13, "Backend Performance",
         "How fast is the backend pipeline and what is the processing latency?",
         "Testing performance metrics.",
         "The full backend pipeline—from raw image ingestion, OpenCV enhancement, Tesseract OCR, declaration extraction, rule evaluation, scoring, visual evidence cropping, to database storage—executes in approximately 1.5 to 3.0 seconds on standard x86 CPU hardware.",
         "1.5 to 3.0 seconds end-to-end; CPU-optimized; sub-second report generation."),

        # Category M: Frontend
        ("M", 14, "Frontend & UX",
         "What accessibility features are implemented for enforcement officers?",
         "Testing accessibility and UX design.",
         "PRAMAN AI includes Senior Mode (enlarging base font sizes and tap targets), High Contrast Mode (optimizing contrast for outdoor sunlight), and Web Speech Synthesis Audio Guidance (reading scores and alerts aloud for hands-free operation).",
         "Senior Mode (large text); High Contrast Mode (sunlight); Web Speech Audio Guidance."),

        # Category N: Authentication
        ("N", 15, "Authentication & Security",
         "How is user authentication secured in the application?",
         "Testing security implementation.",
         "We implement stateless JWT tokens using HMAC-SHA256. Passwords are encrypted using salted SHA-256 hashes. Frontend stores the token in LocalStorage and attaches Bearer authorization headers to API requests. 6 pre-seeded official user roles allow instant demonstration.",
         "JWT HS256; Salted SHA-256 hashing; 6 official seeded enforcement credentials."),

        # Category O: Edge Cases
        ("O", 16, "Edge Cases",
         "What happens if an image has multiple prices or crossed-out old MRPs?",
         "Testing robustness against packaging tampering.",
         "The MRP parser searches for explicit currency symbols and tax clauses. If multiple prices or smudging is detected, OCR confidence drops and Rule LM-PCR-05 triggers a VIOLATION or WARNING for dual/smudged MRP, recommending manual physical inspection under Rule 18.",
         "Dual MRP detection; Rule 18 violation; low confidence triggers manual verification."),

        # Category P: Scalability
        ("P", 17, "Scalability",
         "How would you scale this to handle 1 million scans per day across India?",
         "Testing enterprise scalability thinking.",
         "We would deploy the FastAPI backend on Kubernetes with auto-scaling pods, offload OCR processing to asynchronous Celery worker queues backed by Redis, migrate the database to a sharded PostgreSQL cluster with PgBouncer, and cache static assets and reports on Cloudflare CDN.",
         "Kubernetes auto-scaling; Celery + Redis worker queues; Sharded PostgreSQL; CDN caching."),

        # Category Q: Accuracy
        ("Q", 18, "Accuracy & Confidence",
         "How do you measure and report OCR confidence to the inspector?",
         "Testing AI observability.",
         "Tesseract computes individual character confidence scores (0–100). OCREngine aggregates these into average word and line confidence metrics. If average confidence falls below 50%, the UI displays a low-confidence warning badge and flags legibility under Rule 10.",
         "Character-level confidence aggregation; threshold <50% triggers legibility warning."),

        # Category R: Competitors
        ("R", 19, "Existing Solutions",
         "Why can't the government just use barcode scanners or GS1 databases?",
         "Testing comparative domain understanding.",
         "Barcodes only verify digital database entries registered by the manufacturer; they cannot detect physical packaging violations like smudged MRPs, missing local addresses, prohibited 'Jumbo' qualifiers, or unprinted tax clauses. PRAMAN AI audits the physical package as seen by the consumer.",
         "Barcodes verify registry data; PRAMAN AI audits physical packaging ground-truth."),

        # Category S: Reports
        ("S", 20, "Official Reporting",
         "What makes the generated PDF report legally valuable?",
         "Testing understanding of government documentation.",
         "The PDF report is formatted as an official statutory notice under the Ministry of Consumer Affairs header. It includes full metadata, an itemized declarations audit, statutory rule citations from indexed gazettes, cropped visual evidence snippets, and dual officer endorsement signature blocks.",
         "Official Ministry header; itemized audit; gazette citations; evidence snippets; signature blocks.")
    ]

    for cat_code, q_idx, cat_name, q_text, q_why, q_ans, q_key in qa_list:
        story.append(create_qa_card(q_idx, f"Cat {cat_code} • {cat_name}", q_text, q_why, q_ans, q_key))

    story.append(PageBreak())

    # =========================================================================
    # PART 22: HARD TECHNICAL QUESTIONS & TRAPS
    # =========================================================================
    add_part_header("22", "Hard Technical Questions & Trap Defense", "Tough adversarial questions designed to catch candidates off guard.")

    hard_questions = [
        ("Trap 1: How do you handle OCR errors causing false legal prosecutions?",
         "Evaluator is testing risk mitigation and legal safety checks.",
         "PRAMAN AI operates as an <b>Inspector Decision Support System</b> rather than an autonomous prosecuting agent. Every detected violation displays the exact OCR text, character confidence score, and cropped visual evidence card. High-severity infractions require the Designated Enforcement Officer to review the crop card before signing the official PDF notice. Furthermore, low OCR confidence (<50%) automatically marks rules as 'MANUAL_VERIFICATION_REQUIRED' rather than issuing an immediate penalty.",
         "Human-in-the-loop verification; confidence thresholds prevent false penalties; inspector signs notice."),

        ("Trap 2: What happens when two legal metrology gazettes appear to conflict?",
         "Testing understanding of statutory hierarchy and amendment precedence.",
         "Under Indian administrative law, specific subsequent amendments override general earlier rules (lex posterior derogat priori). For example, GSR 226(E) introduced Unit Sale Price as mandatory, overriding older package format norms. In PRAMAN AI, our 12 rule definitions represent the latest consolidated statutory ground truth from all 40 gazettes through 2026, with exact gazette PDF file traceability.",
         "Lex posterior legal principle; latest gazette supersedes older rules; 40 indexed PDFs."),

        ("Trap 3: How do you distinguish between absence of evidence and evidence of absence?",
         "Testing deep logical modeling in information extraction.",
         "If the OCR engine has high confidence (>85%) across the entire package surface and a mandatory declaration like 'Inclusive of all taxes' is not found, the system registers <b>Evidence of Absence</b> (Statutory Violation). If overall OCR confidence is low (<50%) due to blur or poor lighting, the system registers <b>Absence of Evidence</b> and flags the item for manual inspector verification under Rule 10.",
         "High confidence + missing token = Violation; Low confidence = Manual Review Required."),

        ("Trap 4: Why not just run a lightweight multimodal LLM like Moondream or LLaVA on the edge?",
         "Testing why you didn't adopt newer vision-language trends.",
         "While multimodal VLMs are impressive for general captioning, they lack deterministic legal verification. They cannot perform precise arithmetic validation (verifying USP = MRP / Quantity to 2 decimal places), their bounding box coordinates frequently drift, and they cannot produce explainable mathematical proofs needed to defend a prosecution in consumer court.",
         "VLMs fail precision arithmetic; bounding box drift; lack statutory explainability.")
    ]

    for h_title, h_why, h_ans, h_key in hard_questions:
        story.append(create_qa_card(h_title.split(":")[0], "Technical Defense", h_title.split(":")[1], h_why, h_ans, h_key))

    story.append(Spacer(1, 6))

    # =========================================================================
    # PART 23: DEMO QUESTIONS & LIVE INTERRUPTIONS
    # =========================================================================
    add_part_header("23", "Demo Questions & Live Interruption Preparation", "Realistic questions asked by evaluators while testing the live running application.")

    demo_questions = [
        ("Demo Q1: Where did this extracted MRP come from on the packaging image?",
         "Point to the Visual Evidence tab or Declarations table on screen. Show how the extracted MRP (e.g. ₹230.00) matches the green bounding box on the price block of the packaging image, displaying a 95% confidence rating."),
        ("Demo Q2: Why is the Sunflower Oil sample flagged as NON-COMPLIANT if it has an MRP?",
         "Explain that while MRP is declared, the mandatory statutory clause '(inclusive of all taxes)' is missing, and the statutory consumer care helpline/email was omitted under Rule 6(1)(f), reducing the score to 68/100."),
        ("Demo Q3: Why does the Namkeen pack score so low (32/100)?",
         "Point out the CRITICAL VIOLATION under Rule 6(1)(c) and Rule 11: using the prohibited qualifying expression 'Jumbo Saver Pack' in place of standard SI metric units (e.g. 500g), alongside missing manufacturer address and missing Country of Origin."),
        ("Demo Q4: Can I edit the inspection report before issuing it to the company?",
         "Click 'Export DOCX'. Demonstrate that PRAMAN AI generates an editable Word document containing all findings, allowing officers to customize notice text, case numbers, and legal hearing dates.")
    ]

    for dq_title, dq_desc in demo_questions:
        story.append(Paragraph(f"<b>{dq_title}</b>", sub_section_heading_style))
        story.append(Paragraph(dq_desc, body_style))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # =========================================================================
    # PART 24: PERFECT DEMO WALKTHROUGH SCRIPT
    # =========================================================================
    add_part_header("24", "Perfect Demo Walkthrough Script", "Click-by-click, say-by-say presentation script for a 3-minute winning hackathon demo.")

    story.append(Paragraph("Follow this exact step-by-step presentation script during your evaluation demo:", body_style))
    story.append(Spacer(1, 4))

    script_steps = [
        ("0:00 - 0:30 | Introduction & Login",
         "1. Display the Login Page. Click the 1-click official user card for <b>Soutik (Head Admin)</b>.<br/>"
         "2. <b>What to Say:</b> <i>'Respected Evaluators, PRAMAN AI transforms Legal Metrology compliance in India from a 20-minute manual paperwork bottleneck into a 3-second automated audit. We are logging in as Authorized Enforcement Officer Soutik.'</i>"),

        ("0:30 - 1:00 | Dashboard & Scan Studio Initiation",
         "1. Show Executive Dashboard with compliance rate gauge, top violations chart, and state-wide scan metrics.<br/>"
         "2. Click <b>'Start Packaging Scan'</b> to enter the Scan Packaging Studio.<br/>"
         "3. <b>What to Say:</b> <i>'Our dashboard provides state-wide enforcement visibility. In our Scan Studio, inspectors can upload live package photos or choose statutory benchmark scenarios.'</i>"),

        ("1:00 - 1:45 | Executing AI Pipeline on Sample 1 (Compliant Atta)",
         "1. Select <b>Sample 1: Chakki Fresh Atta (5 kg)</b>.<br/>"
         "2. Click <b>'Execute Legal Metrology Inspection'</b>. Watch the 5-stage progress indicator.<br/>"
         "3. System redirects to Inspection Detail page showing Score: <b>96/100 (COMPLIANT)</b>.<br/>"
         "4. <b>What to Say:</b> <i>'In under 2 seconds, OpenCV deskewed the image, Tesseract extracted word coordinates, and our deterministic rule engine verified all 12 gazette rules. Net quantity (5.0 kg), MRP with tax clause, and calculated USP (₹46.00/kg) all pass.'</i>"),

        ("1:45 - 2:15 | Testing Non-Compliant Sample 3 (Critical Namkeen)",
         "1. Return to Scan Studio, select <b>Sample 3: Desi Namkeen Pack</b>, and execute inspection.<br/>"
         "2. Detail view shows Score: <b>32/100 (CRITICAL VIOLATION - NON-COMPLIANT)</b>.<br/>"
         "3. Click <b>Visual Evidence</b> tab to show red bounding box on prohibited 'Jumbo Saver Pack'.<br/>"
         "4. <b>What to Say:</b> <i>'Notice how PRAMAN AI immediately catches non-standard misleading expressions under Rule 11 and flags missing manufacturer address, generating an immediate Section 36(1) notice recommendation.'</i>"),

        ("2:15 - 2:45 | Official Reports & Rule Library Traceability",
         "1. Click <b>'Download Official PDF'</b>. Open the generated Court-Ready ReportLab PDF notice.<br/>"
         "2. Click <b>'Rule Library (40 PDFs)'</b> in sidebar to demonstrate ground-truth gazette linkage.<br/>"
         "3. <b>What to Say:</b> <i>'Every finding links directly to our index of 40 official gazette PDFs. With one click, the officer exports an official court-ready statutory notice complete with visual evidence and signature blocks.'</i>"),

        ("2:45 - 3:00 | Accessibility & Wrap Up",
         "1. Toggle <b>Senior Mode</b> and <b>High Contrast</b> in the top navbar.<br/>"
         "2. Click Audio Guidance to play speech synthesis.<br/>"
         "3. <b>What to Say:</b> <i>'With senior-friendly accessibility and immutable audit trails, PRAMAN AI is ready for deployment across India. Thank you!'</i>")
    ]

    for sc_time, sc_content in script_steps:
        story.append(Paragraph(f"<b>{sc_time}</b>", section_heading_style))
        story.append(Paragraph(sc_content, body_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # PART 25, 26, 27, 28: PITCHES, PROFESSOR EXPLANATION, CHEAT SHEET, SELF-TEST
    # =========================================================================
    add_part_header("25 & 26", "Elevator Pitches & Academic Architecture", "Concise pitch scripts and systems engineering explanation for technical professors.")

    story.append(Paragraph("<b>Explain It to a Professor (Systems & Academic Perspective):</b>", section_heading_style))
    story.append(Paragraph("<i>'PRAMAN AI is an applied Computer Vision and Symbolic AI platform for regulatory document validation. From an engineering perspective, it solves a domain-specific Document Visual Question Answering (DocVQA) problem without the non-deterministic latency and hallucination risks of Large Language Models. The perceptual pipeline uses OpenCV adaptive histogram equalization and Hough transform deskewing to feed normalized pixel buffers into Tesseract 5.4. Spatial line aggregation reconstructs bounding box coordinate topologies. Our deterministic symbolic rule engine executes constraint-satisfaction algorithms across 12 statutory gazette rule groups, performing arithmetic verification on Unit Sale Prices and regular-expression pattern matching on statutory clauses. The output is a weighted, explainable scalar score (0–100) and an automated PDF/DOCX artifact compiled via flowable document layout engines.'</i>", body_style))
    story.append(Spacer(1, 6))

    add_part_header("27", "Quick Revision Cheat Sheet", "Essential facts, statutory references, and core metrics for last-minute revision.")

    cheat_sheet_data = [
        [Paragraph("<b>Statutory Ground Truth</b>", table_cell_bold), Paragraph("Legal Metrology Act, 2009 & Packaged Commodities Rules, 2011 (40 Official Gazettes Indexed)", table_cell)],
        [Paragraph("<b>Core Penalty Statute</b>", table_cell_bold), Paragraph("Section 36(1) of LM Act 2009 (Fines ₹25,000 to ₹1,00,000 / Imprisonment up to 1 year)", table_cell)],
        [Paragraph("<b>Mandatory Declarations</b>", table_cell_bold), Paragraph("1. Mfr Name & Address, 2. Generic Name, 3. Net Qty (SI units), 4. Mfg Date, 5. MRP (incl. taxes), 6. USP, 7. Consumer Care (Email & Tel), 8. Country of Origin, 9. Garment Size", table_cell)],
        [Paragraph("<b>Scoring Distribution</b>", table_cell_bold), Paragraph("Completeness (40%), Value & Metric Units (25%), Price & USP (15%), Consumer Care & COO (10%), Legibility (10%)", table_cell)],
        [Paragraph("<b>Decision Thresholds</b>", table_cell_bold), Paragraph("Score >= 85 & 0 violations = COMPLIANT; Score < 70 OR >=1 critical violation = NON-COMPLIANT", table_cell)],
        [Paragraph("<b>Benchmark Samples</b>", table_cell_bold), Paragraph("Sample 1 Atta: ~96 (COMPLIANT) | Sample 2 Oil: ~68 (NON-COMPLIANT) | Sample 3 Namkeen: ~32 (CRITICAL VIOLATION)", table_cell)],
        [Paragraph("<b>Authorized Users</b>", table_cell_bold), Paragraph("Soutik (Head Admin - 001), Sayantan (Supervisor - 102), Jiya (Inspector - 203), Rimi (Admin - 004), Debopriya (Supervisor - 105), Arkadip (Inspector - 206)", table_cell)],
        [Paragraph("<b>Tech Stack</b>", table_cell_bold), Paragraph("Python 3.12, FastAPI, React 18, Vite, OpenCV 4.10, Tesseract 5.4, ReportLab 4.5, python-docx, SQLite", table_cell)]
    ]

    t_cs = Table(cheat_sheet_data, colWidths=[150, 390])
    t_cs.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0B1B33")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_cs)
    story.append(Spacer(1, 6))

    add_part_header("28", "Questions We Must Be Able to Answer (Team Self-Test)", "Final readiness checklist before facing the hackathon judging panel.")

    self_test = [
        "1. Can you explain why Unit Sale Price (USP) is mandatory under GSR 226(E) and how our system checks its math?",
        "2. Can you show where in the code bounding box coordinates are converted into cropped evidence JPEG snippets?",
        "3. Can you explain why a high-fat snack can be legally compliant under Metrology while scoring 'LESS HEALTHY' in Nutrition?",
        "4. Can you demonstrate the difference in UI capabilities between Soutik (Admin), Sayantan (Supervisor), and Jiya (Inspector)?",
        "5. Can you explain how our OpenCV preprocessor uses CLAHE and Hough transform to handle uneven lighting and skew?",
        "6. Can you download both the PDF and DOCX reports live during the demo without any server latency?"
    ]

    for st_item in self_test:
        story.append(Paragraph(f"• <b>{st_item}</b>", body_style))

    story.append(Spacer(1, 10))
    add_callout(
        "FINAL PREPARATION DIRECTIVE",
        "All team members must review this dossier thoroughly. Demonstrate confidence, emphasize deterministic legal explainability over AI hype, showcase live visual evidence crops, and highlight the 40 indexed statutory gazettes. Good luck!",
        bg_color="#FEF2F2", border_color="#EF4444", title_color="#B91C1C"
    )

    # Build document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == "__main__":
    out_pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PRAMAN_AI_Technical_Hackathon_Evaluation_Dossier.pdf")
    build_pdf(out_pdf_path)
