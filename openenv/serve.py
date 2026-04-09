from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from env.environment import SOCEnvironment

app = FastAPI(title="OpenEnv SOC Environment")
env = SOCEnvironment()


class ResetRequest(BaseModel):
    task: Optional[Literal["task_1", "task_2", "task_3"]] = "task_1"


class StepRequest(BaseModel):
    action_type: str
    target: Optional[str] = None
    flagged: Optional[bool] = None
    quarantine: Optional[bool] = None
    false_positive: Optional[bool] = None
    documented: Optional[bool] = None
    alert_severity: Optional[str] = None
    evidence_collected: Optional[bool] = None
    incident_closed: Optional[bool] = None
    details: Optional[Dict[str, Any]] = None


@app.get("/")
def root():
    return {"message": "SOC OpenEnv is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(req: ResetRequest):
    return {"state": env.reset(task=req.task or "task_1")}


@app.get("/state")
def state():
    return env.get_state()


@app.post("/step")
def step(req: StepRequest):
    try:
        payload = req.model_dump()
        if payload.get("details") is None:
            payload["details"] = {}
        return env.step(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
