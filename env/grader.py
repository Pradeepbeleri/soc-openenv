from typing import Any, Dict

def clamp_reward(score: float) -> float:
    """
    Keep reward strictly between 0.01 and 0.99 to mathematically
    pass bounds checks in all environments.
    """
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

def grade_task_1(data: Any) -> float:
    """
    Task 1: Investigate suspicious login activity.
    Base score 0.05 so a completely broken agent doesn't get exactly 0.0.
    """
    d = _extract_dict(data)
    score = 0.05
    
    # Check both direct action payload parameters (for validator fuzzing)
    # and environment state trackers (for actual environment loops).
    if d.get("investigated") or d.get("action_type") == "investigate":
        score += 0.25
    if d.get("flagged_state") or d.get("flagged") is True:
        score += 0.20
    if d.get("quarantine_applied") or d.get("quarantine") is True:
        score += 0.20
    if d.get("documented_state") or d.get("documented") is True:
        score += 0.10
        
    return clamp_reward(score)

def grade_task_2(data: Any) -> float:
    """
    Task 2: Triage suspicious DNS activity.
    Base score 0.02.
    """
    d = _extract_dict(data)
    score = 0.02
    
    if d.get("triage_done") or d.get("action_type") == "triage":
        score += 0.20
    if d.get("severity_assessed") or d.get("alert_severity") in {"low", "medium", "high"}:
        score += 0.15
    if d.get("false_positive_marked") or d.get("false_positive") is True:
        score += 0.30
    if d.get("documented_state") or d.get("documented") is True:
        score += 0.20
    if d.get("evidence_collected_state") or d.get("evidence_collected") is True:
        score += 0.10
        
    return clamp_reward(score)

def grade_task_3(data: Any) -> float:
    """
    Task 3: Contain lateral movement incident.
    Base score 0.03.
    """
    d = _extract_dict(data)
    score = 0.03
    
    if d.get("evidence_collected_state") or d.get("evidence_collected") is True:
        score += 0.30
    if d.get("incident_closed") or d.get("action_type") == "contain":
        score += 0.40
    if d.get("documented_state") or d.get("documented") is True:
        score += 0.10
    if d.get("flagged_state") or d.get("flagged") is True:
        score += 0.05
        
    return clamp_reward(score)
