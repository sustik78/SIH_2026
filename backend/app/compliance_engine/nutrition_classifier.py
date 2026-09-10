"""
PRAMAN AI - Nutritional Fact Classifier & Informational Health Assessment
Evaluates extracted package nutritional declarations against standard public health & FSSAI/ICMR thresholds.
Provides transparent, explainable health indicators without medical diagnosis.
"""

from typing import Dict, Any, List

class NutritionClassifier:
    @staticmethod
    def classify(nutrition_dict: Dict[str, Any], product_category: str = "General Packaged Commodity") -> Dict[str, Any]:
        """
        Derives an informational health classification based strictly on detected package nutrition facts.
        """
        if not nutrition_dict:
            return NutritionClassifier._insufficient_data()

        # Count detected fields
        detected_fields = [k for k, v in nutrition_dict.items() if isinstance(v, dict) and v.get("found")]
        
        # If fewer than 2 nutritional values are detected, mark as insufficient data
        if len(detected_fields) < 2:
            return NutritionClassifier._insufficient_data()

        positive_factors: List[str] = []
        risk_factors: List[str] = []
        high_risk_count = 0
        positive_count = 0

        # Helper to extract numeric values safely
        def get_val(key: str):
            item = nutrition_dict.get(key)
            if isinstance(item, dict) and item.get("found"):
                return item.get("numeric_value")
            return None

        energy_val = get_val("energy")
        protein_val = get_val("protein")
        sugars_val = get_val("sugars")
        added_sugars_val = get_val("added_sugars")
        fat_val = get_val("fat")
        sat_fat_val = get_val("saturated_fat")
        trans_fat_val = get_val("trans_fat")
        sodium_val = get_val("sodium")
        fiber_val = get_val("fiber")

        # 1. Sodium Evaluation (Standard Threshold: > 600mg / 100g is High, < 120mg is Low)
        if sodium_val is not None:
            if sodium_val >= 600.0:
                risk_factors.append(f"High Sodium: {sodium_val:.0f} mg/100g (Threshold: > 600mg)")
                high_risk_count += 1
            elif sodium_val <= 120.0:
                positive_factors.append(f"Low Sodium: {sodium_val:.1f} mg/100g (Healthy: < 120mg)")
                positive_count += 1

        # 2. Saturated Fat Evaluation (Standard Threshold: > 5.0g / 100g is High, < 1.5g is Low)
        # Note: Pure cooking oils/fats are handled contextually
        is_pure_oil = "oil" in product_category.lower() or "fat" in product_category.lower()
        if sat_fat_val is not None and not is_pure_oil:
            if sat_fat_val >= 5.0:
                risk_factors.append(f"High Saturated Fat: {sat_fat_val:.1f} g/100g (Threshold: > 5.0g)")
                high_risk_count += 1
            elif sat_fat_val <= 1.5:
                positive_factors.append(f"Low Saturated Fat: {sat_fat_val:.1f} g/100g (Healthy: < 1.5g)")
                positive_count += 1

        # 3. Sugars Evaluation (Standard Threshold: > 22.5g / 100g is High, < 5.0g is Low)
        if sugars_val is not None:
            if sugars_val >= 22.5:
                risk_factors.append(f"High Total Sugars: {sugars_val:.1f} g/100g (Threshold: > 22.5g)")
                high_risk_count += 1
            elif sugars_val <= 5.0:
                positive_factors.append(f"Low Total Sugars: {sugars_val:.1f} g/100g (Healthy: < 5.0g)")
                positive_count += 1

        if added_sugars_val is not None and added_sugars_val >= 10.0:
            risk_factors.append(f"High Added Sugars: {added_sugars_val:.1f} g/100g")
            high_risk_count += 1

        # 4. Trans Fat Evaluation (> 0.2g is non-trivial)
        if trans_fat_val is not None:
            if trans_fat_val > 0.2:
                risk_factors.append(f"Contains Trans Fat: {trans_fat_val:.1f} g/100g (Recommended: 0g)")
                high_risk_count += 1
            elif trans_fat_val == 0.0:
                positive_factors.append("Zero Trans Fat (0.0 g/100g)")

        # 5. Dietary Fiber Evaluation (>= 6.0g is High, >= 3.0g is Source)
        if fiber_val is not None:
            if fiber_val >= 6.0:
                positive_factors.append(f"High Dietary Fiber: {fiber_val:.1f} g/100g (Rich source: > 6.0g)")
                positive_count += 2
            elif fiber_val >= 3.0:
                positive_factors.append(f"Good Source of Fiber: {fiber_val:.1f} g/100g")
                positive_count += 1

        # 6. Protein Evaluation (>= 10.0g is High, >= 5.0g is Source)
        if protein_val is not None:
            if protein_val >= 10.0:
                positive_factors.append(f"High Protein Content: {protein_val:.1f} g/100g (Rich source: > 10.0g)")
                positive_count += 1
            elif protein_val >= 5.0:
                positive_factors.append(f"Source of Protein: {protein_val:.1f} g/100g")

        # Context handling for pure edible oils
        if is_pure_oil:
            if sugars_val == 0.0 or sugars_val is None:
                positive_factors.append("Naturally Sugar-Free")
            if sodium_val == 0.0 or sodium_val is None:
                positive_factors.append("Naturally Sodium-Free")
            return {
                "classification": "MODERATE",
                "score": 65,
                "badge_color": "amber",
                "summary": "100% Lipid / Cooking Medium. Nutrient density represents standard culinary edible oil profile.",
                "positive_factors": positive_factors,
                "risk_factors": ["High Energy Density (Cooking Oil / Fat)"],
                "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
            }

        # Decision Matrix
        if high_risk_count >= 2 or (high_risk_count >= 1 and len(risk_factors) >= 2):
            classification = "HIGH / LESS HEALTHY"
            badge_color = "rose"
            score = max(25, 50 - (high_risk_count * 12))
            summary = "Contains elevated nutrient(s) of public health concern (e.g., Sodium, Saturated Fat, or Sugars) exceeding standard dietary intake benchmarks."
        elif high_risk_count == 0 and positive_count >= 2:
            classification = "HEALTHIER"
            badge_color = "emerald"
            score = min(96, 80 + (positive_count * 4))
            summary = "Favorable nutritional density with low saturated fat, minimal sodium/sugars, and positive dietary fiber or protein content."
        else:
            classification = "MODERATE"
            badge_color = "amber"
            score = 65
            summary = "Standard nutrient distribution within moderate dietary reference intake boundaries."

        return {
            "classification": classification,
            "score": score,
            "badge_color": badge_color,
            "summary": summary,
            "positive_factors": positive_factors,
            "risk_factors": risk_factors,
            "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
        }

    @staticmethod
    def _insufficient_data() -> Dict[str, Any]:
        return {
            "classification": "INSUFFICIENT DATA",
            "score": 50,
            "badge_color": "slate",
            "summary": "Nutritional facts panel was not detected on the scanned package surface. Assessment requires a legible nutrition table.",
            "positive_factors": [],
            "risk_factors": [],
            "disclaimer": "AI-derived informational assessment based on visible package declarations. Not a medical diagnosis."
        }
