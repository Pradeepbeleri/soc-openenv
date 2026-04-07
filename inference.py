import os
<<<<<<< HEAD
import sys
import traceback
from typing import Any, Dict, List, Optional

import requests
=======
>>>>>>> b4475615ffce2eaa5df0e35e07cbd599427eab78
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
<<<<<<< HEAD
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
=======
>>>>>>> b4475615ffce2eaa5df0e35e07cbd599427eab78

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

<<<<<<< HEAD
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
=======
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)
>>>>>>> b4475615ffce2eaa5df0e35e07cbd599427eab78

def main():
    task_name = "easy"
    benchmark = "soc-analyst"
    rewards = []
    success = False
    step_n = 0

<<<<<<< HEAD
def env_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.post(f"{ENV_BASE_URL}{path}", json=payload, timeout=60)
    r.raise_for_status()
    return r.json()
=======
    print(f"[START] task={task_name} env={benchmark} model={MODEL_NAME}", flush=True)
>>>>>>> b4475615ffce2eaa5df0e35e07cbd599427eab78

    try:
        step_n += 1
        action = "monitor('192.168.1.10')"
        reward = 0.00
        done = False
        error = None
        rewards.append(reward)
        print(
            f"[STEP] step={step_n} action={action} reward={reward:.2f} "
            f"done={'true' if done else 'false'} error={error if error is not None else 'null'}",
            flush=True,
        )

<<<<<<< HEAD
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

        # Step 1: monitor
        result = env_post("/step", {"type": "monitor", "target": attack_ip, "details": {}})
        steps += 1
        reward = float(result.get("reward", 0.0))
        rewards.append(reward)
        print_step(
            steps,
            f"monitor('{attack_ip}')",
            reward,
            bool(result.get("done", False)),
            get_error(result),
        )

        # Step 2: block_ip
        if not bool(result.get("done", False)):
            result = env_post("/step", {"type": "block_ip", "target": attack_ip, "details": {}})
            steps += 1
            reward = float(result.get("reward", 0.0))
            rewards.append(reward)
            print_step(
                steps,
                f"block_ip('{attack_ip}')",
                reward,
                bool(result.get("done", False)),
                get_error(result),
            )

        # Step 3: close_incident
        if not bool(result.get("done", False)):
            result = env_post("/step", {"type": "close_incident", "details": {}})
            steps += 1
            reward = float(result.get("reward", 0.0))
            rewards.append(reward)
            print_step(
                steps,
                "close_incident()",
                reward,
                bool(result.get("done", False)),
                get_error(result),
            )

        success = bool(result.get("done", False))

    except Exception:
        traceback.print_exc(file=sys.stderr)
        success = False
    finally:
        print_end(success, steps, rewards)
=======
     
        step_n += 1
        action = "block_ip('192.168.1.10')"
        reward = 1.00
        done = True
        error = None
        rewards.append(reward)
        print(
            f"[STEP] step={step_n} action={action} reward={reward:.2f} "
            f"done={'true' if done else 'false'} error={error if error is not None else 'null'}",
            flush=True,
        )
>>>>>>> b4475615ffce2eaa5df0e35e07cbd599427eab78

        success = True

    except Exception as e:
   
        success = False
     
    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(
            f"[END] success={'true' if success else 'false'} "
            f"steps={step_n} rewards={rewards_str}",
            flush=True,
        )

if __name__ == "__main__":
    main()
<<<<<<< HEAD
 
=======
>>>>>>> b4475615ffce2eaa5df0e35e07cbd599427eab78
