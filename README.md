# 🛡️ SOC Analyst OpenEnv

An automated evaluation environment for benchmarking LLM-based Reinforcement Learning (RL) agents in a simulated Security Operations Center (SOC) workflow.

[![OpenEnv Compatible](https://img.shields.io/badge/OpenEnv-Compatible-green)](https://github.com/openenv)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Educational](https://img.shields.io/badge/License-Educational-lightgrey.svg)](LICENSE)

## 📋 Overview

This project provides a high-fidelity environment where AI agents act as SOC Analysts. The agent must detect, investigate, and mitigate malicious activity using a structured incident response workflow. It is built specifically for **OpenEnv compliance**, supporting reproducible local testing and **Hugging Face Spaces** deployment.

### Why this project?
* **Realistic SOC Triage:** Simulates evidence gathering and threat mitigation.
* **Deterministic Grading:** Advanced reward logic for precise performance tracking.
* **Production Ready:** Fully containerized with Docker for seamless evaluation.
* **Scalable Difficulty:** Supports `easy`, `medium`, and `hard` task modes.

---

## 🏗️ Project Structure

```text
.
├── env/
│   ├── environment.py   # Core SOC logic (States & Transitions)
│   ├── models.py        # Pydantic data models for logs & alerts
│   └── grader.py        # Reward shaping and scoring logic
├── server/
│   └── app.py           # FastAPI server & API endpoints
├── inference.py         # Demo script for agent reasoning (Baseline)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization for reproducibility
├── openenv.yaml         # OpenEnv configuration file
└── README.md            # Project documentation

🚀 Quick Start1.
Local SetupCreate and activate a virtual environment, then install dependencies:
PowerShell# Create environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Start the Environment ServerRun the FastAPI backend using Uvicorn:
PowerShell
uvicorn server.app:app --host 0.0.0.0 --port 7860
3. Run Inference (The Agent)In a separate terminal, set your environment variables and run the agent:PowerShell# Set Environment Variables
$env:API_KEY="your_api_key"
$env:API_BASE_URL="[https://api.openai.com/v1](https://api.openai.com/v1)"
$env:MODEL_NAME="gpt-4o-mini"
$env:ENV_BASE_URL="http://localhost:7860"
$env:TASK_NAME="easy"

# Run Agent
python inference.py
🕹️ Workflow & ActionsThe environment follows a strictly ordered incident response lifecycle:
monitor: Inspect suspicious IPs to gather log evidence.
block_ip: Mitigate the threat by blocking the confirmed malicious IP.
close_incident: Finalize the ticket and calculate the final reward.

Supported API Endpoints
Endpoint,Method,Description
/reset,POST,Resets the incident and sets task difficulty.
/step,POST,"Executes an action (monitor, block_ip, etc.)."
/state,GET,Returns current observation and metadata.

🐳 Docker DeploymentTo ensure a clean and reproducible build for Round 2 evaluation:
Bash# Build the image
docker build -t soc-analyst-env .

# Run the container
docker run -p 7860:7860 soc-analyst-env

🎯 Grading & EvaluationThe environment uses a dense reward signal to guide agent
learning:Positive Rewards: Awarded for monitoring the correct IP and successful mitigation.
Negative Penalties: Applied for "False Positive" blocks on innocent IPs and an incremental "Step Penalty" to reward speed and efficiency.

📝 LicenseThis project is released under an educational license for hackathon participation and research.

## 👨‍💻 Authors

- **Pradeep Beleri**
- **Ashish M Josh**
