import os
import sys
import traceback
from typing import Any, Dict, List, Optional

import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
)


def fmt_err(err: Optional[Any]) -> str:
    return "null" if err is None else str(err).replace("\n", " ").strip()


def print_start(task: str, env_name: str) -> None:
    print(f"[START] task={task} env={env_name} model={MODEL_NAME}", flush=True)


def print_step(step_n: int, action: str, reward: float, done: bool, error: Optional[Any]) -> None:
    print(
        f"[STEP] step={step_n} action={action} reward={reward:.2f} "
        f"done={'true' if done else 'false'} error={fmt_err(error)}",
        flush=True,
    )


def print_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={'true' if success else 'false'} steps={steps} rewards={rewards_str}",
        flush=True,
    )


def env_get(path: str) -> Dict[str, Any]:
    r = requests.get(f"{ENV_BASE_URL}{path}", timeout=60)
    r.raise_for_status()
    return r.json()


def env_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.post(f"{ENV_BASE_URL}{path}", json=payload, timeout=60)
    r.raise_for_status()
    return r.json()


def get_error(result: Dict[str, Any]) -> Optional[Any]:
    info = result.get("info")
    if isinstance(info, dict):
        return info.get("error")
    return None


def main() -> None:
    rewards: List[float] = []
    steps = 0
    success = False

    task = os.getenv("TASK_NAME", "easy")
    env_name = os.getenv("BENCHMARK_NAME", "soc-analyst-openenv")

    print_start(task, env_name)

    try:
        env_post("/reset", {"task": task})
        state = env_get("/state")
        attack_ip = state.get("attack_ip", "192.168.1.234")

        result = env_post("/step", {"type": "monitor", "target": attack_ip, "details": {}})
        steps += 1
        reward = float(result.get("reward", 0.0))
        rewards.append(reward)
        done = bool(result.get("done", False))
        print_step(steps, f"monitor('{attack_ip}')", reward, done, get_error(result))

        if not done:
            result = env_post("/step", {"type": "block_ip", "target": attack_ip, "details": {}})
            steps += 1
            reward = float(result.get("reward", 0.0))
            rewards.append(reward)
            done = bool(result.get("done", False))
            print_step(steps, f"block_ip('{attack_ip}')", reward, done, get_error(result))

        if not done:
            result = env_post("/step", {"type": "close_incident", "details": {}})
            steps += 1
            reward = float(result.get("reward", 0.0))
            rewards.append(reward)
            done = bool(result.get("done", False))
            print_step(steps, "close_incident()", reward, done, get_error(result))

        success = done

    except Exception:
        traceback.print_exc(file=sys.stderr)
        success = False

    finally:
        print_end(success, steps, rewards)


if __name__ == "__main__":
    main()
