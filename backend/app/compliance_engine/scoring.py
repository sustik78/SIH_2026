"""
PRAMAN AI - Explainable Compliance Scoring Algorithm
Computes weighted, explainable compliance scores (0-100) and overall regulatory decision.
"""

from typing import Dict, Any, List

class ComplianceScorer:
    @staticmethod
    def calculate_score(evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates explainable compliance score and generates category breakdown.
        """
        results: List[Dict[str, Any]] = evaluation_result.get("results", [])
        
        # Category trackers
        # 1. Declaration Completeness (Max: 40)
        # 2. Value & Unit Validation (Max: 25)
        # 3. Price & USP Consistency (Max: 15)
        # 4. Consumer Redressal & Origin (Max: 10)
        # 5. Legibility & Placement (Max: 10)

        completeness_score = 40.0
        val_score = 25.0
        price_score = 15.0
        consumer_score = 10.0
        legibility_score = 10.0

        for r in results:
            rid = r["rule_id"]
            status = r["status"]
            severity = r["severity"]

            if rid in ["LM-PCR-01", "LM-PCR-02", "LM-PCR-04"]:
                # Completeness rules
                if status == "VIOLATION":
                    completeness_score -= 13.33
                elif status == "WARNING":
                    completeness_score -= 5.0
            
            elif rid == "LM-PCR-03":
                # Net Quantity validation
                if status == "VIOLATION":
                    val_score -= 25.0
                elif status == "WARNING":
                    val_score -= 10.0

            elif rid in ["LM-PCR-05", "LM-PCR-06"]:
                # Pricing & USP
                if status == "VIOLATION":
                    price_score -= 7.5
                elif status == "WARNING":
                    price_score -= 3.0

            elif rid in ["LM-PCR-07", "LM-PCR-08"]:
                # Consumer Care & COO
                if status == "VIOLATION":
                    consumer_score -= 5.0
                elif status == "WARNING":
                    consumer_score -= 2.0

            elif rid in ["LM-PCR-10", "LM-PCR-11"]:
                # Legibility & Digital
                if status == "VIOLATION":
                    legibility_score -= 5.0
                elif status == "WARNING" or status == "MANUAL_VERIFICATION_REQUIRED":
                    legibility_score -= 2.5

        # Clamp category scores
        completeness_score = max(0.0, round(completeness_score, 1))
        val_score = max(0.0, round(val_score, 1))
        price_score = max(0.0, round(price_score, 1))
        consumer_score = max(0.0, round(consumer_score, 1))
        legibility_score = max(0.0, round(legibility_score, 1))

        total_score = round(completeness_score + val_score + price_score + consumer_score + legibility_score)
        total_score = min(100, max(0, total_score))

        critical_count = evaluation_result.get("critical_violations_count", 0)
        violation_count = evaluation_result.get("violation_count", 0)
        warning_count = evaluation_result.get("warning_count", 0)

        # Regulatory decision logic
        if critical_count > 0 or total_score < 70 or violation_count >= 2:
            decision = "NON-COMPLIANT"
            decision_badge_color = "red"
            decision_summary = f"Regulatory non-compliance detected with {violation_count} violation(s) including {critical_count} critical infraction(s)."
        elif total_score >= 85 and violation_count == 0:
            decision = "COMPLIANT"
            decision_badge_color = "green"
            decision_summary = "Package satisfies statutory Legal Metrology requirements under PCR 2011 and amendments."
        else:
            decision = "PENDING REVIEW"
            decision_badge_color = "amber"
            decision_summary = f"Package has minor non-conformities ({warning_count} warnings, {violation_count} non-critical violation). Requires supervisory review."

        # Action recommendation
        if decision == "COMPLIANT":
            recommended_action = "Approve for retail distribution. No enforcement action required."
        elif critical_count > 0:
            recommended_action = "Issue immediate Notice under Section 36(1) of Legal Metrology Act, 2009. Seizure of non-standard pre-packaged commodity recommended."
        elif decision == "NON-COMPLIANT":
            recommended_action = "Issue Statutory Show Cause Notice under Legal Metrology (Packaged Commodities) Rules, 2011. Require rectification within 15 days."
        else:
            recommended_action = "Mark for manual verification by Designated Legal Metrology Officer before releasing compliance certificate."

        return {
            "overall_score": total_score,
            "decision": decision,
            "decision_badge_color": decision_badge_color,
            "decision_summary": decision_summary,
            "recommended_action": recommended_action,
            "categories": [
                {
                    "name": "Declaration Completeness",
                    "score": completeness_score,
                    "max_score": 40,
                    "percentage": round((completeness_score / 40.0) * 100)
                },
                {
                    "name": "Value & Unit Validation",
                    "score": val_score,
                    "max_score": 25,
                    "percentage": round((val_score / 25.0) * 100)
                },
                {
                    "name": "Price & USP Consistency",
                    "score": price_score,
                    "max_score": 15,
                    "percentage": round((price_score / 15.0) * 100)
                },
                {
                    "name": "Consumer Redressal & Origin",
                    "score": consumer_score,
                    "max_score": 10,
                    "percentage": round((consumer_score / 10.0) * 100)
                },
                {
                    "name": "Display Legibility & Placement",
                    "score": legibility_score,
                    "max_score": 10,
                    "percentage": round((legibility_score / 10.0) * 100)
                }
            ]
        }
