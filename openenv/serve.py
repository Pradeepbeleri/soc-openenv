"""
OpenEnv FastAPI Server for SOC Analyst Environment
---------------------------------------------------
Provides HTTP endpoints for environment interaction.
Compliant with OpenEnv 2026 specification.
"""
from fastapi import FastAPI
from env.environment import SOCEnv
from env.models import Action

app = FastAPI()
env = SOCEnv()

@app.post("/reset")
def reset(data: dict):
    """Reset environment and return initial observation."""
    task = data.get("task", "easy")
    obs = env.reset(task)
    return obs.model_dump()

@app.post("/step")
def step(action: Action):
    """Execute action and return (observation, reward, done, info)."""
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    """Get current environment state for grading."""
    return env.state()

@app.post("/close")
def close():
    """Reset environment."""
    env.reset()
    return {"status": "closed"}
