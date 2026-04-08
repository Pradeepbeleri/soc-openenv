import os
import sys
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")


def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    task = os.getenv("TASK_NAME", "unknown")
    benchmark = os.getenv("BENCHMARK_NAME", "unknown")

    print(f"[START] task={task} env={benchmark} model={MODEL_NAME}")

    steps = 0
    rewards = []
    success = False

    try:
        # Minimal safe behavior: make one LLM call and emit one step.
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Return a single action for a SOC incident response task."}
            ],
        )
        action = response.choices[0].message.content.strip().replace("\n", " ")

        steps = 1
        reward = 0.00
        rewards.append(reward)
        print(f"[STEP] step=1 action={action} reward={reward:.2f} done=false error=null")

    except Exception as e:
        print(f"[STEP] step=1 action=none reward=0.00 done=false error={str(e).replace(chr(10), ' ')}")
    finally:
        print(f"[END] success={str(success).lower()} steps={steps} rewards={','.join(f'{r:.2f}' for r in rewards)}")


if __name__ == "__main__":
    main()
