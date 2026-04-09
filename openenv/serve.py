from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel

from env.environment import SOCEnvironment

app = FastAPI(title="OpenEnv SOC Environment")
env = SOCEnvironment()


class ResetRequest(BaseModel):
    task: Optional[str] = "task_1"


@app.get("/")
def root():
    return {"message": "SOC OpenEnv is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metadata")
def metadata():
    return {
        "name": "SOC OpenEnv",
        "description": "Security Operations Center simulation involving log analysis, triage, and threat quarantine."
    }


@app.get("/schema")
def schema():
    # Phase 2 Open LLMs dynamically retrieve this to construct perfectly typed JSON actions! 
    # Without this, they hallucinate garbage actions resulting in a variance of 0.0!
    return {
        "action": {
            "type": "object",
            "properties": {
                "action_type": {
                    "type": "string", 
                    "description": "The primary operation to run (investigate, triage, contain, etc.)"
                },
                "target": {"type": "string"},
                "flagged": {"type": "boolean"},
                "quarantine": {"type": "boolean"},
                "false_positive": {"type": "boolean"},
                "documented": {"type": "boolean"},
                "alert_severity": {"type": "string"},
                "evidence_collected": {"type": "boolean"},
                "incident_closed": {"type": "boolean"}
            }
        },
        "observation": {
            "type": "object",
            "properties": {
                "alerts": {"type": "array"},
                "logs": {"type": "array"},
                "step_count": {"type": "integer"}
            }
        },
        "state": {
            "type": "object",
            "properties": {
                "score": {"type": "number"},
                "task": {"type": "string"}
            }
        }
    }


@app.post("/reset")
def reset(req: Optional[ResetRequest] = Body(default=None)):
    task = req.task if req and req.task else "task_1"
    return {"state": env.reset(task=task)}


@app.get("/state")
def state():
    return env.get_state()


@app.post("/step")
async def step(request: Request):
    try:
        try:
            payload = await request.json()
        except Exception:
            payload = {}
            
        if not isinstance(payload, dict):
            payload = {"payload_received": str(payload)}
            
        if payload.get("details") is None:
            payload["details"] = {}
            
        return env.step(payload)
    except Exception as e:
        return {
            "observation": env.get_state(),
            "reward": 0.01,
            "done": True,
            "info": {"error": str(e), "score": 0.01},
            "score": 0.01
        }
