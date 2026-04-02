# 🛡️ SOC Analyst OpenEnv Environment

> A reinforcement learning environment built for the Meta PyTorch OpenEnv Hackathon.

This environment simulates a simple **SOC (Security Operations Center)** incident response workflow where the agent must identify a malicious IP, monitor it, and block it using the OpenEnv-style interface.

---

## ✨ Features

- 🚀 FastAPI-based local server
- 🔄 Reset/step/state endpoints
- 📦 Pydantic models for observations and actions
- 🎯 Simple reward logic
- 📊 Multiple difficulty levels: `easy`, `medium`, `hard`
- 🐳 Docker support
- 📝 Demo script for testing the environment

---

## 📁 Project Structure

```
.
├── Dockerfile
├── openenv.yaml
├── pyproject.toml
├── requirements.txt
├── inference.py
├── server/
│   └── app.py
└── env/
    ├── environment.py
    ├── grader.py
    └── models.py
```

---

## 📋 Requirements

- **Python** 3.10+
- **Docker** (optional, for containerized execution)

---

## 🔧 Installation

This environment is built for the **OpenEnv** framework. Make sure you have the required dependencies installed.

### Local Setup

**1. Create a virtual environment:**

```bash
python -m venv .venv
```

**2. Activate it:**

#### Windows
```bash
.venv\Scripts\activate
```

#### macOS/Linux
```bash
source .venv/bin/activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Server

Start the FastAPI app:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

---

## 🎮 Running the Demo

In a second terminal, run:

```bash
python inference.py
```

This will:
- ✅ Reset the environment
- ✅ Fetch the hidden attack IP
- ✅ Monitor the correct IP
- ✅ Block the correct IP
- ✅ Print the final reward and score

---

## 🔍 How It Works

1. **Reset** — Generates a random SOC incident scenario with a hidden malicious IP
2. **Monitor** — Reveals system logs and network activity related to the target IP
3. **Block IP** — Blocks the threat IP and ends the episode
4. **Reward** — Computed based on action correctness (bonus for efficient solutions)

The agent must learn to identify and neutralize threats within the step limit to maximize the reward.

---

## 🐳 Docker

**Build the container:**

```bash
docker build -t soc-analyst-env .
```

**Run it:**

```bash
docker run -p 7860:7860 soc-analyst-env
```

Then run:

```bash
python inference.py
```

---

## 🔌 API Endpoints

### `POST /reset`

Resets the environment.

**Example request:**

```json
{
  "task": "easy"
}
```

### `POST /step`

Takes an action in the environment.

**Example request:**

```json
{
  "type": "monitor",
  "target": "192.168.1.10"
}
```

**Example response:**

```json
{
  "observation": { },
  "reward": 0.35,
  "done": false,
  "info": {}
}
```

### `GET /state`

Returns current internal state, including the task id, attack IP, history, and step count.

---

## 📚 Example Workflow

```python
import requests

BASE_URL = "http://localhost:7860"

requests.post(f"{BASE_URL}/reset", json={"task": "easy"})
state = requests.get(f"{BASE_URL}/state").json()
attack_ip = state["attack_ip"]

requests.post(f"{BASE_URL}/step", json={"type": "monitor", "target": attack_ip})
requests.post(f"{BASE_URL}/step", json={"type": "block_ip", "target": attack_ip})
```

---

## 📝 Notes

- `easy`, `medium`, and `hard` are supported task modes
- The environment ends when the correct IP is blocked or the max step limit is reached
- The final score is returned in the `info` field after completion

---

## ✅ Submission Checklist

Before submitting to the hackathon, ensure you have:

- ✓ Public GitHub repository
- ✓ Environment source code (`env/`)
- ✓ `requirements.txt` with all dependencies
- ✓ `README.md` with clear documentation
- ✓ Demo script (`inference.py`)
- ✓ Deployed Hugging Face Spaces demo URL (optional but recommended)
- ✓ `Dockerfile` for reproducibility
- ✓ `openenv.yaml` for OpenEnv compliance

---

## 📄 License

For hackathon submission and educational use.

---

## 👨‍💻 Authors

- **Pradeep Beleri**
- **Ashish M Josh**