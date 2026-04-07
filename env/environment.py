from typing import Dict, Any
from env.models import EnvironmentState, StepResult, Alert, LogEntry
from env.grader import grade_action


class SOCEnvironment:
    def __init__(self):
        self.state = self._initial_state()

    def _initial_state(self) -> EnvironmentState:
        return EnvironmentState(
            task="easy",
            attack_ip="192.168.1.234",
            alerts=[
                Alert(
                    id="ALERT-001",
                    severity="high",
                    type="suspicious_activity",
                    description="Multiple failed login attempts detected",
                    source_ip="192.168.1.234",
                )
            ],
            logs=[
                LogEntry(
                    timestamp="2026-04-07T12:00:00Z",
                    source_ip="192.168.1.234",
                    destination_ip="10.0.0.5",
                    action="failed_login",
                    protocol="tcp",
                )
            ],
        )

    def reset(self, task: str = "easy") -> Dict[str, Any]:
        self.state = self._initial_state()
        self.state.task = task
        return self.state.model_dump()

    def get_state(self) -> Dict[str, Any]:
        return self.state.model_dump()

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if self.state.done:
            return StepResult(
                observation=self.state.model_dump(),
                reward=0.0,
                done=True,
                info={"error": "Environment already completed"},
            ).model_dump()

        self.state.step_count += 1
        reward, done, error = grade_action(self.state, action)

        self.state.score += float(reward)
        self.state.history.append(f"{action.get('type')}:{action.get('target')}")

        if done or self.state.step_count >= self.state.max_steps:
            self.state.done = True

        if self.state.done and self.state.score >= 1.0:
            self.state.score = 1.0

        return StepResult(
            observation=self.state.model_dump(),
            reward=float(reward),
            done=self.state.done,
            info={"error": error},
        ).model_dump()