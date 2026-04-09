from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel

from env.environment import SOCEnvironment

app = FastAPI(title="SOC Phishing Triage Environment")
env = SOCEnvironment()


class ResetRequest(BaseModel):
    task: Optional[str] = "task_1"


@app.get("/")
def root():
    return {"message": "SOC Phishing Triage is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metadata")
def metadata():
    return {
        "name": "SOC Email Triage",
        "description": "SOC analyst training environment for triaging highly obfuscated phishing emails."
    }


@app.get("/schema")
def schema():
    return {
        "action": {
            "type": "object",
            "properties": {
                "action_type": {
                    "type": "string", 
                    "enum": ["read_headers", "read_body", "scan_attachments", "resolve"],
                    "description": "The analytical action to take."
                },
                "decision": {
                    "type": "string",
                    "description": "If action_type is resolve, provide the decision (benign, spam, phishing, malware)."
                }
            }
        },
        "observation": {
            "type": "object",
            "properties": {
                "step_count": {"type": "integer"},
                "action_output": {"type": "string"}
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
            
        return env.step(payload)
    except Exception as e:
        return {
            "observation": env.get_state(),
            "reward": 0.01,
            "done": True,
            "info": {"error": str(e), "score": 0.01},
            "score": 0.01
        }
