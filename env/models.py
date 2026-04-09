from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


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
    alerts: List[Alert] = Field(default_factory=list)
    logs: List[LogEntry] = Field(default_factory=list)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    step_count: int = 0
    done: bool = False
    max_steps: int = 5
    score: float = 0.0
    incident_closed: bool = False
    quarantine_applied: bool = False
    false_positive_marked: bool = False


class StepResult(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)
    score: float = 0.0


class StepResult(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)
