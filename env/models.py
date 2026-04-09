from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EnvironmentState(BaseModel):
    task: str
    step_count: int = 0
    max_steps: int = 5
    done: bool = False
    score: float = 0.01  # Safe default within (0, 1) bounds

    # Investigation Flags (Partial progress signals)
    headers_read: bool = False
    body_read: bool = False
    attachments_scanned: bool = False
    
    # Task Resolution
    resolution: Optional[str] = None
    
    # Static data for current task (hidden from agent observation)
    sender_domain: str = ""
    email_body: str = ""
    attachment_virus: bool = False
    correct_resolution: str = ""

class StepResult(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)
    score: float = 0.01
