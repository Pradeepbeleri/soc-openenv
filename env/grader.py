

from typing import Dict, Any


def clamp_open_interval(score: float) -> float:
    """
    Force score to be strictly inside (0, 1).
    """
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return round(score, 2)


def grade_action(result: Dict[str, Any]) -> float:
    """
    Compatibility hook expected by env/environment.py.
    """
    score = 0.0

    if result.get("valid_action"):
        score += 0.34
    if result.get("progress_made"):
        score += 0.33
    if result.get("safe_action"):
        score += 0.33

    return clamp_open_interval(score)


def grade_task_1(result: Dict[str, Any]) -> float:
    """
    Task 1 grader.
    """
    score = 0.0
    if result.get("task_1_complete"):
        score += 0.6
    if result.get("task_1_partial"):
        score += 0.3
    if result.get("task_1_safe"):
        score += 0.1
    return clamp_open_interval(score)


def grade_task_2(result: Dict[str, Any]) -> float:
    """
    Task 2 grader.
    """
    score = 0.0
    if result.get("task_2_complete"):
        score += 0.6
    if result.get("task_2_partial"):
        score += 0.3
    if result.get("task_2_safe"):
        score += 0.1
    return clamp_open_interval(score)


def grade_task_3(result: Dict[str, Any]) -> float:
    """
    Task 3 grader.
    """
    score = 0.0
    if result.get("task_3_complete"):
        score += 0.6
    if result.get("task_3_partial"):
        score += 0.3
    if result.get("task_3_safe"):
        score += 0.1
    return clamp_open_interval(score)


def grade_submission(result: Dict[str, Any]) -> Dict[str, float]:
    """
    Main scoring entry point with 3 graded tasks.
    """
    return {
        "task_1": grade_task_1(result),
        "task_2": grade_task_2(result),
        "task_3": grade_task_3(result),
    }
