import os
import sys
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")


def print_start():
    print(f"[START] model={MODEL_NAME}")


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


def main():
    success = False
    steps = 0
    rewards = []

    try:
        print_start()

        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY,
        )

        # This is the actual API call that should be observed by the proxy
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Say hello in one short sentence."}
            ],
        )

        answer = response.choices[0].message.content.strip()
        steps = 1
        rewards.append(0.0)

        print_step(
            step=1,
            action="llm_call",
            reward=0.00,
            done=True,
            error=None,
        )

        print(answer)
        success = True

    except Exception as e:
        steps = max(steps, 1)
        print_step(
            step=steps,
            action="llm_call",
            reward=0.00,
            done=True,
            error=str(e),
        )

    finally:
        print_end(success=success, steps=steps, rewards=rewards)


if __name__ == "__main__":
    main()
