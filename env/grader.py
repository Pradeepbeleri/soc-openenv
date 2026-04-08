from typing import Dict, Any


def normalize_score(score: float) -> float:
    """
    Clamp score strictly inside (0, 1).
    """
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return round(score, 2)


# -------------------------------------------------
# Runtime-compatible grader expected by environment.py
# -------------------------------------------------
def grade_action(result: Dict[str, Any]) -> float:
    """
    Single-action grading hook used by env/environment.py.
    Must return a score strictly between 0 and 1.
    """
    score = 0.0

    if result.get("valid_action"):
        score += 0.4
    if result.get("progress_made"):
        score += 0.3
    if result.get("safe_action"):
        score += 0.3

    return normalize_score(score)


# -------------------------------------------------
# 3 task graders for validator / submission scoring
# -------------------------------------------------
def grade_task_1(result: Dict[str, Any]) -> float:
    """
    Task 1: Detect the issue.
    """
    score = 0.0

    if result.get("observed_alert"):
        score += 0.4
    if result.get("identified_attack_ip"):
        score += 0.4
    if result.get("used_monitor_action"):
        score += 0.2

    return normalize_score(score)


def grade_task_2(result: Dict[str, Any]) -> float:
    """
    Task 2: Contain the threat.
    """
    score = 0.0

    if result.get("correct_ip_blocked"):
        score += 0.5
    if result.get("block_action_valid"):
        score += 0.3
    if result.get("no_invalid_actions"):
        score += 0.2

    return normalize_score(score)


def grade_task_3(result: Dict[str, Any]) -> float:
    """
    Task 3: Close the incident.
    """
    score = 0.0

    if result.get("incident_closed"):
        score += 0.6
    if result.get("incident_summary_logged"):
        score += 0.2
    if result.get("workflow_completed"):
        score += 0.2

    return normalize_score(score)


def grade_submission(result: Dict[str, Any]) -> Dict[str, float]:
    """
    Returns all task scores.
    """
    return {
        "task_1": grade_task_1(result),
        "task_2": grade_task_2(result),
        "task_3": grade_task_3(result),
    }
