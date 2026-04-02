from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from env.environment import OpenEnvSOCEnvironment
from typing import Optional
from fastapi import Body, HTTPException


app = FastAPI(title="SOC Analyst OpenEnv Environment")

env = OpenEnvSOCEnvironment()


class ResetRequest(BaseModel):
    task: str = "easy"


class StepRequest(BaseModel):
    type: str
    target: str


@app.get("/")
def root():
    return {"message": "SOC Analyst OpenEnv Environment is running"}


@app.post("/reset")
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
        result = env.step(action_type=req.type, target=req.target)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    return env.get_state()

@app.get("/state")
def state():
    return env.get_state()
