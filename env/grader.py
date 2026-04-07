from typing import Dict, Any, Tuple
from env.models import EnvironmentState


def grade_action(state: EnvironmentState, action: Dict[str, Any]) -> Tuple[float, bool, str | None]:
    action_type = action.get("type")
    target = action.get("target")

    if not action_type:
        return 0.0, False, "Missing action type"

    if action_type == "monitor":
        if not target:
            return 0.1, False, "Missing target for monitor"
        if target == state.attack_ip:
            return 0.4, False, None
        return 0.2, False, "Target does not match attack_ip"

    if action_type == "block_ip":
        if not target:
            return 0.1, False, "Missing target for block_ip"
        if target == state.attack_ip:
            return 0.8, False, None
        return 0.2, False, "Blocked wrong IP"

    if action_type == "close_incident":
        if state.score < 0.8:
            return 0.0, False, "Insufficient score to close incident"
        return 1.0, True, None

    return 0.0, False, f"Unknown action type: {action_type}"