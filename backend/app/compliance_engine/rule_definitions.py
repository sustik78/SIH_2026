"""
PRAMAN AI - Legal Metrology Compliance Rule Definitions
Derived directly from the 40 Legal Metrology Act 2009 & Packaged Commodities Rules (PCR 2011 & Gazette Amendments) dataset.
"""

from typing import List, Dict, Any

COMPLIANCE_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "LM-PCR-01",
        "rule_name": "Manufacturer / Packer / Importer Name & Complete Address",
        "category": "Identity & Origin",
        "requirement": "Every pre-packaged commodity must declare the name and complete address of the manufacturer, or the packer (if not manufactured by them), or the importer (if imported).",
        "required_declaration": "Manufacturer / Packer / Importer Details",
        "validation_logic": "Must contain business entity identifier and complete address with identifiable locality/city, state, and pin code.",
        "severity": "HIGH",
        "source_document": "8(xii)_0_1732871346.pdf & PCR_1732871549.pdf",
        "source_section": "Rule 6(1)(a) & GSR 226(E)",
        "explanation": "Consumers and enforcement authorities must be able to trace the legal entity responsible for the packaging, quality, and quantity of the commodity.",
        "exemptions": "For small packages under Rule 26 where space is constrained, manufacturer name must still be legible on outer or digital display."
    },
    {
        "rule_id": "LM-PCR-02",
        "rule_name": "Common or Generic Name of the Commodity",
        "category": "Product Identification",
        "requirement": "The package shall bear the common or generic name of the commodity contained therein.",
        "required_declaration": "Generic / Commodity Name",
        "validation_logic": "Must explicitly state the recognized commodity name (e.g. Wheat Flour / Atta, Basmati Rice, Mustard Oil, Cotton Shirt) rather than solely a brand trade-name.",
        "severity": "HIGH",
        "source_document": "8(xii)_0_1732871346.pdf",
        "source_section": "Rule 6(1)(b)",
        "explanation": "Prevents misleading consumers about the actual nature and contents of the packaged item.",
        "exemptions": "None"
    },
    {
        "rule_id": "LM-PCR-03",
        "rule_name": "Net Quantity in Standard Units of Weight/Measure",
        "category": "Quantity & Measurement",
        "requirement": "Net quantity must be declared in standard metric units (g, kg, ml, L, m, cm, mm, or N/pieces). Qualifiers like 'Jumbo', 'Family Pack', 'Super Saver' without standard metric quantity are strictly prohibited.",
        "required_declaration": "Net Quantity",
        "validation_logic": "Must contain numeric magnitude followed by recognized SI unit symbol or unit word. Non-metric units (lbs, oz, feet) are non-compliant.",
        "severity": "CRITICAL",
        "source_document": "8(xii)_0_1732871346.pdf & 2023.12.29 SOP for Edible Oil & Fats",
        "source_section": "Rule 6(1)(c), Rule 11, 12, 13",
        "explanation": "Core metrological requirement to ensure fair trade and accurate measurement for the consumer.",
        "exemptions": "Packages <= 10g or 10ml (other than pan masala/tobacco) under Rule 26(a)."
    },
    {
        "rule_id": "LM-PCR-04",
        "rule_name": "Month and Year of Manufacture / Pre-packing / Import",
        "category": "Dates & Freshness",
        "requirement": "The package shall declare the month and year in which the commodity is manufactured or pre-packed or imported.",
        "required_declaration": "Date of Manufacture / Packing / Import",
        "validation_logic": "Must contain valid Month and Year declaration (e.g. MM/YYYY, Month YYYY, or DD/MM/YYYY) preceded by 'Mfg Date', 'Pkd Date', 'Mfd on', or 'Packed on'.",
        "severity": "HIGH",
        "source_document": "8(xii)_0_1732871346.pdf",
        "source_section": "Rule 6(1)(d)",
        "explanation": "Ensures freshness, shelf-life verification, and enforcement of packaging timelines.",
        "exemptions": "Specific commodities exempted under Rule 26 or where Best Before / Expiry is specifically mandated under FSSAI."
    },
    {
        "rule_id": "LM-PCR-05",
        "rule_name": "Maximum Retail Price (MRP) & Inclusive of All Taxes",
        "category": "Pricing & Taxes",
        "requirement": "The retail sale price shall be declared as 'Maximum Retail Price ₹... (inclusive of all taxes)' or 'MRP ₹... incl. of all taxes'. Dual MRP, smudging, or selling above MRP is punishable.",
        "required_declaration": "MRP Declaration",
        "validation_logic": "Must specify Indian Rupees symbol (₹ or Rs.) followed by price amount and explicit tax declaration string ('incl. of all taxes' or 'inclusive of all taxes').",
        "severity": "CRITICAL",
        "source_document": "8(xii)_0_1732871346.pdf & 230946_1732871433.pdf",
        "source_section": "Rule 6(1)(e) & Rule 18",
        "explanation": "Protects consumers against overcharging and ensures all applicable GST and local levies are included.",
        "exemptions": "Institutional consumer packages marked 'Not for Retail Sale'."
    },
    {
        "rule_id": "LM-PCR-06",
        "rule_name": "Unit Sale Price (USP) Declaration",
        "category": "Pricing & Taxes",
        "requirement": "Unit Sale Price rounded off to nearest 2 decimal places must be declared on every pre-packaged commodity: per gram (<1kg), per kg (>=1kg), per ml (<1L), per litre (>=1L), per metre, or per number.",
        "required_declaration": "Unit Sale Price (USP)",
        "validation_logic": "Must display unit sale price in format '₹ X / g', '₹ X / kg', '₹ X / ml', '₹ X / L' or '₹ X / N'. Value must mathematically correspond to MRP divided by Net Quantity.",
        "severity": "HIGH",
        "source_document": "GSR226_1732871458.pdf, 2023.10.6 amendment in PCR_1732871982.pdf & Amendment of PCR ext till 31.12.2023 (1)_1732871950.pdf",
        "source_section": "Rule 6(1)(11) & GSR 226(E)",
        "explanation": "Enables consumers to make direct price-to-quantity comparisons across different brands and package sizes.",
        "exemptions": "Single item packages where net quantity equals 1 unit or packages < 10g/10ml where exempted."
    },
    {
        "rule_id": "LM-PCR-07",
        "rule_name": "Consumer Care & Grievance Redressal Mechanism",
        "category": "Consumer Protection",
        "requirement": "The package shall declare the name, complete address, telephone number / helpline, and email address of the person/officer who can be contacted by the consumer in case of complaints.",
        "required_declaration": "Consumer Care Contact Details",
        "validation_logic": "Must contain at least two modes of direct contact: valid Email address AND Telephone / Toll-Free Number, along with customer care address.",
        "severity": "HIGH",
        "source_document": "8(xii)_0_1732871346.pdf & 2022 3rd amendment in PCR Garments_1733228786.pdf",
        "source_section": "Rule 6(1)(f) & Rule 2(aa)",
        "explanation": "Guarantees statutory consumer right to grievance redressal for defective or under-filled packages.",
        "exemptions": "None."
    },
    {
        "rule_id": "LM-PCR-08",
        "rule_name": "Country of Origin (COO) Declaration",
        "category": "Identity & Origin",
        "requirement": "For imported commodities and products marketed on e-commerce platforms, the name of the Country of Origin / Country of Manufacture must be explicitly declared.",
        "required_declaration": "Country of Origin",
        "validation_logic": "Must declare 'Country of Origin: <Country>' or 'Made in <Country>' or 'Manufactured in <Country>'.",
        "severity": "HIGH",
        "source_document": "2026.02.13 PCR 1st COO Filter on e-commerce websites_1771231030.pdf & PCR_3rd_29May2026_1780376045.pdf",
        "source_section": "Rule 6(1)(da) & Rule 6(4)",
        "explanation": "Mandates clear origin disclosure for trade transparency and import tracking.",
        "exemptions": "Domestic goods where manufacturer address explicitly includes India, though explicit COO is best practice."
    },
    {
        "rule_id": "LM-PCR-09",
        "rule_name": "Garment & Hosiery Standard Size & Piece Count",
        "category": "Category Specific",
        "requirement": "For readymade garments or hosiery goods, mandatory declarations include standard international/Indian size (S, M, L, XL, XXL, etc.) or dimensional measurements (chest/waist/length in cm/inches) and piece count.",
        "required_declaration": "Size & Piece Count",
        "validation_logic": "When product is apparel/garment, size code or dimensional metric + '1 N' or piece count must be declared.",
        "severity": "MEDIUM",
        "source_document": "2022 3rd amendment in PCR Garments_1733228786.pdf & LM_Advisory_for_Readymade_Garments_0_1732710356.pdf",
        "source_section": "3rd Amendment 2022 / GSR 858(E)",
        "explanation": "Streamlines apparel declarations allowing size codes and reducing unnecessary packaging text.",
        "exemptions": "Non-garment commodities."
    },
    {
        "rule_id": "LM-PCR-10",
        "rule_name": "Principal Display Panel (PDP) & Minimum Numeral Height",
        "category": "Display & Legibility",
        "requirement": "Mandatory declarations must appear on the Principal Display Panel with minimum numeral and letter height proportional to net quantity / panel area (e.g. >=1.0mm for <=50g, >=2.0mm for 50g-200g, >=4.0mm for 200g-1kg, >=6.0mm for >1kg) and maintain sharp contrast.",
        "required_declaration": "PDP Numeral Height & Contrast",
        "validation_logic": "Bounding box height of text numerals and background contrast analysis must meet minimum legibility thresholds.",
        "severity": "MEDIUM",
        "source_document": "8(xii)_0_1732871346.pdf & 267107_1761404707.pdf",
        "source_section": "Rule 7 & Rule 9",
        "explanation": "Prevents deceptive micro-lettering or low-contrast text that hides critical consumer information.",
        "exemptions": "Medical devices as per Medical Device Rules 2017 proviso."
    },
    {
        "rule_id": "LM-PCR-11",
        "rule_name": "QR Code & Digital Declarations Proviso",
        "category": "Digital Compliance",
        "requirement": "Where QR code is provided (such as on electronic products or smart packaging), the physical package MUST still declare manufacturer name, commodity name, MRP, net quantity, and consumer care. The QR code must lead to complete digital statutory declarations.",
        "required_declaration": "Physical + QR Code Harmonization",
        "validation_logic": "Presence of QR code does not permit omission of physical MRP, Net Qty, or Consumer Care.",
        "severity": "MEDIUM",
        "source_document": "Notification - Legal Metrology (QR Code)_1732871487.pdf & 2023.6.23 QR Code PCR amendment_1732871827.pdf",
        "source_section": "Rule 6(1)(a) proviso & QR Code Amendment",
        "explanation": "Ensures elderly and offline consumers can still read vital information directly from the packaging without needing a smartphone.",
        "exemptions": "Certain electronic products for technical specifications only."
    },
    {
        "rule_id": "LM-PCR-12",
        "rule_name": "Rule 26 Exemption Verification & Pan Masala Restriction",
        "category": "Exemptions & Special Provisions",
        "requirement": "Packages with net weight <= 10g or <= 10ml are exempt from certain declarations, EXCEPT for Pan Masala and Tobacco products where all declarations remain mandatory regardless of size. Packages > 25kg or 25L are exempt except cement and fertilizer.",
        "required_declaration": "Exemption Applicability Check",
        "validation_logic": "Evaluate package size and category to verify if any claimed exemption is legally valid or constitutes a non-compliant omission.",
        "severity": "LOW",
        "source_document": "2nd PCR Pan Masala_1764736734.pdf & 2023.3.6 farm produce upto 50 kg as per PCR_1732871747.pdf",
        "source_section": "Rule 26 & 2025 Amendment",
        "explanation": "Prevents manufacturers of pan masala or bulk goods from falsely claiming micro-package exemptions.",
        "exemptions": "Qualifying bulk institutional packages as defined in Rule 2(bc)."
    }
]
