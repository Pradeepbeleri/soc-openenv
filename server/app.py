from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from env.environment import OpenEnvSOCEnvironment

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
def reset(req: ResetRequest):
    try:
        observation = env.reset(task=req.task)
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