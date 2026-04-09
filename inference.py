import os
import sys
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")


def print_start():
    print(f"[START] task=demo env=openenv model={MODEL_NAME}")


def print_step(step: int, action: str, reward: float, done: bool, error: str | None):
    err = error if error is not None else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={'true' if done else 'false'} error={err}"
    )


def print_end(success: bool, steps: int, rewards: list[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={'true' if success else 'false'} "
        f"steps={steps} rewards={rewards_str}"
    )


def run_inference():
    if HF_TOKEN is None:
        raise ValueError("HF_TOKEN environment variable is required")

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    # Replace this with your real episode logic if needed
    prompt = "Hello from OpenEnv!"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    success = False
    steps = 0
    rewards = []

    try:
        print_start()

        result = run_inference()
        steps = 1
        rewards.append(0.00)
        print_step(
            step=1,
            action="llm_call()",
            reward=0.00,
            done=True,
            error=None,
        )

        success = True
        print(result)

    except Exception as e:
        print_step(
            step=max(1, steps + 1),
            action="llm_call()",
            reward=0.00,
            done=True,
            error=str(e),
        )
        success = False

    finally:
        print_end(success=success, steps=steps, rewards=rewards)
