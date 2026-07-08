"""
NLP Agent — extracts symptoms from free-text using spaCy + a curated symptom lexicon.
Falls back gracefully if the spaCy model isn't installed.
"""

import re
from typing import List, Dict

# ── Symptom lexicon ────────────────────────────────────────────────────────────
SYMPTOM_LEXICON: List[str] = [
    # Pain
    "headache", "migraine", "chest pain", "abdominal pain", "back pain",
    "neck pain", "joint pain", "muscle pain", "ear pain", "throat pain",
    "stomach ache", "cramps", "pain",

    # Respiratory
    "cough", "dry cough", "wet cough", "shortness of breath", "difficulty breathing",
    "wheezing", "breathlessness", "runny nose", "nasal congestion", "sore throat",
    "sneezing", "hoarseness",

    # Systemic
    "fever", "chills", "fatigue", "weakness", "dizziness", "fainting",
    "loss of consciousness", "sweating", "night sweats", "weight loss",
    "weight gain", "loss of appetite", "dehydration",

    # Gastrointestinal
    "nausea", "vomiting", "diarrhea", "constipation", "bloating",
    "indigestion", "heartburn", "blood in stool", "black stool",

    # Neurological
    "numbness", "tingling", "seizure", "confusion", "memory loss",
    "blurred vision", "double vision", "vision loss", "hearing loss",
    "ringing in ears", "tinnitus", "slurred speech", "difficulty speaking",
    "tremor", "loss of balance",

    # Cardiac / Vascular
    "palpitations", "irregular heartbeat", "rapid heartbeat", "slow heartbeat",
    "swelling", "edema", "leg swelling", "chest tightness",

    # Skin
    "rash", "hives", "itching", "redness", "bruising", "yellowing",
    "jaundice", "pale skin", "cyanosis", "skin discoloration",

    # Urinary
    "frequent urination", "painful urination", "blood in urine",
    "dark urine", "reduced urination",

    # Mental / Emotional
    "anxiety", "depression", "insomnia", "irritability", "mood swings",
    "panic attack", "hallucination",

    # Musculoskeletal
    "stiffness", "swollen joints", "muscle weakness", "muscle cramps",
]

# Sort by length (longest first) so multi-word phrases match before single words
SYMPTOM_LEXICON.sort(key=len, reverse=True)


def _extract_with_regex(text: str) -> List[str]:
    """Keyword-match symptoms from text using the curated lexicon."""
    text_lower = text.lower()
    found: List[str] = []
    for symptom in SYMPTOM_LEXICON:
        pattern = r"\b" + re.escape(symptom) + r"\b"
        if re.search(pattern, text_lower):
            found.append(symptom)
    # De-duplicate while preserving order
    seen = set()
    unique = []
    for s in found:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return unique


def _extract_with_spacy(text: str):
    """Use spaCy NER + noun chunks to surface symptom-like phrases."""
    try:
        import spacy  # type: ignore
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return None  # Model not installed → fall back

        doc = nlp(text)
        candidates: List[str] = []

        # Named entities labelled as symptoms / medical concepts
        for ent in doc.ents:
            if ent.label_ in ("SYMPTOM", "DISEASE", "CONDITION"):
                candidates.append(ent.text.lower())

        # Noun chunks that overlap with our lexicon
        for chunk in doc.noun_chunks:
            chunk_lower = chunk.text.lower()
            for symptom in SYMPTOM_LEXICON:
                if symptom in chunk_lower:
                    candidates.append(symptom)

        return candidates if candidates else None
    except ImportError:
        return None


def extract_symptoms(text: str) -> Dict:
    """
    Main entry-point for the NLP agent.

    Returns:
        {
            "symptoms": [...],
            "method": "spacy" | "regex",
            "symptom_count": int,
            "original_text": str,
        }
    """
    spacy_results = _extract_with_spacy(text)

    if spacy_results:
        # Merge spaCy results with regex to ensure nothing is missed
        regex_results = _extract_with_regex(text)
        combined = list(dict.fromkeys(spacy_results + regex_results))
        method = "spacy+regex"
    else:
        combined = _extract_with_regex(text)
        method = "regex"

    return {
        "symptoms": combined,
        "method": method,
        "symptom_count": len(combined),
        "original_text": text,
    }