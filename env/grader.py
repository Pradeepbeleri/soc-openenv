from typing import Any, Dict

def clamp_reward(score: float) -> float:
    """Ensure score is strictly inside (0, 1) — never 0.0 or 1.0."""
    # Map [0, 1] → [0.02, 0.98] to guarantee strict bounds with margin
    clamped = 0.02 + (max(0.0, min(1.0, score)) * 0.96)
    return round(clamped, 4)

def _extract_dict(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        return data
    if hasattr(data, "model_dump"):
        return data.model_dump()
    try:
        return vars(data)
    except TypeError:
        return {}

def _base_score(d: Dict[str, Any], max_possible: float) -> float:
    score = 0.05
    if d.get("headers_read"):
        score += 0.20
    if d.get("body_read"):
        score += 0.20
    if d.get("attachments_scanned"):
        score += 0.15

    correct_resolution = d.get("correct_resolution", "unknown")
    if d.get("resolution") == correct_resolution:
        score += 0.35
    elif d.get("resolution") is not None and d.get("resolution") != correct_resolution:
        score -= 0.10

    # Clamp raw score to [0, max_possible] before mapping to strict (0,1)
    raw = max(0.0, min(score, max_possible))
    # Normalise against max_possible so the full range is used fairly
    normalised = raw / max_possible if max_possible > 0 else raw
    return clamp_reward(normalised)

def grade_task_1(data: Any) -> float:
    """Task 1: Basic Spam. Easy."""
    return _base_score(_extract_dict(data), 0.90)

def grade_task_2(data: Any) -> float:
    """Task 2: Phishing attempt. Medium."""
    return _base_score(_extract_dict(data), 0.95)

def grade_task_3(data: Any) -> float:
    """Task 3: Stealth Macro malware. Hard."""
    return _base_score(_extract_dict(data), 0.99)

def grade_task_3(data: Any) -> float:
    """Task 3: Stealth Macro malware. Hard."""
    return _base_score(_extract_dict(data), 0.99)
