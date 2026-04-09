# 🛡️ SOC Analyst OpenEnv

A Reinforcement Learning environment for simulating genuine Security Operations Center (SOC) incident response tasks, built for the Meta PyTorch OpenEnv Hackathon.

## 🌟 Motivation & Description
Traditional RL environments often rely heavily on games or artificial benchmarks. **SOC Analyst OpenEnv** directly mirrors real-world cybersecurity triage. Real-world agents must filter through noisy authentication logs, investigate potential lateral movements, and successfully decide when to contain systems versus categorizing alerts as false positives. This open environment tests frontier models on multi-step reasoning, documentation consistency, and safe incident closure.

## 🧩 Spaces

### Observation Space
The environment represents the system state as a typed `EnvironmentState` schema encompassing:
- **`alerts`**: Real-time security events detailing `id`, `severity`, `type`, `description`, and `source_ip`.
- **`logs`**: Historical context encompassing `timestamp`, `source_ip`, `destination_ip`, `action`, and `protocol`.
- **`history`**: The iterative action trace of the investigation.
- **`step_count` & `max_steps`**: Pacing constraints for agent execution loops.

### Action Space
Agents must execute JSON payloads interacting with the following deterministic features:
- `action_type` *(str)*: `investigate`, `triage`, or `contain`.
- `target` *(str)*: Specific entity, e.g., an IP address.
- `alert_severity` *(str)*: `low`, `medium`, `high`.
- Boolean Flags: `flagged`, `quarantine`, `false_positive`, `documented`, `evidence_collected`, `incident_closed`.

## 🎯 Tasks & Difficulty Progression

This environment challenges the agent over three structured difficulties. Graders use deterministically weighted properties yielding a reward strictly clamped between **(0.01 - 1.0)** per step. 

| Task | Title | Difficulty | Expected Goal |
| :--- | :--- | :--- | :--- |
| **`task_1`** | **Investigate Suspicious Logins** | **Easy** | Identify brute force attacks. The agent should properly `investigate` the target IP, mark it `flagged`, `quarantine` the host, and ensure it is `documented`. |
| **`task_2`** | **Triage Suspicious DNS Network** | **Medium** | Differentiate benign development noise from malicious activity. The agent must `triage`, identify `false_positive`, document properly, and assess `alert_severity`. |
| **`task_3`** | **Contain Lateral Movement** | **Hard** | Manage high-risk escalation. Requires the agent to properly choose `contain`, ensure `evidence_collected`, and most importantly guarantee the `incident_closed` flag securely ends the episode. |

## 📊 Baseline Scores

A baseline model (using generic inference Fallbacks and standard reasoning patterns) reproduces the following optimal reward limits executing through all tasks sequentially:
- **`task_1` (Optimal Baseline)**: Target Reward: **1.0** (Per step, capped at max episode limits)
- **`task_2` (Optimal Baseline)**: Target Reward: **1.0** (Perfectly isolates the false positive schema)
- **`task_3` (Optimal Baseline)**: Target Reward: **0.95 - 1.0** (Resolves within a single closure step)

## 🚀 Setup & Execution

### 1. Local Run
Install the environment securely on your local desktop.
```bash
# Install specific OpenEnv dependencies
pip install -r requirements.txt

# Start the FastApi endpoint
uvicorn openenv.serve:app --host 0.0.0.0 --port 7860
```

### 2. Connect the Inference Baseline
The repository uses standard OpenAI format wrappers compatible with major LLMs.
```bash
# Map Model Variables
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-api-key"

# Run Agent
python inference.py
```

### 3. Containerized Runtime (Docker / HF Spaces)
The submission complies fully with containerization standard deployments:
```bash
docker build -t soc-openenv .
docker run -p 7860:7860 soc-openenv
```

## ✅ OpenEnv Validator Specs
This project is certified against `openenv validate` checking for:
- [x] Hugging Face Space endpoints returning valid `GET 200`
- [x] Robust Dockerfile integration parsing
- [x] 3 multi-stage tasks deploying between explicit 0.0-1.0 rewards 
- [x] Pydantic modeled data parameters across API definitions
- [x] Structured Baseline Inference executing via `[START]`, `[STEP]`, and `[END]` JSON log streams.
