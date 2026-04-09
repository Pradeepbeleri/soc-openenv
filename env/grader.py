from typing import Any, Dict

def clamp_reward(score: float) -> float:
    """Ensure strictly strictly inside (0, 1) to pass bounds tests universally."""
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return round(score, 3)

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
        # Penalized down slightly for incorrect conclusion but retaining partial progress points
        score -= 0.10
        
    return clamp_reward(min(score, max_possible))

def grade_task_1(data: Any) -> float:
    """Task 1: Basic Spam. Easy."""
    return _base_score(_extract_dict(data), 0.90)

def grade_task_2(data: Any) -> float:
    """Task 2: Phishing attempt. Medium."""
    return _base_score(_extract_dict(data), 0.95)

def grade_task_3(data: Any) -> float:
    """Task 3: Stealth Macro malware. Hard."""
    return _base_score(_extract_dict(data), 0.99)
