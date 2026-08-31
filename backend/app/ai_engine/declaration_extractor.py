"""
PRAMAN AI - Legal Metrology Declaration Extractor
Extracts mandatory packaging declarations from OCR text and bounding boxes using deterministic NLP/regex patterns.
"""

import re
from typing import Dict, Any, List, Optional

class DeclarationExtractor:
    @staticmethod
    def extract_declarations(ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses OCR lines and raw text into structured Legal Metrology declarations.
        Associates each declaration with its bounding box coordinates and confidence score.
        """
        raw_text = ocr_result.get("raw_text", "")
        lines = ocr_result.get("lines", [])
        
        declarations = {
            "commodity_name": DeclarationExtractor._extract_commodity_name(lines, raw_text),
            "manufacturer_details": DeclarationExtractor._extract_manufacturer(lines, raw_text),
            "net_quantity": DeclarationExtractor._extract_net_quantity(lines, raw_text),
            "mfg_date": DeclarationExtractor._extract_mfg_date(lines, raw_text),
            "mrp": DeclarationExtractor._extract_mrp(lines, raw_text),
            "unit_sale_price": DeclarationExtractor._extract_usp(lines, raw_text),
            "consumer_care": DeclarationExtractor._extract_consumer_care(lines, raw_text),
            "country_of_origin": DeclarationExtractor._extract_country_of_origin(lines, raw_text),
            "garment_size": DeclarationExtractor._extract_garment_size(lines, raw_text),
            "qr_code_present": DeclarationExtractor._detect_qr_reference(raw_text)
        }
        
        return declarations

    @staticmethod
    def _find_matching_box(lines: List[Dict[str, Any]], pattern: str) -> Optional[Dict[str, int]]:
        """Finds bounding box coordinates of line matching regex."""
        regex = re.compile(pattern, re.IGNORECASE)
        for line in lines:
            if regex.search(line["text"]):
                return {
                    "x": line["x"],
                    "y": line["y"],
                    "w": line["w"],
                    "h": line["h"]
                }
        return None

    @staticmethod
    def _extract_commodity_name(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        # Look for explicit 'Commodity Name:', 'Commodity:', 'Generic Name:', 'Product Name:'
        pattern = r"(?:Commodity\s*(?:Name)?|Generic\s*Name|Product\s*Name|Item\s*Name)\s*[:\-]?\s*([^\n\r]+)"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            val = match.group(1).strip()
            # Clean trailing label artifacts
            val = re.split(r"(?:Manufactured|Net\s*Q|MRP|Date|FSSAI|Customer)", val, flags=re.IGNORECASE)[0].strip()
            if len(val) >= 3:
                bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Commodity|Generic Name|Product Name)")
                return {"value": val, "found": True, "confidence": 95, "bbox": bbox}

        # Fallback: check prominent lines
        known_commodities = [
            "whole wheat atta", "chakki fresh", "atta", "basmati rice", "sunflower oil",
            "mustard oil", "pure ghee", "iodized salt", "tea", "coffee", "biscuits", "soap",
            "detergent powder", "cotton shirt", "t-shirt", "namkeen", "spicy mixture"
        ]
        for line in lines[:5]:
            lt = line["text"].lower()
            for comm in known_commodities:
                if comm in lt:
                    return {
                        "value": line["text"].strip(),
                        "found": True,
                        "confidence": 85,
                        "bbox": {"x": line["x"], "y": line["y"], "w": line["w"], "h": line["h"]}
                    }

        return {"value": None, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_manufacturer(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        pattern = r"(?:Manufactured\s*(?:&|and)?\s*Packed\s*by|Manufactured\s*by|Mfg\s*(?:&|and)?\s*Pkd\s*by|Mfg\s*by|Packed\s*by|Pkg\s*by|Imported\s*by|Marketed\s*by)\s*[:\-]?\s*([^\n\r]+(?:\n[^\n\r]+)?)"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            raw_val = match.group(0).strip()
            lines_val = [l.strip() for l in raw_val.split("\n") if l.strip()]
            clean_val = " ".join(lines_val)
            # Cut at next major label
            clean_val = re.split(r"(?:Net\s*Q|Date\s*of|MRP|Unit\s*Sale|Consumer)", clean_val, flags=re.IGNORECASE)[0].strip()
            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Manufactured|Packed|Mfg by|Packed by|Marketed by)")
            
            has_pincode = bool(re.search(r"\b\d{6}\b", clean_val))
            has_address = bool(re.search(r"(?:Plot|Industrial|Road|Nagar|Lane|Street|Dist|State|Delhi|Haryana|Mumbai|Pin)", clean_val, re.IGNORECASE))
            
            return {
                "value": clean_val,
                "found": True,
                "has_complete_address": has_pincode or has_address,
                "confidence": 90 if has_pincode else 75,
                "bbox": bbox
            }
            
        return {"value": None, "found": False, "has_complete_address": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_net_quantity(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        # Regex for Net Quantity with standard units: g, kg, ml, l, litre, m, cm, mm, N, units, pcs
        pattern = r"(?:Net\s*(?:Quantity|Qty|Weight|Wt|Vol|Volume|Content|Contents)?)\s*[:\-]?\s*(\d+(?:[\.\,]\d+)?)\s*(kg|g|gm|gms|grams|kilogram|kilograms|ml|millilitre|l|ltr|litre|litres|m|meter|metre|cm|mm|N|units|unit|pcs|pieces)\b"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            val_str = match.group(1).replace(",", ".")
            amount = float(val_str)
            unit = match.group(2).lower()
            # Standardize unit
            std_unit = unit
            if unit in ["g", "gm", "gms", "grams"]: std_unit = "g"
            elif unit in ["kg", "kilogram", "kilograms"]: std_unit = "kg"
            elif unit in ["ml", "millilitre"]: std_unit = "ml"
            elif unit in ["l", "ltr", "litre", "litres"]: std_unit = "L"
            elif unit in ["n", "unit", "units", "pcs", "pieces"]: std_unit = "N"
            elif unit in ["m", "meter", "metre"]: std_unit = "m"
            elif unit == "cm": std_unit = "cm"
            elif unit == "mm": std_unit = "mm"

            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Net\s*(?:Quantity|Qty|Weight|Wt|Vol))")
            if not bbox:
                bbox = DeclarationExtractor._find_matching_box(lines, rf"{amount}\s*{unit}")

            return {
                "value": f"{amount} {std_unit}",
                "numeric_value": amount,
                "unit": std_unit,
                "raw_match": match.group(0),
                "is_standard_unit": std_unit in ["g", "kg", "ml", "L", "m", "cm", "mm", "N"],
                "found": True,
                "confidence": 95,
                "bbox": bbox
            }

        # Check for non-standard prohibited expressions
        non_std_match = re.search(r"(?:Net\s*(?:Quantity|Qty|Weight)?)\s*[:\-]?\s*(Jumbo[^\n\r]*|Family\s*Pack|Mega\s*Saver[^\n\r]*)", raw_text, re.IGNORECASE)
        if non_std_match:
            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Net\s*(?:Quantity|Qty)|Jumbo|Family Pack)")
            return {
                "value": non_std_match.group(1).strip(),
                "numeric_value": None,
                "unit": "NON_STANDARD_EXPRESSION",
                "raw_match": non_std_match.group(0),
                "is_standard_unit": False,
                "found": True,
                "confidence": 85,
                "bbox": bbox
            }

        return {"value": None, "numeric_value": None, "unit": None, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_mfg_date(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        pattern = r"(?:Mfg(?:\.|\s*Date)?|Mfd(?:\.|\s*Date)?|Packed(?:\.|\s*Date)?|Pkd(?:\.|\s*Date)?|Date\s*of\s*(?:Mfg|Manufacture|Packing|Import)|Imported\s*on)\s*[:\-]?\s*([0-3]?\d[\/\-\.][0-1]?\d[\/\-\.]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\-\/]+\d{4}|[0-1]?\d[\/\-]\d{4})"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            date_str = match.group(1).strip()
            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Mfg|Mfd|Packed|Pkd|Date of)")
            return {
                "value": date_str,
                "found": True,
                "raw_match": match.group(0),
                "confidence": 92,
                "bbox": bbox
            }
            
        date_loose = re.search(r"\b(0[1-9]|1[0-2])[\/\-](202[0-9])\b", raw_text)
        if date_loose:
            bbox = DeclarationExtractor._find_matching_box(lines, date_loose.group(0))
            return {
                "value": date_loose.group(0),
                "found": True,
                "raw_match": date_loose.group(0),
                "confidence": 75,
                "bbox": bbox
            }

        return {"value": None, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_mrp(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        # Matches MRP Rs./₹ with inclusive of taxes
        pattern = r"(?:M\.?R\.?P\.?|Maximum\s*Retail\s*Price)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*(\d+(?:[\.\,]\d{1,2})?)"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        has_taxes_clause = bool(re.search(r"(?:incl(?:usive)?\.?\s*of\s*all\s*taxes|incl\.\s*taxes)", raw_text, re.IGNORECASE))
        
        if match:
            val_str = match.group(1).replace(",", ".")
            price = float(val_str)
            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:M\.?R\.?P|Maximum Retail)")
            return {
                "value": f"₹ {price:.2f}",
                "numeric_value": price,
                "includes_taxes_text": has_taxes_clause,
                "found": True,
                "confidence": 95 if has_taxes_clause else 80,
                "bbox": bbox
            }

        loose_pattern = r"(?:₹|Rs\.?)\s*(\d+(?:[\.\,]\d{1,2})?)"
        loose_match = re.search(loose_pattern, raw_text)
        if loose_match:
            price = float(loose_match.group(1).replace(",", "."))
            bbox = DeclarationExtractor._find_matching_box(lines, rf"(?:₹|Rs\.?)\s*{price}")
            return {
                "value": f"₹ {price:.2f}",
                "numeric_value": price,
                "includes_taxes_text": has_taxes_clause,
                "found": True,
                "confidence": 70,
                "bbox": bbox
            }

        return {"value": None, "numeric_value": None, "includes_taxes_text": False, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_usp(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        pattern = r"(?:Unit\s*Sale\s*Price|USP)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*(\d+(?:[\.\,]\d{1,2})?)\s*(?:\/|\s*per\s*)\s*(g|gm|kg|ml|l|ltr|litre|piece|pcs|N|unit|cm|m)\b"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            usp_val = float(match.group(1).replace(",", "."))
            usp_unit = match.group(2).lower()
            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Unit\s*Sale\s*Price|USP)")
            return {
                "value": f"₹ {usp_val:.2f} / {usp_unit}",
                "numeric_value": usp_val,
                "unit": usp_unit,
                "found": True,
                "confidence": 95,
                "bbox": bbox
            }

        loose_usp = re.search(r"(?:₹|Rs\.?)\s*(\d+(?:[\.\,]\d{1,2})?)\s*\/\s*(g|kg|ml|l|N|piece)", raw_text, re.IGNORECASE)
        if loose_usp:
            usp_val = float(loose_usp.group(1).replace(",", "."))
            usp_unit = loose_usp.group(2).lower()
            bbox = DeclarationExtractor._find_matching_box(lines, rf"(\/|per)\s*{usp_unit}")
            return {
                "value": f"₹ {usp_val:.2f} / {usp_unit}",
                "numeric_value": usp_val,
                "unit": usp_unit,
                "found": True,
                "confidence": 80,
                "bbox": bbox
            }

        return {"value": None, "numeric_value": None, "unit": None, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_consumer_care(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", raw_text)
        email = email_match.group(0) if email_match else None

        phone_match = re.search(r"(?:Toll\s*Free|Helpline|Tel|Phone|Contact|Care)?\s*[:\-]?\s*(\b1800[-\s]?\d{2,4}[-\s]?\d{3,4}\b|\b\d{3,5}[-\s]?\d{6,8}\b|\b[6-9]\d{9}\b)", raw_text, re.IGNORECASE)
        phone = phone_match.group(1) if phone_match else None

        has_consumer_header = bool(re.search(r"(?:Consumer\s*Care|Customer\s*Care|Grievance|Feedback|Queries|Complaints)", raw_text, re.IGNORECASE))

        bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Consumer\s*Care|Customer\s*Care|Grievance|1800|@)")

        found = bool(email or phone or has_consumer_header)
        return {
            "value": f"Email: {email or 'Not Detected'} | Phone: {phone or 'Not Detected'}" if found else None,
            "email": email,
            "phone": phone,
            "has_email": bool(email),
            "has_phone": bool(phone),
            "found": found,
            "confidence": 95 if (email and phone) else 80 if (email or phone) else 0,
            "bbox": bbox
        }

    @staticmethod
    def _extract_country_of_origin(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        pattern = r"(?:Country\s*of\s*Origin|Made\s*in|Manufactured\s*in|Product\s*of)\s*[:\-]?\s*([A-Za-z\s]+)"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            country = match.group(1).split("\n")[0].strip()
            country = re.split(r"(?:Mfg|Net|MRP|Batch|Pkg|For|FSSAI)", country, flags=re.IGNORECASE)[0].strip()
            if len(country) >= 3:
                bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Country\s*of\s*Origin|Made\s*in)")
                return {
                    "value": country,
                    "found": True,
                    "confidence": 90,
                    "bbox": bbox
                }

        if re.search(r"\bIndia\b", raw_text, re.IGNORECASE):
            return {
                "value": "India",
                "found": True,
                "confidence": 80,
                "bbox": DeclarationExtractor._find_matching_box(lines, r"\bIndia\b")
            }

        return {"value": None, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _extract_garment_size(lines: List[Dict[str, Any]], raw_text: str) -> Dict[str, Any]:
        pattern = r"(?:Size|Dimensions)\s*[:\-]?\s*([X|S|M|L|XL|XXL|XXXL|\d]{1,5}(?:\s*(?:cm|inches|in))?)"
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            bbox = DeclarationExtractor._find_matching_box(lines, r"(?:Size|Dimensions)")
            return {"value": match.group(1).strip(), "found": True, "confidence": 85, "bbox": bbox}
        return {"value": None, "found": False, "confidence": 0, "bbox": None}

    @staticmethod
    def _detect_qr_reference(raw_text: str) -> bool:
        return bool(re.search(r"(?:QR\s*Code|Scan\s*(?:for|here|to)|Scan\s*QR)", raw_text, re.IGNORECASE))
