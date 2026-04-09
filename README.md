# 🛡️ SOC Analyst OpenEnv

A Reinforcement Learning environment for Security Operations Center (SOC) incident response tasks, built for the Meta PyTorch OpenEnv Hackathon.

This project provides a FastAPI-based OpenEnv-style environment with multiple graded security tasks, designed to be deployed on Hugging Face Spaces and evaluated through automated agentic workflows.

---

## 🌟 Features

- **3 graded SOC tasks**
- **OpenEnv-style environment API**
- **FastAPI server for deployment**
- **Docker-based containerization**
- **Hugging Face Spaces compatible**
- **LLM-friendly inference script**
- **Structured grading logic with bounded rewards**

---

## 📁 Project Structure

```text
project/
├── env/
│   ├── environment.py   # Core SOC environment logic
│   ├── models.py        # Data models for alerts, logs, and state
│   └── grader.py        # Reward and scoring logic
├── openenv/
│   ├── serve.py         # FastAPI app and API endpoints
│   └── __init__.py
├── server/
│   └── app.py           # App re-export
├── inference.py         # Demo script for agent reasoning
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build file
├── README.md           # Project documentation
└── openenv.yaml       # OpenEnv configuration
```

---

## 🎯 Available Tasks

This environment includes three SOC-style tasks:

1. **task_1** — Investigate suspicious login activity
2. **task_2** — Triage suspicious DNS activity
3. **task_3** — Contain lateral movement incident

Each task has its own grader and returns a reward strictly between **0 and 1**.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root health message |
| `GET` | `/health` | Health check |
| `POST` | `/reset` | Reset the environment to a selected task |
| `GET` | `/state` | Get current environment state |
| `POST` | `/step` | Apply an action and receive reward |

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
uvicorn openenv.serve:app --host 0.0.0.0 --port 7860
```

### 4. Open in browser
- [http://localhost:7860/](http://localhost:7860/)
- [http://localhost:7860/health](http://localhost:7860/health)

---

## 💡 Example Usage

### Reset the environment
```bash
curl -X POST "http://localhost:7860/reset" \
  -H "Content-Type: application/json" \
  -d '{"task":"task_1"}'
```

### Step through the environment
```bash
curl -X POST "http://localhost:7860/step" \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "investigate",
    "target": "malicious_ip",
    "flagged": true,
    "quarantine": true,
    "documented": true
  }'
```

---

## 🤖 Inference Script

The repository includes `inference.py` for LLM-based demo inference.

### Environment variables
- `API_BASE_URL` — API endpoint for the model
- `MODEL_NAME` — model name
- `HF_TOKEN` — Hugging Face token

### Example:
```bash
export HF_TOKEN=your_token
python inference.py
```

---

## 🐳 Docker

### Build the container:
```bash
docker build -t soc-openenv .
```

### Run the container:
```bash
docker run -p 7860:7860 soc-openenv
```

---

## 🚀 Deployment

This project is designed to run on **Hugging Face Spaces** using Docker.

Make sure:
- The app starts successfully
- The root route `/` returns a valid response
- `openenv.serve:app` is the entrypoint

---

## ✅ Validation Notes

This submission is designed to satisfy:
- [x] Docker build success
- [x] Hugging Face deployment
- [x] OpenEnv compatibility
- [x] 3+ tasks with graders
- [x] Reward scores strictly between 0 and 1

## ⚖️ License
For hackathon submission and educational use.

---

## 👨‍💻 Authors

- **Pradeep Beleri**
- **Ashish M Josh**
