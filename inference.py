import os
import sys
import traceback
from typing import Any, Dict, List, Optional

import requests
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
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


def get_llm_action(task: str, attack_ip: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": f"Choose the next best action for task={task} and ip={attack_ip}. "
                           f"Return only one of: monitor, block_ip, close_incident.",
            }
        ],
    )
    text = response.choices[0].message.content.strip().lower()
    if "block" in text:
        return "block_ip"
    if "close" in text:
        return "close_incident"
    return "monitor"


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

        first_action = get_llm_action(task, attack_ip)

        if first_action == "monitor":
            result = env_post("/step", {"type": "monitor", "target": attack_ip, "details": {}})
            action_str = f"monitor('{attack_ip}')"
        elif first_action == "block_ip":
            result = env_post("/step", {"type": "block_ip", "target": attack_ip, "details": {}})
            action_str = f"block_ip('{attack_ip}')"
        else:
            result = env_post("/step", {"type": "close_incident", "details": {}})
            action_str = "close_incident()"

        steps += 1
        reward = float(result.get("reward", 0.0))
        rewards.append(reward)
        done = bool(result.get("done", False))
        print_step(steps, action_str, reward, done, get_error(result))

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
