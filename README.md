# 🛡️ SOC Analyst OpenEnv

Build an AI agent for incident response in a simulated Security Operations Center (SOC) workflow.
This OpenEnv environment lets participants create reinforcement-learning agents that detect suspicious activity, monitor network behavior, block malicious IPs, and complete incident response actions in a structured workflow.

## Why this project?

- Realistic SOC-style incident response
- OpenEnv-compatible environment design
- Clear task progression for RL agents
- Built for reproducible local testing and Hugging Face Spaces deployment

This environment simulates a SOC incident response workflow where the agent must infer, investigate, and mitigate a malicious IP using structured observations and actions.
---
.
## ✨ Features
## Quick Start
### 1. Setup
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Environment Server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 3. Run the Demo / Inference Script

In a separate terminal:

```bash
export HF_TOKEN=your_huggingface_token
python inference.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | (required) | Hugging Face token for LLM access |
| `API_BASE_URL` | `https://api.openai.com/v1` | LLM API endpoint |
| `MODEL_NAME` | `gpt-4.1-mini` | Model used for inference |
| `ENV_BASE_URL` | `http://localhost:7860` | Environment server URL |
| `TASK_NAME` | `easy` | Task difficulty: easy, medium, hard |
| `BENCHMARK_NAME` | `soc-analyst-openenv` | Benchmark identifier |

## API Endpoints

- **POST /reset** — Initialize a new incident scenario
- **POST /step** — Execute an action in the environment
- **GET /state** — Inspect the current environment state

## Supported Actions

- **monitor** — Inspect an IP for suspicious behavior
- **block_ip** — Block the malicious IP from the network
- **close_incident** — Close the incident once the response is complete

## Example Workflow

```python
import requests

BASE_URL = "http://localhost:7860"

# Reset environment
requests.post(f"{BASE_URL}/reset", json={"task": "easy"})

# Get current state
state = requests.get(f"{BASE_URL}/state").json()
attack_ip = state["attack_ip"]

# Step through the response workflow
requests.post(f"{BASE_URL}/step", json={"type": "monitor", "target": attack_ip, "details": {}})
requests.post(f"{BASE_URL}/step", json={"type": "block_ip", "target": attack_ip, "details": {}})
requests.post(f"{BASE_URL}/step", json={"type": "close_incident", "details": {}})
```

## How It Works

1. **Reset** — A new SOC incident is generated with a hidden malicious IP
2. **Monitor** — The agent gathers evidence and logs related to the suspicious target
3. **Block IP** — The malicious IP is blocked
4. **Close Incident** — The response workflow is finalized
5. **Reward** — Scores are assigned based on correctness and efficiency

The intended agent flow is:

**monitor → block_ip → close_incident**

## Project Structure

- **env/environment.py** — Core SOC environment logic
- **env/models.py** — Data models for state, alerts, and logs
- **env/grader.py** — Reward and scoring logic
- **server/app.py** — FastAPI server with API endpoints
- **inference.py** — Demo script for agent reasoning

## Local Testing

### Build and run with Docker

```bash
docker build -t soc-analyst-env .
docker run -p 7860:7860 soc-analyst-env
```

Then run the inference script:

```bash
python inference.py
```

## Deployment

Deploy the environment as a Hugging Face Space and ensure it is in the Running state before submission.

## Requirements

- Python 3.10+
- OpenAI/Hugging Face API access
- Docker for reproducible execution

## Submission Checklist

Before submitting, ensure the following are included:

- ☑ Public GitHub repository
- ☑ Environment source code in `env/`
- ☑ `requirements.txt`
- ☑ `README.md`
- ☑ `inference.py` in the project root
- ☑ Deployed Hugging Face Spaces demo URL
- ☑ `Dockerfile`

## Notes

- `easy`, `medium`, and `hard` are supported task modes
- The environment requires completing the full workflow: `monitor` → `block_ip` → `close_incident`
- The submission should be reproducible and runnable locally
- The deployed demo on Hugging Face Spaces should demonstrate the environment end-to-end
- `HF_TOKEN` is required; the script will raise an error if missing

## ✅ Submission Checklist

Before submitting to the hackathon, ensure you have:

- ✓ Public GitHub repository
- ✓ Environment source code (`env/`)
- ✓ `requirements.txt` with all dependencies
- ✓ `README.md` with clear documentation
- ✓ Demo script (`inference.py`)
- ✓ Deployed Hugging Face Spaces demo URL
- ✓ `Dockerfile` for reproducibility
- ✓ `openenv.yaml` for OpenEnv compliance

---
## 📄 License
For hackathon submission and educational use.
---

## 👨‍💻 Authors

- **Pradeep Beleri**
- **Ashish M Josh**
