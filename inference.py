import os
import sys
from openai import OpenAI

def main():
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"],
        )

        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
            messages=[{"role": "user", "content": "Reply with OK"}],
        )

        print(response.choices[0].message.content)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
