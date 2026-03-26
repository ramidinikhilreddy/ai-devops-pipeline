# 🚀 AI DevOps Pipeline (Self-Healing LLM System)

## 📌 Overview
This project implements an AI-driven DevOps pipeline that automatically:
- Converts requirements → structured JSON
- Generates backend code (FastAPI)
- Generates test cases
- Runs automated tests (pytest)
- Detects failures
- Fixes code using LLM feedback
- Re-runs tests until success

👉 This creates a self-healing software system

---

## 🧠 Core Idea
Instead of expecting perfect AI-generated code, this system:
❌ allows failure → 🔍 analyzes errors → 🤖 fixes itself → ✅ ensures correctness

---

## ⚙️ Pipeline Flow

Requirement
   ↓
LLM → JSON
   ↓
LLM → Code (FastAPI)
   ↓
Tests (pytest)
   ↓
❌ Failure?
   ↓
LLM Fix (using logs)
   ↓
Re-run tests
   ↓
✅ PASS

---

## 🏗️ Project Structure

ai-devops-pipeline/

llm/ → LLM service + prompts  
pipeline/ → main execution logic  
project/ → generated code + tests  

Dockerfile → container setup  
docker-compose.yaml → run environment  
requirements.txt → dependencies  
.env → API keys  

---

## 🛠️ Tech Stack
- Python 3.11
- FastAPI
- Pytest
- Google Gemini (LLM)
- Docker
- Git / GitHub

---

## 🚀 How to Run

Run Locally:
python -m pipeline.test_runner

Run with Docker:
docker-compose up --build

---

## ⚙️ Configuration

.env file:
GEMINI_API_KEY=your_api_key_here

Toggle LLM usage in test_runner.py:
USE_REAL_LLM = False   # demo mode
USE_REAL_LLM = True    # full AI pipeline

---

## 🔁 Auto-Fix Loop

If tests fail:
1. Capture pytest logs
2. Send logs + code to LLM
3. Generate fixed code
4. Re-run tests
5. Repeat until success

---

## 📊 Example Output

TEST ATTEMPT 1 → FAIL ❌
Trying LLM-based auto-fix...

TEST ATTEMPT 2 → PASS ✅

Pipeline completed successfully ✅

---

## 🔥 Key Features
- Automated code generation
- Automated test generation
- Self-healing fix loop
- Dockerized execution
- Failure-driven improvement

---

## ⚠️ Notes
- LLM usage depends on API quota
- Use USE_REAL_LLM = False for demo
- Docker ensures consistent environment

---

## 🎯 Future Improvements
- Multi-file code generation
- CI/CD integration
- UI dashboard
- RAG integration
- Local LLM support

---

## 🧠 Conclusion
This project demonstrates how AI can be integrated into DevOps pipelines to build self-correcting, automated software systems.

---
