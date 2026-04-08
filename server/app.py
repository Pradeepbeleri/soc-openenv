from typing import Any, Dict, Optional, Literal

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from env.environment import SOCEnvironment

app = FastAPI()
env = SOCEnvironment()


@app.get("/")
def root():
    return {"message": "Working"}


class ResetRequest(BaseModel):
    task: Optional[Literal["task_1", "task_2", "task_3"]] = "task_1"


class StepRequest(BaseModel):
    type: str
    target: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(req: Optional[ResetRequest] = Body(default=None)):
    try:
        task = req.task if req and req.task else "task_1"
        observation = env.reset(task=task)
        return observation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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


def main():
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
