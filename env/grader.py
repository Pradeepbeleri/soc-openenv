from typing import Dict, Any


class SOCGrader:
    def score(self, state: Dict[str, Any]) -> float:
        """
        Simple offline scoring logic.
        Higher score if the correct sequence was followed with fewer steps.
        """
        history = state.get("history", [])
        step_count = state.get("step_count", 0)
        done = state.get("done", False)

        if not done:
            return 0.0

        base = 0.7

        if any(h.startswith("monitor(") for h in history):
            base += 0.1
        if any(h.startswith("block_ip(") for h in history):
            base += 0.15

        efficiency_bonus = max(0.0, 0.15 - 0.03 * max(0, step_count - 2))
        return round(min(1.0, base + efficiency_bonus), 2)