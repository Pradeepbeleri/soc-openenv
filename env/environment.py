import random
from typing import Dict, Any
from env.models import Alert, LogEntry
from env.grader import SOCGrader


TASK_CONFIG = {
    "easy": {
        "max_steps": 4,
        "severity": "high",
        "log_count": 1,
        "reward_monitor": 0.35,
        "reward_block": 2.0,
    },
    "medium": {
        "max_steps": 5,
        "severity": "critical",
        "log_count": 2,
        "reward_monitor": 0.25,
        "reward_block": 2.3,
    },
    "hard": {
        "max_steps": 6,
        "severity": "critical",
        "log_count": 3,
        "reward_monitor": 0.15,
        "reward_block": 2.7,
    },
}


class OpenEnvSOCEnvironment:
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.grader = SOCGrader()
        self.reset("easy")

    def _new_attack_ip(self) -> str:
        return f"192.168.1.{random.randint(10, 250)}"

    def _make_logs(self, attack_ip: str, count: int):
        logs = []
        for i in range(count):
            logs.append(
                LogEntry(
                    timestamp=f"22:{10 + i:02d}",
                    source_ip=attack_ip,
                    destination_ip="10.0.0.5",
                    action="MALICIOUS_LOGIN" if i == 0 else "LATERAL_MOVEMENT",
                    protocol="TCP",
                )
            )
        return logs

    def reset(self, task: str = "easy"):
        if task not in TASK_CONFIG:
            raise ValueError("Invalid task. Choose one of: easy, medium, hard")

        cfg = TASK_CONFIG[task]
        attack_ip = self._new_attack_ip()

        self.state = {
            "task": task,
            "attack_ip": attack_ip,
            "alerts": [
                Alert(
                    id="A1",
                    severity=cfg["severity"],
                    type="Anomalous Traffic",
                    description="Suspected brute force activity detected",
                    source_ip=attack_ip,
                )
            ],
            "logs": [],
            "history": [],
            "step_count": 0,
            "done": False,
            "max_steps": cfg["max_steps"],
            "score": 0.0,
            "task_config": cfg,
            "evidence_revealed": False,
        }

        return self._observation()

    def _observation(self):
        return {
            "alerts": [a.model_dump() for a in self.state["alerts"]],
            "logs": [l.model_dump() for l in self.state["logs"]],
            "history": self.state["history"],
            "step_count": self.state["step_count"],
            "done": self.state["done"],
        }

    def get_state(self):
        return {
            "task": self.state["task"],
            "attack_ip": self.state["attack_ip"],
            "history": self.state["history"],
            "step_count": self.state["step_count"],
            "done": self.state["done"],
            "max_steps": self.state["max_steps"],
            "score": self.state["score"],
        }

    def step(self, action_type: str, target: str):
        if self.state["done"]:
            return {
                "observation": self._observation(),
                "reward": 0.0,
                "done": True,
                "info": {"message": "Episode already completed"},
            }

        self.state["step_count"] += 1
        self.state["history"].append(f"{action_type}({target})")

        reward = -0.05
        info = {}

        attack_ip = self.state["attack_ip"]
        cfg = self.state["task_config"]

        if action_type == "monitor":
            if target == attack_ip:
                if not self.state["evidence_revealed"]:
                    self.state["logs"] = self._make_logs(attack_ip, cfg["log_count"])
                    self.state["evidence_revealed"] = True
                reward = cfg["reward_monitor"]
                info["message"] = "Correct IP monitored"
            else:
                reward = -0.15
                info["message"] = "Monitored non-suspicious IP"

        elif action_type == "block_ip":
            if target == attack_ip:
                reward = cfg["reward_block"]
                self.state["done"] = True
                info["message"] = "Correct IP blocked"
                self.state["score"] = self.grader.score(self.get_state())
                info["score"] = self.state["score"]
            else:
                reward = -0.4
                info["message"] = "Blocked wrong IP"

        elif action_type == "investigate":
            if target == attack_ip:
                reward = 0.2
                info["message"] = "Investigation added context"
            else:
                reward = -0.1
                info["message"] = "Investigation found nothing useful"

        else:
            raise ValueError("Invalid action type. Use monitor, block_ip, or investigate.")

        if self.state["step_count"] >= self.state["max_steps"] and not self.state["done"]:
            self.state["done"] = True
            info["message"] = info.get("message", "") + " | Max steps reached"
            self.state["score"] = self.grader.score(self.get_state())
            info["score"] = self.state["score"]

        if self.state["done"] and "score" not in info:
            self.state["score"] = self.grader.score(self.get_state())
            info["score"] = self.state["score"]

        return {
            "observation": self._observation(),
            "reward": round(reward, 2),
            "done": self.state["done"],
            "info": info,
        }