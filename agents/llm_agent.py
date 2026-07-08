"""
LLM Agent — uses Google Gemini API to reason about symptoms and
generate structured clinical insights.
"""

import os
import json
import re
from typing import List, Dict


def _build_prompt(symptoms: List[str], risk_level: str, user_text: str) -> str:
    symptom_str = ", ".join(symptoms) if symptoms else "none clearly identified"
    return f"""You are a clinical decision-support assistant. A patient has described their symptoms.

Patient's message: "{user_text}"
Extracted symptoms: {symptom_str}
Preliminary risk level: {risk_level}

Respond ONLY with a valid JSON object (no markdown, no code fences) with this exact structure:
{{
  "possible_conditions": [
    {{
      "name": "Condition Name",
      "likelihood": "High/Moderate/Low",
      "brief_explanation": "1-2 sentences"
    }}
  ],
  "risk_summary": "2-3 sentence summary of overall risk",
  "general_advice": ["advice point 1", "advice point 2", "advice point 3"],
  "when_to_seek_care": "Clear guidance on when to see a doctor",
  "disclaimer": "This is not a medical diagnosis. Always consult a qualified healthcare professional."
}}

Guidelines:
- List 2-4 possible conditions, most likely first.
- Be empathetic but clinically precise.
- Always include a disclaimer.
- Do NOT make definitive diagnoses.
- If symptoms are vague, reflect that uncertainty honestly.
"""


def _parse_response(raw: str) -> Dict:
    """Extract JSON from the model response, stripping any markdown fences."""
    # Strip ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to salvage the JSON substring
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {
        "possible_conditions": [],
        "risk_summary": "Unable to parse structured response.",
        "general_advice": ["Please describe your symptoms more clearly."],
        "when_to_seek_care": "Consult a healthcare professional if unsure.",
        "disclaimer": "This is not a medical diagnosis.",
        "raw_response": raw,
    }


def generate_insights(
    symptoms: List[str],
    risk_level: str,
    user_text: str,
    api_key: str,
) -> Dict:
    """
    Call Google Gemini and return structured clinical insights.

    Returns a dict matching the JSON schema defined in _build_prompt.
    """
    try:
        import google.generativeai as genai  # type: ignore

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-3-flash-preview")

        prompt = _build_prompt(symptoms, risk_level, user_text)
        response = model.generate_content(prompt)
        raw_text = response.text

        return _parse_response(raw_text)

    except ImportError:
        return _fallback_response(symptoms, risk_level)
    except Exception as e:
        return {
            "possible_conditions": [],
            "risk_summary": f"LLM service unavailable: {str(e)[:120]}",
            "general_advice": [
                "Please consult a qualified healthcare professional.",
                "Describe your symptoms clearly when seeking help.",
            ],
            "when_to_seek_care": "Seek care if symptoms are severe or worsening.",
            "disclaimer": "This is not a medical diagnosis.",
            "error": str(e),
        }


def _fallback_response(symptoms: List[str], risk_level: str) -> Dict:
    """Provide a basic response when Gemini is unavailable."""
    return {
        "possible_conditions": [
            {
                "name": "Unknown — LLM Unavailable",
                "likelihood": "N/A",
                "brief_explanation": "The AI reasoning module is not available. Please configure a valid Gemini API key.",
            }
        ],
        "risk_summary": (
            f"Based on extracted symptoms ({', '.join(symptoms) or 'none'}), "
            f"the preliminary risk level is {risk_level}."
        ),
        "general_advice": [
            "Consult a healthcare professional for a proper evaluation.",
            "Monitor your symptoms and seek emergency care if they worsen.",
        ],
        "when_to_seek_care": "See a doctor promptly if symptoms are severe or persistent.",
        "disclaimer": "This is not a medical diagnosis. Always consult a qualified healthcare professional.",
    }