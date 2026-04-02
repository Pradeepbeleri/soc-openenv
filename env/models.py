from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class Alert(BaseModel):
    id: str
    severity: str
    type: str
    description: str
    source_ip: str


class LogEntry(BaseModel):
    timestamp: str
    source_ip: str
    destination_ip: str
    action: str
    protocol: str


class EnvironmentState(BaseModel):
    task: str
    attack_ip: str
    alerts: List[Alert] = Field(default_factory=list)
    logs: List[LogEntry] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)
    step_count: int = 0
    done: bool = False
    max_steps: int = 5
    score: float = 0.0


class StepResult(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)