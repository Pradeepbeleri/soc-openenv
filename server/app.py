from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from env.environment import SOCEnvironment

app = FastAPI()
env = SOCEnvironment()


class ResetRequest(BaseModel):
    task: Optional[str] = "easy"


class StepRequest(BaseModel):
    type: str
    target: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(req: ResetRequest):
    return {"state": env.reset(task=req.task or "easy")}


@app.get("/state")
def state():
    return env.get_state()


@app.post("/step")
def step(req: StepRequest):
    try:
        return env.step(
            {"type": req.type, "target": req.target, "details": req.details or {}}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))