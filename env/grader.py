from typing import Any

def clamp_reward(score: float) -> float:
    """
    Keep reward strictly between 0 and 1 to be absolutely safe, 
    though our deterministic formulas already achieve this.
    """
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return round(score, 2)

def grade_task_1(state: Any) -> float:
    """
    Task 1: Investigate suspicious login activity.
    Base score 0.05 so a completely broken agent doesn't get exactly 0.0.
    """
    score = 0.05
    if getattr(state, "investigated", False):
        score += 0.25
    if getattr(state, "flagged_state", False):
        score += 0.20
    if getattr(state, "quarantine_applied", False):
        score += 0.20
    if getattr(state, "documented_state", False):
        score += 0.10
    # Max possible = 0.80
    return clamp_reward(score)

def grade_task_2(state: Any) -> float:
    """
    Task 2: Triage suspicious DNS activity.
    Base score 0.02.
    """
    score = 0.02
    if getattr(state, "triage_done", False):
        score += 0.20
    if getattr(state, "severity_assessed", False):
        score += 0.15
    if getattr(state, "false_positive_marked", False):
        score += 0.30
    if getattr(state, "documented_state", False):
        score += 0.20
    if getattr(state, "evidence_collected_state", False):
        score += 0.10
    # Max possible = 0.97
    return clamp_reward(score)

def grade_task_3(state: Any) -> float:
    """
    Task 3: Contain lateral movement incident.
    Base score 0.03.
    """
    score = 0.03
    if getattr(state, "evidence_collected_state", False):
        score += 0.30
    if getattr(state, "incident_closed", False):
        score += 0.40
    if getattr(state, "documented_state", False):
        score += 0.10
    if getattr(state, "flagged_state", False):
        score += 0.05
    # Max possible = 0.88
    return clamp_reward(score)
