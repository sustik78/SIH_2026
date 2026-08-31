"""
PRAMAN AI - Legal Metrology Official Inspection PDF Report Generator
Generates evidence-backed inspection reports using ReportLab.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from datetime import datetime

class PDFReportGenerator:
    @staticmethod
    def generate(
        inspection_data: dict,
        output_filepath: str
    ) -> str:
        """
        Generates a comprehensive Legal Metrology Inspection Report PDF.
        """
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        doc = SimpleDocTemplate(
            output_filepath,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            "GovTitle",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#0F2942"),
            alignment=1
        )
        subtitle_style = ParagraphStyle(
            "GovSubtitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#4B5563"),
            alignment=1
        )
        h2_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1E40AF"),
            spaceBefore=10,
            spaceAfter=6
        )
        cell_style = ParagraphStyle(
            "CellNormal",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#1F2937")
        )
        cell_bold = ParagraphStyle(
            "CellBold",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#111827")
        )
        badge_style_red = ParagraphStyle(
            "BadgeRed",
            parent=styles["Normal"],
            fontSize=10,
            leading=12,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#DC2626")
        )
        badge_style_green = ParagraphStyle(
            "BadgeGreen",
            parent=styles["Normal"],
            fontSize=10,
            leading=12,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#059669")
        )

        story = []

        # 1. Header Banner
        header_text = """
        <b>GOVERNMENT OF INDIA</b><br/>
        <b>MINISTRY OF CONSUMER AFFAIRS, FOOD & PUBLIC DISTRIBUTION</b><br/>
        DEPARTMENT OF CONSUMER AFFAIRS — LEGAL METROLOGY DIVISION
        """
        story.append(Paragraph(header_text, title_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>PRAMAN AI</b> — Packaging Regulations & Automated Metrology Audit Network", subtitle_style))
        story.append(Paragraph("STATUTORY INSPECTION & EVIDENCE-BACKED AUDIT REPORT", ParagraphStyle("SubSub", parent=subtitle_style, fontName="Helvetica-Bold", textColor=colors.HexColor("#1E3A8A"))))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0F2942"), spaceAfter=10))

        # 2. Metadata Table
        status_color = colors.HexColor("#DC2626") if inspection_data.get("compliance_status") == "NON-COMPLIANT" else colors.HexColor("#059669")
        
        meta_data = [
            [
                Paragraph("<b>Inspection ID:</b>", cell_bold),
                Paragraph(str(inspection_data.get("inspection_id", "N/A")), cell_style),
                Paragraph("<b>Inspection Date:</b>", cell_bold),
                Paragraph(datetime.now().strftime("%d-%b-%Y %H:%M IST"), cell_style)
            ],
            [
                Paragraph("<b>Product Name:</b>", cell_bold),
                Paragraph(str(inspection_data.get("product_name", "N/A")), cell_style),
                Paragraph("<b>Enforcement Officer:</b>", cell_bold),
                Paragraph(str(inspection_data.get("inspector_name", "Officer In-charge")), cell_style)
            ],
            [
                Paragraph("<b>Category:</b>", cell_bold),
                Paragraph(str(inspection_data.get("category", "Packaged Commodity")), cell_style),
                Paragraph("<b>Statutory Reference:</b>", cell_bold),
                Paragraph("LM Act 2009 & PCR 2011", cell_style)
            ],
            [
                Paragraph("<b>Compliance Status:</b>", cell_bold),
                Paragraph(f"<b>{inspection_data.get('compliance_status', 'PENDING')}</b>", badge_style_red if inspection_data.get("compliance_status") == "NON-COMPLIANT" else badge_style_green),
                Paragraph("<b>Compliance Score:</b>", cell_bold),
                Paragraph(f"<b>{inspection_data.get('overall_score', 0)} / 100</b>", cell_bold)
            ]
        ]

        meta_table = Table(meta_data, colWidths=[110, 160, 110, 160])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # 3. Decision & Recommended Action
        story.append(Paragraph("1. Compliance Decision & Statutory Action", h2_style))
        decision_box = [
            [
                Paragraph("<b>Regulatory Summary:</b>", cell_bold),
                Paragraph(str(inspection_data.get("decision_summary", "Evaluation complete.")), cell_style)
            ],
            [
                Paragraph("<b>Recommended Action:</b>", cell_bold),
                Paragraph(str(inspection_data.get("recommended_action", "Proceed with standard review.")), cell_style)
            ]
        ]
        decision_table = Table(decision_box, colWidths=[130, 410])
        decision_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF2F2") if inspection_data.get("compliance_status") == "NON-COMPLIANT" else colors.HexColor("#F0FDF4")),
            ("BOX", (0, 0), (-1, -1), 1, status_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(decision_table)
        story.append(Spacer(1, 10))

        # 4. Mandatory Declarations Audit Table
        story.append(Paragraph("2. Mandatory Declarations Audit (Rule 6, PCR 2011)", h2_style))
        decl_headers = [
            Paragraph("<b>Mandatory Declaration</b>", cell_bold),
            Paragraph("<b>Detected Value</b>", cell_bold),
            Paragraph("<b>Status</b>", cell_bold),
            Paragraph("<b>Confidence</b>", cell_bold)
        ]
        decl_rows = [decl_headers]
        for d in inspection_data.get("declarations", []):
            st = "FOUND" if d.get("is_found") else "MISSING"
            st_color = colors.HexColor("#059669") if d.get("is_found") else colors.HexColor("#DC2626")
            decl_rows.append([
                Paragraph(str(d.get("field_name", "")), cell_style),
                Paragraph(str(d.get("detected_value") or "—"), cell_style),
                Paragraph(f"<b>{st}</b>", ParagraphStyle("st", parent=cell_style, textColor=st_color)),
                Paragraph(f"{d.get('confidence_score', 0)}%", cell_style)
            ])
        
        decl_table = Table(decl_rows, colWidths=[140, 240, 80, 80])
        decl_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F2942")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ]))
        story.append(decl_table)
        story.append(Spacer(1, 10))

        # 5. Rule Evaluation & Detected Violations
        story.append(Paragraph("3. Rule Evaluation & Detected Violations", h2_style))
        rule_headers = [
            Paragraph("<b>Rule ID / Name</b>", cell_bold),
            Paragraph("<b>Statutory Reference</b>", cell_bold),
            Paragraph("<b>Status</b>", cell_bold),
            Paragraph("<b>Findings & Explanation</b>", cell_bold)
        ]
        rule_rows = [rule_headers]
        for r in inspection_data.get("results", []):
            st_text = r.get("status", "PASS")
            r_col = colors.HexColor("#059669") if st_text == "PASS" else colors.HexColor("#D97706") if st_text == "WARNING" else colors.HexColor("#DC2626")
            rule_rows.append([
                Paragraph(f"<b>{r.get('rule_id')}</b><br/>{r.get('rule_name')}", cell_style),
                Paragraph(f"<b>{r.get('source_section')}</b><br/><i>{r.get('source_document')}</i>", cell_style),
                Paragraph(f"<b>{st_text}</b><br/>({r.get('severity')})", ParagraphStyle("rcol", parent=cell_style, textColor=r_col)),
                Paragraph(str(r.get("explanation")), cell_style)
            ])

        rules_table = Table(rule_rows, colWidths=[120, 130, 80, 210])
        rules_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ]))
        story.append(rules_table)
        story.append(Spacer(1, 14))

        # 6. Official Endorsement Footer
        sign_box = [
            [
                Paragraph("<b>Inspecting Official Sign & Stamp:</b><br/><br/><br/>_____________________________________<br/>Authorized Legal Metrology Officer", cell_style),
                Paragraph("<b>Supervisory Review Endorsement:</b><br/><br/><br/>_____________________________________<br/>Assistant Controller / Controller", cell_style)
            ]
        ]
        sign_table = Table(sign_box, colWidths=[270, 270])
        sign_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(KeepTogether([sign_table]))

        doc.build(story)
        return output_filepath
