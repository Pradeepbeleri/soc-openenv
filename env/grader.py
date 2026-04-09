from typing import Any, Dict


def clamp_reward(score: float) -> float:
    """
    Keep reward strictly between 0 and 1.
    """
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return round(score, 2)


def grade_task_1(action: Dict[str, Any]) -> float:
    """
    Task 1: Investigate suspicious login activity.
    """
    score = 0.0

    if action.get("action_type") == "investigate":
        score += 0.25
    if action.get("target") == "malicious_ip":
        score += 0.25
    if action.get("flagged") is True:
        score += 0.20
    if action.get("quarantine") is True:
        score += 0.20
    if action.get("documented") is True:
        score += 0.10

    return clamp_reward(score)


def grade_task_2(action: Dict[str, Any]) -> float:
    """
    Task 2: Triage suspicious DNS activity.
    """
    score = 0.0

    if action.get("action_type") == "triage":
        score += 0.20
    if action.get("alert_severity") in {"low", "medium", "high"}:
        score += 0.15
    if action.get("false_positive") is True:
        score += 0.30
    if action.get("documented") is True:
        score += 0.20
    if action.get("evidence_collected") is True:
        score += 0.15

    return clamp_reward(score)


def grade_task_3(action: Dict[str, Any]) -> float:
    """
    Task 3: Contain lateral movement incident.
    """
    score = 0.0

    if action.get("action_type") == "contain":
        score += 0.25
    if action.get("evidence_collected") is True:
        score += 0.25
    if action.get("incident_closed") is True:
        score += 0.30
    if action.get("documented") is True:
        score += 0.10
    if action.get("flagged") is True:
        score += 0.05

    return clamp_reward(score)
