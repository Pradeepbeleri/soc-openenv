from typing import Dict, Any
from env.models import EnvironmentState, StepResult, Alert, LogEntry
from env.grader import grade_task_1, grade_task_2, grade_task_3


class SOCEnvironment:
    def __init__(self):
        self.state = self._initial_state()

    def _initial_state(self, task: str = "task_1") -> EnvironmentState:
        return EnvironmentState(
            task=task,
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

    def reset(self, task: str = "task_1") -> Dict[str, Any]:
        self.state = self._initial_state(task=task)
        return self.state.model_dump()

    def get_state(self) -> Dict[str, Any]:
        return self.state.model_dump()

    def _grade(self, action: Dict[str, Any]) -> float:
        if self.state.task == "task_1":
            reward = grade_task_1(action)
        elif self.state.task == "task_2":
            reward = grade_task_2(action)
        elif self.state.task == "task_3":
            reward = grade_task_3(action)
        else:
            reward = 0.50

        return max(0.01, min(0.99, float(reward)))

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if self.state.done:
            return StepResult(
                observation=self.state.model_dump(),
                reward=0.01,
                done=True,
                info={"error": "Environment already completed"},
            ).model_dump()

        self.state.step_count += 1
        reward = self._grade(action)
        done = self.state.step_count >= self.state.max_steps
        error = None

        self.state.score += reward
        self.state.history.append(f"{action.get('type')}:{action.get('target')}")

        if done:
            self.state.done = True

        if self.state.score >= 1.0:
            self.state.score = 0.99

        return StepResult(
            observation=self.state.model_dump(),
            reward=reward,
            done=self.state.done,
            info={"error": error},
        ).model_dump()
