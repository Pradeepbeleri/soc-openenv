from typing import Any, Dict

from env.grader import grade_task_1, grade_task_2, grade_task_3
from env.models import Alert, EnvironmentState, LogEntry, StepResult


class SOCEnvironment:
    def __init__(self, task: str = "task_1"):
        self.state = self._initial_state(task)

    def _initial_state(self, task: str) -> EnvironmentState:
        if task == "task_1":
            return EnvironmentState(
                task="task_1",
                alerts=[
                    Alert(
                        id="A-001",
                        severity="high",
                        type="bruteforce",
                        description="Multiple failed logins from a single source IP",
                        source_ip="192.168.1.50",
                    )
                ],
                logs=[
                    LogEntry(
                        timestamp="2026-04-09T08:00:00Z",
                        source_ip="192.168.1.50",
                        destination_ip="10.0.0.10",
                        action="failed_login",
                        protocol="tcp",
                    )
                ],
            )

        if task == "task_2":
            return EnvironmentState(
                task="task_2",
                alerts=[
                    Alert(
                        id="A-010",
                        severity="medium",
                        type="suspicious_dns",
                        description="Unusual DNS traffic to known domain",
                        source_ip="172.16.0.24",
                    ),
                    Alert(
                        id="A-011",
                        severity="low",
                        type="auth_noise",
                        description="Repeated benign auth failures from test user",
                        source_ip="172.16.0.11",
                    ),
                ],
                logs=[
                    LogEntry(
                        timestamp="2026-04-09T08:10:00Z",
                        source_ip="172.16.0.24",
                        destination_ip="8.8.8.8",
                        action="dns_query",
                        protocol="udp",
                    )
                ],
            )

        return EnvironmentState(
            task="task_3",
            alerts=[
                Alert(
                    id="A-020",
                    severity="high",
                    type="lateral_movement",
                    description="Possible lateral movement detected",
                    source_ip="10.1.2.9",
                )
            ],
            logs=[
                LogEntry(
                    timestamp="2026-04-09T08:20:00Z",
                    source_ip="10.1.2.9",
                    destination_ip="10.1.2.20",
                    action="remote_exec",
                    protocol="tcp",
                )
            ],
        )

    def reset(self, task: str = "task_1") -> Dict[str, Any]:
        self.state = self._initial_state(task)
        return self.state.model_dump()

    def get_state(self) -> Dict[str, Any]:
        return self.state.model_dump()

    def _grade(self, state: EnvironmentState) -> float:
        if state.task == "task_1":
            return grade_task_1(state)
        if state.task == "task_2":
            return grade_task_2(state)
        return grade_task_3(state)

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if self.state.done:
            return StepResult(
                observation=self.state.model_dump(),
                reward=0.0,
                done=True,
                info={"error": "environment already completed"},
            ).model_dump()

        self.state.step_count += 1
        self.state.history.append(action)

        # Update environment tracking state based on action payload
        action_type = action.get("action_type")
        if action_type == "investigate":
            self.state.investigated = True
        elif action_type == "triage":
            self.state.triage_done = True

        if action.get("quarantine") is True:
            self.state.quarantine_applied = True
        if action.get("false_positive") is True:
            self.state.false_positive_marked = True
        if action.get("incident_closed") is True:
            self.state.incident_closed = True
        if action.get("evidence_collected") is True:
            self.state.evidence_collected_state = True
        if action.get("documented") is True:
            self.state.documented_state = True
        if action.get("flagged") is True:
            self.state.flagged_state = True
        if action.get("alert_severity") in {"low", "medium", "high"}:
            self.state.severity_assessed = True

        old_score = self.state.score
        new_score = self._grade(self.state)
        
        # Calculate shaped reward so that the cumulative sum explicitly matches new_score
        reward = round(new_score - old_score, 2)
        self.state.score = new_score

        if self.state.step_count >= self.state.max_steps or self.state.incident_closed:
            self.state.done = True

        return StepResult(
            observation=self.state.model_dump(),
            reward=reward,
            done=self.state.done,
            info={"error": None},
            score=self.state.score
        ).model_dump()
