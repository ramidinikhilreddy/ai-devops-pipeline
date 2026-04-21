# 🚀 AI DevOps Pipeline (Self-Healing Multi-Agent System)

## 📌 Overview

This project implements an **AI-powered DevOps pipeline** that can:

* Read real **Jira tickets**
* Generate backend code (FastAPI)
* Run automated tests (pytest)
* Detect failures
* Fix code using **LLM agents**
* Re-run tests until success

👉 Result: A **self-healing system** that converts requirements → working code automatically.

---

## 🧠 Core Idea

Instead of expecting perfect code from AI:

❌ Failure is allowed
🔍 Errors are analyzed
🤖 Code is fixed automatically
✅ Tests ensure correctness

---

## ⚙️ Full System Flow

```
Jira Ticket
     ↓
Fetch Requirement
     ↓
Run Tests (Fail)
     ↓
Analyzer Agent (LLM)
     ↓
Fix Plan
     ↓
Fixer Agent (LLM)
     ↓
Rewrite Full Code
     ↓
Run Tests Again
     ↓
✅ PASS
```

---

## 🤖 Multi-Agent Architecture

The system uses two AI agents:

### 🧠 Analyzer Agent

* Reads:

  * Code
  * Test failures
  * Jira ticket
* Outputs:

  * Issues
  * Fix plan

---

### 🔧 Fixer Agent

* Uses:

  * Code + Fix Plan
* Generates:

  * Complete corrected FastAPI file

---

## 🏗️ Project Structure

```
ai-devops-pipeline/

llm/            → LLM service, agents, prompts  
pipeline/       → main pipeline logic  
project/        → generated FastAPI app + tests  
scripts/        → reset demo script  
jira/           → Jira ticket fetch logic  

.github/        → GitHub Actions (CI)

Dockerfile
docker-compose.yaml
requirements.txt
.env (not committed)
```

---

## 🛠️ Tech Stack

* Python 3.11
* FastAPI
* Pytest
* Google Gemini (LLM)
* Jira API
* Docker
* GitHub Actions (CI/CD)

---

## ⚙️ Configuration

Create a `.env` file:

```
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
USE_REAL_LLM=true

JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_token
JIRA_TICKET_KEY=KAN-1
```

---

## 🚀 How to Run

### 🔹 Step 1 — Activate environment

```
source .venv/bin/activate
```

---

### 🔹 Step 2 — Reset demo (broken code)

```
python scripts/reset_demo.py
```

---

### 🔹 Step 3 — Run pipeline

```
python -m pipeline.pipeline
```

---

## 🔁 Example Output

```
📄 JIRA TICKET FETCHED

Attempt 1 → FAIL ❌

Analyzer Agent → identifies issues  
Fixer Agent → rewrites code  

Attempt 2 → PASS ✅
```

---

## 🔄 GitHub Actions (CI)

On every push:

* installs dependencies
* runs tests
* verifies correctness

👉 Ensures code is always stable

---

## 🔥 Key Features

* Real Jira ticket integration
* Multi-agent LLM architecture
* Full-file code generation
* Self-healing fix loop
* Automated testing (pytest)
* CI/CD with GitHub Actions

---

## ⚠️ Important Notes

* `.env` is NOT committed (security)
* LLM usage depends on API quota
* Use `USE_REAL_LLM=false` for development mode

---

## 🎯 Future Improvements

* UI Dashboard (in progress)
* Multi-file code generation
* Auto PR creation
* RAG-based context retrieval
* Local LLM support

---

## 🧠 Conclusion

This project demonstrates how AI can be integrated into DevOps pipelines to build:

> Self-healing, automated, intelligent software systems.

---
