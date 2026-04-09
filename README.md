# SOC Phishing Triage Environment

A realistic OpenEnv environment designed for training and evaluating autonomous Security Operations Center (SOC) agents in triaging complex phishing emails. 

## Motivation
Email remains the primary attack vector for enterprise breaches. SOC analysts suffer from extreme alert fatigue analyzing thousands of suspicious emails daily. This environment provides a completely secure sandbox to train LLM-driven agents to read email headers, analyze body text, inspect attachments for malicious payloads, and confidently close out tickets. By testing against varying levels of obfuscation, it benchmarks whether frontier models possess the deductive reasoning necessary for Tier-1 SOC automation.

## Action Space
The agent interacts with the environment by outputting JSON payloads targeting the `/step` endpoint.
```json
{
  "action_type": "<read_headers|read_body|scan_attachments|resolve>",
  "decision": "<spam|phishing|malware|benign>" // Required only if action_type is 'resolve'
}
```

## Observation Space
The environment returns structured analytical data based on the action taken.
```json
{
  "step_count": 1,
  "action_output": "Sender Address: lottery-winner@free-cash-528.com"
}
```

## Tasks & Difficulties
- **`task_1` (Easy)**: Basic Spam. Features blatantly obvious keywords and sender domains. Agent resolves it quickly. Max Score: 0.90
- **`task_2` (Medium)**: Phishing Attempt. Uses visual homoglyphs in the domain (e.g., paypaI instead of paypal) and high-urgency lock warnings. Agent must carefully parse the headers. Max Score: 0.95
- **`task_3` (Hard)**: Stealth Macro Malware. The sender is a trusted internal vendor and the body is benign. The danger lies cleanly hidden inside a malicious macro attachment. The agent must proactively invoke `scan_attachments` before making a decision. Max Score: 0.99

## Rewards
The reward function yields partial fractional progress limits strictly clamped inside `(0.01, 0.99)`:
- `+0.20`: For analyzing headers and body structure.
- `+0.15`: For executing an attachment scan against advanced payloads.
- `+0.35`: For mathematically selecting the perfect resolution closure.
- `-0.10`: Penalty for classifying a malicious email incorrectly.

## Setup Instructions
```bash
# Build the container
docker build -t soc-openenv:latest .

# Run the env server on port 7860
docker run -p 7860:7860 soc-openenv:latest
```

## Baseline Validation
Execute the deterministic baseline validation script using your OpenAI API keys:
```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4"
export HF_TOKEN="your-token"

python inference.py
```

### Baseline Scores
- `task_1`: Score = ~0.80
- `task_2`: Score = ~0.80
- `task_3`: Score = ~0.95
