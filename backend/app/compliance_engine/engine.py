"""
PRAMAN AI - Legal Metrology Compliance Rule Engine
Deterministic rule evaluator based on Legal Metrology Act 2009 & Packaged Commodities Rules 2011 dataset.
"""

from typing import Dict, Any, List
from .rule_definitions import COMPLIANCE_RULES

class ComplianceRuleEngine:
    @staticmethod
    def evaluate_compliance(
        declarations: Dict[str, Any],
        image_metrics: Dict[str, Any],
        product_category: str = "General Packaged Food / FMCG"
    ) -> Dict[str, Any]:
        """
        Executes all Legal Metrology compliance checks deterministically.
        """
        results: List[Dict[str, Any]] = []
        violations: List[Dict[str, Any]] = []
        warnings: List[Dict[str, Any]] = []
        passed_checks: List[Dict[str, Any]] = []

        mfr = declarations.get("manufacturer_details", {})
        comm = declarations.get("commodity_name", {})
        net_qty = declarations.get("net_quantity", {})
        mfg_date = declarations.get("mfg_date", {})
        mrp = declarations.get("mrp", {})
        usp = declarations.get("unit_sale_price", {})
        consumer_care = declarations.get("consumer_care", {})
        coo = declarations.get("country_of_origin", {})
        garment_size = declarations.get("garment_size", {})
        qr_present = declarations.get("qr_code_present", False)

        # -------------------------------------------------------------
        # 1. LM-PCR-01: Manufacturer / Packer / Importer Name & Address
        # -------------------------------------------------------------
        rule_01 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-01")
        if mfr.get("found"):
            if mfr.get("has_complete_address"):
                status_01 = "PASS"
                severity_01 = "NONE"
                explanation_01 = f"Manufacturer/Packer identity and address successfully detected: '{mfr.get('value')}'."
            else:
                status_01 = "WARNING"
                severity_01 = "MEDIUM"
                explanation_01 = "Manufacturer name found, but address appears incomplete (missing city/pincode). Manual review advised."
        else:
            status_01 = "VIOLATION"
            severity_01 = rule_01["severity"]
            explanation_01 = "Mandatory declaration of Manufacturer, Packer, or Importer name and address is missing."

        res_01 = ComplianceRuleEngine._build_rule_result(
            rule_01, mfr.get("value") or "Not Detected", "Valid name & complete address with locality/pincode",
            status_01, severity_01, mfr.get("bbox"), explanation_01
        )
        results.append(res_01)

        # -------------------------------------------------------------
        # 2. LM-PCR-02: Common / Generic Commodity Name
        # -------------------------------------------------------------
        rule_02 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-02")
        if comm.get("found"):
            status_02 = "PASS"
            severity_02 = "NONE"
            explanation_02 = f"Generic commodity name detected: '{comm.get('value')}'."
        else:
            status_02 = "VIOLATION"
            severity_02 = rule_02["severity"]
            explanation_02 = "Common or generic name of commodity could not be identified on the packaging."

        res_02 = ComplianceRuleEngine._build_rule_result(
            rule_02, comm.get("value") or "Not Detected", "Explicit generic / common name of commodity",
            status_02, severity_02, comm.get("bbox"), explanation_02
        )
        results.append(res_02)

        # -------------------------------------------------------------
        # 3. LM-PCR-03: Net Quantity in Standard Metric Units
        # -------------------------------------------------------------
        rule_03 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-03")
        if net_qty.get("found"):
            if net_qty.get("is_standard_unit"):
                status_03 = "PASS"
                severity_03 = "NONE"
                explanation_03 = f"Standard net quantity declared in valid metric unit: '{net_qty.get('value')}'."
            else:
                status_03 = "VIOLATION"
                severity_03 = "HIGH"
                explanation_03 = f"Net quantity unit '{net_qty.get('unit')}' is non-metric or prohibited under Rule 11/12."
        else:
            status_03 = "VIOLATION"
            severity_03 = rule_03["severity"]
            explanation_03 = "Mandatory Net Quantity declaration is missing from the package."

        res_03 = ComplianceRuleEngine._build_rule_result(
            rule_03, net_qty.get("value") or "Not Detected", "Valid metric weight/volume/count (g, kg, ml, L, N)",
            status_03, severity_03, net_qty.get("bbox"), explanation_03
        )
        results.append(res_03)

        # -------------------------------------------------------------
        # 4. LM-PCR-04: Month and Year of Manufacture / Packing / Import
        # -------------------------------------------------------------
        rule_04 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-04")
        if mfg_date.get("found"):
            status_04 = "PASS"
            severity_04 = "NONE"
            explanation_04 = f"Date of Manufacture/Packing detected: '{mfg_date.get('value')}'."
        else:
            status_04 = "VIOLATION"
            severity_04 = rule_04["severity"]
            explanation_04 = "Mandatory Month and Year of Manufacture or Pre-packing is missing."

        res_04 = ComplianceRuleEngine._build_rule_result(
            rule_04, mfg_date.get("value") or "Not Detected", "Valid MM/YYYY or Month YYYY manufacturing date",
            status_04, severity_04, mfg_date.get("bbox"), explanation_04
        )
        results.append(res_04)

        # -------------------------------------------------------------
        # 5. LM-PCR-05: Maximum Retail Price (MRP) & Tax Declaration
        # -------------------------------------------------------------
        rule_05 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-05")
        if mrp.get("found"):
            if mrp.get("includes_taxes_text"):
                status_05 = "PASS"
                severity_05 = "NONE"
                explanation_05 = f"MRP declared in Indian Rupees with statutory tax clause: '{mrp.get('value')} (incl. of all taxes)'."
            else:
                status_05 = "VIOLATION"
                severity_05 = "HIGH"
                explanation_05 = f"MRP declared ({mrp.get('value')}), but mandatory 'inclusive of all taxes' / 'incl. of all taxes' clause is missing."
        else:
            status_05 = "VIOLATION"
            severity_05 = rule_05["severity"]
            explanation_05 = "Mandatory Maximum Retail Price (MRP) declaration is missing."

        res_05 = ComplianceRuleEngine._build_rule_result(
            rule_05, mrp.get("value") or "Not Detected", "MRP ₹ XX.XX (inclusive of all taxes)",
            status_05, severity_05, mrp.get("bbox"), explanation_05
        )
        results.append(res_05)

        # -------------------------------------------------------------
        # 6. LM-PCR-06: Unit Sale Price (USP) Declaration & Math Check
        # -------------------------------------------------------------
        rule_06 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-06")
        if usp.get("found"):
            # Check consistency if MRP and Net Qty exist
            math_warning = None
            if mrp.get("numeric_value") and net_qty.get("numeric_value") and net_qty.get("unit"):
                qty = net_qty.get("numeric_value")
                unit = net_qty.get("unit")
                price = mrp.get("numeric_value")
                # Expected USP calculation
                if unit == "g":
                    expected_usp = price / qty
                elif unit == "kg":
                    expected_usp = price / qty
                elif unit == "ml":
                    expected_usp = price / qty
                elif unit == "L":
                    expected_usp = price / qty
                else:
                    expected_usp = price / qty

                detected_usp_val = usp.get("numeric_value", 0)
                diff = abs(detected_usp_val - expected_usp)
                if diff > 0.05 and expected_usp > 0:
                    math_warning = f"Calculated USP (₹{expected_usp:.2f}/{usp.get('unit')}) differs from declared USP ({usp.get('value')})."

            if math_warning:
                status_06 = "WARNING"
                severity_06 = "MEDIUM"
                explanation_06 = f"USP detected ({usp.get('value')}), but discrepancy noted: {math_warning}"
            else:
                status_06 = "PASS"
                severity_06 = "NONE"
                explanation_06 = f"Unit Sale Price correctly declared as '{usp.get('value')}' per GSR 226(E)."
        else:
            # If package is single unit or Net Qty is 1 N, it might be exempt
            if net_qty.get("unit") == "N" and net_qty.get("numeric_value") == 1:
                status_06 = "PASS"
                severity_06 = "NONE"
                explanation_06 = "USP declaration exempted for single unit commodity (1 N)."
            else:
                status_06 = "VIOLATION"
                severity_06 = rule_06["severity"]
                explanation_06 = "Mandatory Unit Sale Price (USP) per g/kg/ml/L/piece is missing on the package."

        res_06 = ComplianceRuleEngine._build_rule_result(
            rule_06, usp.get("value") or "Not Detected", "Unit Sale Price per g/kg/ml/L/N rounded to 2 decimals",
            status_06, severity_06, usp.get("bbox"), explanation_06
        )
        results.append(res_06)

        # -------------------------------------------------------------
        # 7. LM-PCR-07: Consumer Care & Grievance Redressal Mechanism
        # -------------------------------------------------------------
        rule_07 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-07")
        if consumer_care.get("found"):
            if consumer_care.get("has_email") and consumer_care.get("has_phone"):
                status_07 = "PASS"
                severity_07 = "NONE"
                explanation_07 = f"Both Email ({consumer_care.get('email')}) and Phone/Helpline ({consumer_care.get('phone')}) detected."
            elif consumer_care.get("has_email") or consumer_care.get("has_phone"):
                status_07 = "WARNING"
                severity_07 = "LOW"
                explanation_07 = f"Partial consumer care details detected: {consumer_care.get('value')}. Both Email and Phone are recommended."
            else:
                status_07 = "WARNING"
                severity_07 = "MEDIUM"
                explanation_07 = "Consumer care heading detected but contact details could not be parsed with high confidence."
        else:
            status_07 = "VIOLATION"
            severity_07 = rule_07["severity"]
            explanation_07 = "Mandatory Consumer Care contact information (Email / Phone / Address) is missing."

        res_07 = ComplianceRuleEngine._build_rule_result(
            rule_07, consumer_care.get("value") or "Not Detected", "Telephone/Helpline number AND Email address for grievance redressal",
            status_07, severity_07, consumer_care.get("bbox"), explanation_07
        )
        results.append(res_07)

        # -------------------------------------------------------------
        # 8. LM-PCR-08: Country of Origin (COO) Declaration
        # -------------------------------------------------------------
        rule_08 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-08")
        if coo.get("found"):
            status_08 = "PASS"
            severity_08 = "NONE"
            explanation_08 = f"Country of Origin disclosed as '{coo.get('value')}'."
        else:
            # If domestic manufacturer address clearly states India
            if mfr.get("found") and "india" in str(mfr.get("value")).lower():
                status_08 = "PASS"
                severity_08 = "NONE"
                explanation_08 = "Country of Origin inferred as India from domestic manufacturing address."
            else:
                status_08 = "WARNING"
                severity_08 = "MEDIUM"
                explanation_08 = "Country of Origin not explicitly declared. Mandatory for imported products and e-commerce listings."

        res_08 = ComplianceRuleEngine._build_rule_result(
            rule_08, coo.get("value") or "Not Explicitly Declared", "Country of Origin / Made in <Country>",
            status_08, severity_08, coo.get("bbox"), explanation_08
        )
        results.append(res_08)

        # -------------------------------------------------------------
        # 9. LM-PCR-09: Garment Size & Count (if category is Garments)
        # -------------------------------------------------------------
        if "garment" in product_category.lower() or "apparel" in product_category.lower() or "clothing" in product_category.lower():
            rule_09 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-09")
            if garment_size.get("found"):
                status_09 = "PASS"
                severity_09 = "NONE"
                explanation_09 = f"Garment size '{garment_size.get('value')}' declared as per 3rd Amendment 2022."
            else:
                status_09 = "VIOLATION"
                severity_09 = "HIGH"
                explanation_09 = "Mandatory garment size code or dimensional measurement is missing."

            res_09 = ComplianceRuleEngine._build_rule_result(
                rule_09, garment_size.get("value") or "Not Detected", "Standard size (S/M/L/XL) or dimensional measurements in cm/in",
                status_09, severity_09, garment_size.get("bbox"), explanation_09
            )
            results.append(res_09)

        # -------------------------------------------------------------
        # 10. LM-PCR-10: Display Panel Legibility & Contrast
        # -------------------------------------------------------------
        rule_10 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-10")
        quality = image_metrics.get("quality_rating", "GOOD")
        if quality == "GOOD":
            status_10 = "PASS"
            severity_10 = "NONE"
            explanation_10 = f"Display legibility and contrast meet standard visibility criteria (Contrast STD: {image_metrics.get('contrast_std')})."
        elif quality == "FAIR":
            status_10 = "WARNING"
            severity_10 = "LOW"
            explanation_10 = "Moderate contrast detected on packaging panel. Inspection recommended under standard lighting."
        else:
            status_10 = "MANUAL_VERIFICATION_REQUIRED"
            severity_10 = "MEDIUM"
            explanation_10 = "Low image contrast or lighting detected. Inspector verification required for numeral height compliance."

        res_10 = ComplianceRuleEngine._build_rule_result(
            rule_10, f"Contrast STD: {image_metrics.get('contrast_std')}, Lighting: {image_metrics.get('mean_brightness')}",
            "High contrast text with adequate numeral height per Rule 7 & 9",
            status_10, severity_10, None, explanation_10
        )
        results.append(res_10)

        # -------------------------------------------------------------
        # 11. LM-PCR-11: QR Code Harmonization Proviso
        # -------------------------------------------------------------
        rule_11 = next(r for r in COMPLIANCE_RULES if r["rule_id"] == "LM-PCR-11")
        if qr_present:
            # If QR is present, ensure physical mandatory declarations are not missing
            has_missing_essentials = (status_03 == "VIOLATION" or status_05 == "VIOLATION")
            if has_missing_essentials:
                status_11 = "VIOLATION"
                severity_11 = "HIGH"
                explanation_11 = "QR Code detected, but physical package omits essential declarations (Net Qty / MRP) in violation of QR Code Proviso 2023."
            else:
                status_11 = "PASS"
                severity_11 = "NONE"
                explanation_11 = "QR Code present and physical mandatory declarations are preserved."
        else:
            status_11 = "PASS"
            severity_11 = "NONE"
            explanation_11 = "Physical label contains declarations without relying on digital substitutes."

        res_11 = ComplianceRuleEngine._build_rule_result(
            rule_11, "QR Reference Present" if qr_present else "Standard Physical Label",
            "Physical mandatory declarations accompanied by QR where applicable",
            status_11, severity_11, None, explanation_11
        )
        results.append(res_11)

        # Categorize results
        for r in results:
            if r["status"] == "VIOLATION":
                violations.append(r)
            elif r["status"] == "WARNING":
                warnings.append(r)
            elif r["status"] == "PASS":
                passed_checks.append(r)

        return {
            "results": results,
            "violations": violations,
            "warnings": warnings,
            "passed_checks": passed_checks,
            "total_rules_checked": len(results),
            "passed_count": len(passed_checks),
            "warning_count": len(warnings),
            "violation_count": len(violations),
            "critical_violations_count": sum(1 for v in violations if v["severity"] == "CRITICAL")
        }

    @staticmethod
    def _build_rule_result(
        rule_meta: Dict[str, Any],
        detected_value: str,
        expected_condition: str,
        status: str,
        severity: str,
        bbox: Any,
        explanation: str
    ) -> Dict[str, Any]:
        return {
            "rule_id": rule_meta["rule_id"],
            "rule_name": rule_meta["rule_name"],
            "category": rule_meta["category"],
            "requirement": rule_meta["requirement"],
            "required_declaration": rule_meta["required_declaration"],
            "detected_value": detected_value,
            "expected_condition": expected_condition,
            "status": status,
            "severity": severity,
            "bbox": bbox,
            "explanation": explanation,
            "source_document": rule_meta["source_document"],
            "source_section": rule_meta["source_section"],
            "exemptions": rule_meta.get("exemptions", "None")
        }
