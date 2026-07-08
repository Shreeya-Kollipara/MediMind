"""
Explain Agent — provides transparency about how the system derived its output.
No external API calls; purely rule-based reasoning trails.
"""

from typing import List, Dict


def build_explanation(
    original_text: str,
    symptoms: List[str],
    extraction_method: str,
    risk_assessment: Dict,
    llm_insights: Dict,
) -> Dict:
    """
    Construct a human-readable explanation of the system's reasoning chain.

    Returns:
        {
            "steps": [...],
            "confidence": str,
            "transparency_note": str,
        }
    """
    steps = []

    # Step 1 — Input reception
    steps.append({
        "step": 1,
        "title": "Input Analysis",
        "detail": (
            f"Received user input of {len(original_text.split())} words. "
            "Text was pre-processed (lowercased, whitespace normalised) "
            "before symptom extraction."
        ),
        "icon": "📝",
    })

    # Step 2 — Symptom extraction
    if symptoms:
        steps.append({
            "step": 2,
            "title": "Symptom Extraction",
            "detail": (
                f"The NLP agent ({extraction_method}) identified "
                f"{len(symptoms)} symptom(s): {', '.join(symptoms)}. "
                "Extraction used a curated medical lexicon with longest-match priority."
            ),
            "icon": "🔍",
        })
    else:
        steps.append({
            "step": 2,
            "title": "Symptom Extraction",
            "detail": (
                "No specific symptoms were detected in the input. "
                "The system will still attempt to provide general guidance."
            ),
            "icon": "🔍",
        })

    # Step 3 — Risk assessment
    triggered = risk_assessment.get("triggered_rules", [])
    risk_level = risk_assessment.get("level", "LOW")
    risk_score = risk_assessment.get("score", 0)

    if triggered:
        rule_labels = [r["label"] for r in triggered]
        steps.append({
            "step": 3,
            "title": "Risk Detection",
            "detail": (
                f"Risk agent matched {len(triggered)} emergency rule(s): "
                f"{', '.join(rule_labels)}. "
                f"Final risk level: {risk_level} (score {risk_score}/10)."
            ),
            "icon": "⚠️",
        })
    else:
        steps.append({
            "step": 3,
            "title": "Risk Detection",
            "detail": (
                f"No emergency rule patterns triggered. "
                f"Risk level assessed as {risk_level} (score {risk_score}/10) "
                "based on individual symptom severity weights."
            ),
            "icon": "✅",
        })

    # Step 4 — LLM reasoning
    conditions = llm_insights.get("possible_conditions", [])
    if conditions and "error" not in llm_insights:
        cond_names = [c.get("name", "Unknown") for c in conditions]
        steps.append({
            "step": 4,
            "title": "AI Reasoning (Gemini)",
            "detail": (
                f"The LLM agent analysed {len(symptoms)} symptom(s) alongside "
                f"the {risk_level} risk context and surfaced "
                f"{len(conditions)} possible condition(s): {', '.join(cond_names)}. "
                "Conditions are ranked by likelihood, not certainty."
            ),
            "icon": "🤖",
        })
    else:
        steps.append({
            "step": 4,
            "title": "AI Reasoning (Gemini)",
            "detail": (
                "LLM reasoning was unavailable or returned an error. "
                "Fallback guidance has been provided instead."
            ),
            "icon": "🤖",
        })

    # Step 5 — Output composition
    steps.append({
        "step": 5,
        "title": "Response Assembly",
        "detail": (
            "All agent outputs were merged by the central Manager module. "
            "Risk colours, condition cards, and advice were composed "
            "into the structured response you see."
        ),
        "icon": "🔗",
    })

    # Confidence heuristic
    if len(symptoms) >= 3 and risk_level in ("EMERGENCY", "HIGH"):
        confidence = "High"
        confidence_note = "Multiple clear symptoms with strong risk signals."
    elif len(symptoms) >= 2:
        confidence = "Moderate"
        confidence_note = "Some symptoms identified; results are indicative."
    elif len(symptoms) == 1:
        confidence = "Low"
        confidence_note = "Only one symptom detected; more detail would improve accuracy."
    else:
        confidence = "Very Low"
        confidence_note = "No specific symptoms found; guidance is generic."

    return {
        "steps": steps,
        "confidence": confidence,
        "confidence_note": confidence_note,
        "transparency_note": (
            "This explanation shows every reasoning step the system took. "
            "No diagnosis is made — results are for informational purposes only. "
            "Always consult a licensed healthcare professional."
        ),
    }