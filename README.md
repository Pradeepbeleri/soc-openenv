# 🛡️SOC Analyst OpenEnv

Build an AI agent for incident response in a simulated Security Operations Center (SOC) workflow. This OpenEnv environment lets participants create reinforcement-learning agents that detect suspicious activity, monitor network behavior, block malicious IPs, and complete incident response actions in a structured workflow.

## Why this project?

- Realistic SOC-style incident response
- OpenEnv-compatible environment design
- Clear task progression for RL agents
- Built for reproducible local testing and Hugging Face Spaces deployment

This environment simulates a SOC incident response workflow where the agent must infer, investigate, and mitigate a malicious IP using structured observations and actions.

---

## Features

- Quick setup for local development
- FastAPI-based environment server
- OpenEnv-style action workflow
- LLM-guided demo agent
- Reproducible Docker deployment
- Hugging Face Spaces deployment support

## Workflow

The intended agent flow is:

    monitor → block_ip → close_incident

### Step descriptions

- **monitor** — inspect the suspicious IP and gather evidence
- **block_ip** — block the malicious IP from the network
- **close_incident** — finalize the incident response

## Project Structure

```
env/environment.py   # Core SOC environment logic
env/models.py        # Data models for state, alerts, and logs
env/grader.py        # Reward and scoring logic
server/app.py        # FastAPI server with API endpoints
inference.py         # Demo script for agent reasoning
requirements.txt     # Python dependencies
Dockerfile           # Container build file
README.md            # Project documentation
```

## Quick Start

### 1. Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the Environment Server

Start the local SOC environment server:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 3. Run the Demo / Inference Script

In a separate terminal:

```bash
export API_KEY=your_api_key
export API_BASE_URL=https://api.openai.com/v1
export MODEL_NAME=gpt-4.1-mini
export ENV_BASE_URL=http://localhost:7860
export TASK_NAME=easy
export BENCHMARK_NAME=soc-analyst-openenv

python inference.py
```

## Environment Variables

The inference script uses the following environment variables:

| Variable        | Default                        | Description                                    |
|-----------------|-------------------------------|------------------------------------------------|
| API_BASE_URL    | https://api.openai.com/v1      | LLM API endpoint used by the OpenAI client     |
| API_KEY         | required                       | API key injected by the evaluation system      |
| MODEL_NAME      | gpt-4.1-mini                   | Model used for inference                       |
| ENV_BASE_URL    | http://localhost:7860          | SOC environment server URL                     |
| TASK_NAME       | easy                           | Task difficulty: easy, medium, or hard         |
| BENCHMARK_NAME  | soc-analyst-openenv            | Benchmark identifier                           |

#### Example

```bash
export API_KEY=your_api_key
export API_BASE_URL=https://api.openai.com/v1
export MODEL_NAME=gpt-4.1-mini
export ENV_BASE_URL=http://localhost:7860
export TASK_NAME=easy
export BENCHMARK_NAME=soc-analyst-openenv
python inference.py
```

## LLM Integration

This project uses the OpenAI Python client (`openai` package) to make LLM calls through the provided proxy endpoint.

The client is initialized with:

```python
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"],
)
```
To ensure compatibility with evaluation, do not hardcode credentials or bypass the provided proxy.

## API Endpoints

- **POST /reset**  
  Initialize a new incident scenario.

- **POST /step**  
  Execute an action in the environment.

- **GET /state**  
  Inspect the current environment state.

### Supported Actions

- **monitor**  
  Inspect an IP for suspicious behavior.

- **block_ip**  
  Block the malicious IP from the network.

- **close_incident**  
  Close the incident once the response is complete.

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

## Local Testing

Build and run with Docker

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
- OpenAI / Hugging Face API access
- Docker for reproducible execution

## Submission Checklist

Before submitting, ensure you have included:

- Public GitHub repository
- Environment source code in `env/`
- `requirements.txt` with all dependencies
- `README.md` with clear documentation
- `inference.py` in the project root
- Deployed Hugging Face Spaces demo URL
- `Dockerfile` for reproducibility
- `openenv.yaml` for OpenEnv compliance

## Notes

- Supported task modes: `easy`, `medium`, `hard`
- The environment requires completing the full workflow: `monitor → block_ip → close_incident`
- The submission should be reproducible and runnable locally
- The deployed Hugging Face Space should demonstrate the environment end-to-end

---
## 📄 License
For hackathon submission and educational use.
---

## 👨‍💻 Authors

- **Pradeep Beleri**
- **Ashish M Josh**
