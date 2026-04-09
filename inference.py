import os
import sys
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")


def main():
    success = False
    steps = 0
    rewards = []

    try:
        print(f"[START] task=openenv env=proxy-check model={MODEL_NAME}")

        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY,
        )

        # This must produce at least one API call through the LiteLLM proxy
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Respond with a single word: OK"}
            ],
        )

        answer = response.choices[0].message.content.strip()

        steps = 1
        rewards.append(0.00)

        print(
            "[STEP] step=1 action=llm_call reward=0.00 done=true error=null"
        )

        print(answer)
        success = True

    except Exception as e:
        steps = max(steps, 1)
        print(
            f"[STEP] step={steps} action=llm_call reward=0.00 done=true error={str(e)}"
        )
        success = False

    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(
            f"[END] success={'true' if success else 'false'} "
            f"steps={steps} rewards={rewards_str}"
        )


if __name__ == "__main__":
    main()
 
