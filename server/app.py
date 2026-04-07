from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from typing import Any, Dict, Optional
from env.environment import SOCEnvironment

from env.environment import OpenEnvSOCEnvironment
from typing import Optional


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

def reset(req: Optional[ResetRequest] = Body(default=None)):
    try:
        task = req.task if req and req.task else "easy"
        observation = env.reset(task=task)
        return observation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/step")
def step(req: StepRequest):
    try:

        return env.step(
            {"type": req.type, "target": req.target, "details": req.details or {}}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

        result = env.step(action_type=req.type, target=req.target)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    return env.get_state()


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()

