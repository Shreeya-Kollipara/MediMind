"""
Risk Agent — detects emergency / high-risk symptom patterns and
returns a structured risk assessment without any external API calls.
"""

from typing import List, Dict, Tuple

# ── Emergency rule definitions ─────────────────────────────────────────────────
# Each rule: (frozenset of trigger symptoms, label, advice, severity 1-10)
EMERGENCY_RULES: List[Tuple[frozenset, str, str, int]] = [
    (
        frozenset(["chest pain", "shortness of breath", "sweating"]),
        "Possible Cardiac Emergency",
        "These symptoms may indicate a heart attack. Call emergency services immediately.",
        10,
    ),
    (
        frozenset(["chest pain", "palpitations"]),
        "Possible Cardiac Event",
        "Seek immediate medical evaluation for chest pain with palpitations.",
        9,
    ),
    (
        frozenset(["chest tightness", "difficulty breathing"]),
        "Possible Cardiac / Respiratory Emergency",
        "Call emergency services immediately.",
        9,
    ),
    (
        frozenset(["slurred speech", "weakness", "confusion"]),
        "Possible Stroke",
        "FAST check: Face drooping, Arm weakness, Speech difficulty, Time to call 911.",
        10,
    ),
    (
        frozenset(["loss of consciousness"]),
        "Loss of Consciousness",
        "Call emergency services immediately. Do not leave the person alone.",
        10,
    ),
    (
        frozenset(["seizure"]),
        "Seizure Detected",
        "Clear the area of hazards, do not restrain. Call emergency if lasting >5 min.",
        9,
    ),
    (
        frozenset(["difficulty breathing", "cyanosis"]),
        "Severe Respiratory Distress",
        "Call emergency services. Ensure airway is clear.",
        10,
    ),
    (
        frozenset(["blood in stool"]),
        "Gastrointestinal Bleeding",
        "Seek urgent medical attention. This may indicate internal bleeding.",
        8,
    ),
    (
        frozenset(["blood in urine"]),
        "Hematuria",
        "See a doctor promptly — blood in urine requires evaluation.",
        7,
    ),
    (
        frozenset(["hallucination"]),
        "Neuropsychiatric Symptom",
        "Seek prompt psychiatric or neurological evaluation.",
        7,
    ),
    (
        frozenset(["high fever", "stiffness", "confusion"]),
        "Possible Meningitis",
        "Seek emergency care immediately.",
        10,
    ),
]

# ── Severity tiers ─────────────────────────────────────────────────────────────
HIGH_RISK_SYMPTOMS = {
    "chest pain", "shortness of breath", "loss of consciousness",
    "seizure", "slurred speech", "cyanosis", "difficulty breathing",
    "blood in stool", "blood in urine", "hallucination", "loss of balance",
    "vision loss", "severe headache",
}

MODERATE_RISK_SYMPTOMS = {
    "fever", "vomiting", "diarrhea", "fainting", "palpitations",
    "numbness", "tingling", "confusion", "blurred vision",
    "rapid heartbeat", "swelling",
}


def assess_risk(symptoms: List[str]) -> Dict:
    """
    Evaluate risk level from extracted symptoms.

    Returns:
        {
            "level": "EMERGENCY" | "HIGH" | "MODERATE" | "LOW",
            "score": int (0-10),
            "triggered_rules": [...],
            "advice": str,
            "color": str (hex),
        }
    """
    symptom_set = set(s.lower() for s in symptoms)
    triggered_rules = []
    max_severity = 0

    for trigger, label, advice, severity in EMERGENCY_RULES:
        if trigger.issubset(symptom_set) or any(t in symptom_set for t in trigger):
            triggered_rules.append({
                "label": label,
                "advice": advice,
                "severity": severity,
            })
            if severity > max_severity:
                max_severity = severity

    # Compute base score from individual symptom risk tiers
    high_count = len(symptom_set & HIGH_RISK_SYMPTOMS)
    moderate_count = len(symptom_set & MODERATE_RISK_SYMPTOMS)
    base_score = min(10, high_count * 3 + moderate_count * 1)

    final_score = min(10, max(max_severity, base_score))

    if final_score >= 8 or triggered_rules:
        level = "EMERGENCY"
        color = "#FF6B6B"
        generic_advice = (
            "⚠️ One or more high-risk symptoms detected. "
            "Please seek emergency medical care or call your local emergency number immediately."
        )
    elif final_score >= 5:
        level = "HIGH"
        color = "#FFB347"
        generic_advice = (
            "Your symptoms suggest a condition that needs prompt medical evaluation. "
            "Please contact a healthcare provider today."
        )
    elif final_score >= 2:
        level = "MODERATE"
        color = "#87CEEB"
        generic_advice = (
            "Some of your symptoms warrant monitoring. "
            "Consider scheduling a doctor's appointment if symptoms persist or worsen."
        )
    else:
        level = "LOW"
        color = "#98D8C8"
        generic_advice = (
            "Your symptoms appear to be low-risk. "
            "Rest, stay hydrated, and monitor for any changes."
        )

    return {
        "level": level,
        "score": final_score,
        "triggered_rules": triggered_rules,
        "advice": generic_advice,
        "color": color,
    }