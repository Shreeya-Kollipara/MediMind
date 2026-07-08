"""
Manager — orchestrates all agents and returns a unified response dict.
"""

import os
from agents.nlp_agent import extract_symptoms
from agents.risk_agent import assess_risk
from agents.llm_agent import generate_insights
from agents.explain_agent import build_explanation


def process_message(user_text: str) -> dict:
    """
    Full pipeline:
        1. NLP agent  → extract symptoms
        2. Risk agent → assess risk level
        3. LLM agent  → generate clinical insights
        4. Explain agent → build reasoning trail
    """
    if not user_text or not user_text.strip():
        return {
            "error": "Please describe your symptoms so I can assist you.",
            "symptoms": [],
            "risk": {},
            "insights": {},
            "explanation": {},
        }

    # 1. Symptom extraction
    nlp_result = extract_symptoms(user_text)
    symptoms = nlp_result["symptoms"]
    extraction_method = nlp_result["method"]

    # 2. Risk assessment
    risk = assess_risk(symptoms)

    # 3. LLM reasoning
    api_key = os.getenv("GEMINI_API_KEY", "")
    insights = generate_insights(
        symptoms=symptoms,
        risk_level=risk["level"],
        user_text=user_text,
        api_key=api_key,
    )

    # 4. Explainability
    explanation = build_explanation(
        original_text=user_text,
        symptoms=symptoms,
        extraction_method=extraction_method,
        risk_assessment=risk,
        llm_insights=insights,
    )

    return {
        "symptoms": symptoms,
        "symptom_count": nlp_result["symptom_count"],
        "extraction_method": extraction_method,
        "risk": risk,
        "insights": insights,
        "explanation": explanation,
    }