from typing import Dict, Any, Tuple


def clamp_open_interval(score: float) -> float:
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return round(score, 2)


def grade_task_1(result: Dict[str, Any]) -> float:
    score = 0.0
    if result.get("task_1_complete"):
        score += 0.6
    if result.get("task_1_partial"):
        score += 0.3
    if result.get("task_1_safe"):
        score += 0.1
    return clamp_open_interval(score)


def grade_task_2(result: Dict[str, Any]) -> float:
    score = 0.0
    if result.get("task_2_complete"):
        score += 0.6
    if result.get("task_2_partial"):
        score += 0.3
    if result.get("task_2_safe"):
        score += 0.1
    return clamp_open_interval(score)


def grade_task_3(result: Dict[str, Any]) -> float:
    score = 0.0
    if result.get("task_3_complete"):
        score += 0.6
    if result.get("task_3_partial"):
        score += 0.3
    if result.get("task_3_safe"):
        score += 0.1
    return clamp_open_interval(score)


def grade_action(state, action):
    # temporary compatible hook
    result = action if isinstance(action, dict) else {}

    if state.task == "task_1":
        reward = grade_task_1(result)
    elif state.task == "task_2":
        reward = grade_task_2(result)
    elif state.task == "task_3":
        reward = grade_task_3(result)
    else:
        reward = 0.01

    done = False
    error = None
    return reward, done, error
