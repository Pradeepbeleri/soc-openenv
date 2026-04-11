import copy
from typing import Any, Dict, Optional

from pydantic import BaseModel

from .models import EnvironmentState, StepResult
import env.grader as grader


def _safe_score(score: float) -> float:
    """Clamp to strictly (0, 1) — never 0.0 or 1.0."""
    return max(0.02, min(0.98, float(score)))


class SOCEnvironment:
    def __init__(self):
        self.state = self._initial_state("task_1")

    def _initial_state(self, task: str) -> EnvironmentState:
        state = EnvironmentState(task=task)
        if task == "task_1":
            state.sender_domain = "lottery-winner@free-cash-528.com"
            state.email_body = "URGENT: YOU WON! Click here to claim your $5,000,000 instantly."
            state.attachment_virus = False
            state.correct_resolution = "spam"
        elif task == "task_2":
            state.sender_domain = "security-update@paypaI-support.com"  # Fake L
            state.email_body = "Your account has been locked due to suspicious activity. Log in at the prompt to unlock."
            state.attachment_virus = False
            state.correct_resolution = "phishing"
        elif task == "task_3":
            state.sender_domain = "john.doe@trusted-vendor.com"
            state.email_body = "Hey, please review the attached Q4 invoicing manifest for sign-off. - John"
            state.attachment_virus = True
            state.correct_resolution = "malware"

        state.score = 0.02  # Safe default strictly inside (0, 1)
        return state

    def reset(self, task: str = "task_1") -> Dict[str, Any]:
        self.state = self._initial_state(task)
        return self._get_observation()

    def _get_observation(self) -> Dict[str, Any]:
        return {
            "step_count": self.state.step_count,
            "max_steps": self.state.max_steps,
            "done": self.state.done
        }

    def get_state(self) -> Dict[str, Any]:
        return self.state.model_dump()

    def _grade(self, state: EnvironmentState) -> float:
        d = state.model_dump()
        if state.task == "task_1":
            return grader.grade_task_1(d)
        elif state.task == "task_2":
            return grader.grade_task_2(d)
        elif state.task == "task_3":
            return grader.grade_task_3(d)
        return 0.02

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if self.state.done:
            final_score = _safe_score(self.state.score)
            return StepResult(
                observation=self._get_observation(),
                reward=0.02,
                done=True,
                info={"error": "environment completed", "score": final_score},
                score=final_score
            ).model_dump()

        self.state.step_count += 1
        action_type = action.get("action_type")
        action_output = "Action taken."

        if action_type == "read_headers":
            self.state.headers_read = True
            action_output = f"Sender Address: {self.state.sender_domain}"
        elif action_type == "read_body":
            self.state.body_read = True
            action_output = f"Body Content: {self.state.email_body}"
        elif action_type == "scan_attachments":
            self.state.attachments_scanned = True
            action_output = "Threat Report: Malicious Macros Detected!" if self.state.attachment_virus else "Threat Report: Clean"
        elif action_type == "resolve":
            decision = action.get("decision")
            self.state.resolution = str(decision).lower() if decision else "unknown"
            self.state.done = True
            action_output = f"Resolved task as {self.state.resolution}."

        if self.state.step_count >= self.state.max_steps:
            self.state.done = True

        new_score = self._grade(self.state)
        delta = max(0.0, new_score - self.state.score)
        reward = _safe_score(0.02 + delta * 0.9)
        self.state.score = new_score

        obs = self._get_observation()
        obs["action_output"] = action_output

        final_score = _safe_score(self.state.score)
        return StepResult(
            observation=obs,
            reward=reward,
            done=self.state.done,
            info={"error": None, "score": final_score},
            score=final_score
        ).model_dump()
