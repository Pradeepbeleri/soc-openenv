# 🛡️ SOC Analyst OpenEnv

Build an AI agent for incident response in a simulated Security Operations Center (SOC) workflow. This OpenEnv environment lets participants create reinforcement-learning agents that detect suspicious activity, monitor network behavior, block malicious IPs, and complete incident response actions in a structured workflow.

---

## 🌟 Features

- ⚡ **Quick Setup** — Get running locally in seconds.
- 🚀 **FastAPI-powered** — High-performance environment server.
- 🔄 **Structured Workflow** — Real SOC incident response: Monitor → Block → Close.
- 🤖 **LLM-Guided** — Built-in demo agent logic.
- 🐳 **Dockerized** — Fully reproducible deployments.
- 🤗 **HF Spaces Support** — Deploy and demo on Hugging Face easily.

---

## 🛠️ Workflow

The environment simulates a SOC incident where the agent must investigate and mitigate threats using a structured sequence:

1. **Monitor** — Inspect the suspicious IP and gather evidence such as logs and activity.
2. **Block IP** — Neutralize the threat by blocking the malicious IP.
3. **Close Incident** — Finalize the response and submit the remediation report.

---

## 📁 Project Structure

```text
env/environment.py   # Core SOC environment logic
env/models.py        # Data models for state, alerts, and logs
env/grader.py        # Reward and scoring logic
server/app.py        # FastAPI server with API endpoints
inference.py         # Demo script for agent reasoning (LLM-driven)
requirements.txt     # Python dependencies
Dockerfile           # Container build file
README.md            # Project documentation
openenv.yaml
```

---

## 🚀 Quick Start

### 1. Setup
Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the Environment Server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 3. Run the Demo / Inference Script
In a separate terminal, set your environment variables and run the agent:

```bash
# Set environment variables (PowerShell)
$env:HF_TOKEN="your_api_key"
$env:API_BASE_URL="https://api.openai.com/v1"
$env:MODEL_NAME="gpt-4o-mini"
$env:ENV_BASE_URL="http://localhost:7860"
$env:TASK_NAME="easy"
$env:BENCHMARK_NAME="soc-analyst-openenv"

python inference.py
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /reset | POST | Initialize a new incident scenario. |
| /step | POST | Execute an action (monitor, block_ip, close_incident). |
| /state | GET | Inspect the current environment state. |

---

## 💡 LLM Integration

This project uses the OpenAI Python client to bridge LLMs with the SOC environment. The agent determines actions based on the observations returned from the server.

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"],
)
```

---

## 🐳 Deployment

Build and run with Docker:

```bash
docker build -t soc-analyst-env .
docker run -p 7860:7860 soc-analyst-env
```

---

## ✅ Submission Checklist

- [x] Public GitHub repository
- [x] Environment source code in `env/`
- [x] `requirements.txt` with all dependencies
- [x] `README.md` with clear documentation
- [x] `inference.py` in the project root
- [x] Deployed Hugging Face Spaces demo URL
- [x] `Dockerfile` for reproducibility
- [x] `openenv.yaml` for OpenEnv compliance

---

## ⚖️ License
For hackathon submission and educational use.

---

## 👨‍💻 Authors

- **Pradeep Beleri**
- **Ashish M Josh**
