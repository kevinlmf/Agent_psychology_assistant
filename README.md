# Health_Agent_System

**Unified Multi-Agent Health AI System — Four-Dimensional Health Analysis**

Health_Agent_System is an integrated AI health agent powered by multi-agent LLM processing, multi-modal models, and long-term memory.  
It performs **four-dimensional health analysis** across:

1. **Mental Health** — LLM-based cognitive and emotional reasoning  
2. **Physical Health** — Multi-modal injury and symptom understanding  
3. **Economic Health** — Practicality-aware recommendations  
4. **Long-Term Memory** — Health experience storage and retrieval  

The system is fully modular, runs locally, and requires **no REST API server**.

---

## System Overview

The system processes:

- LLM text  
- Images  
- Sensor data  
- Tabular data  

Agents collaboratively produce a unified health assessment:

- **Mental Health Agent (LLM)** — emotional and cognitive reasoning  
- **Physical Health Agent (Multi-modal)** — sports, injuries, body metrics  
- **Economics Health Agent** — affordability and practicality  
- **Health Coordinator** — unified reasoning router  
- **Memory System** — user profile, session history, health logs  

---

 
## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/kevinlmf/Health_Agent_System
cd Health_Agent_System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add API Keys
```bash
cp env.example .env
# Edit .env and add:
# ANTHROPIC_API_KEY=your-key
# OPENAI_API_KEY=your-key (optional)
```

Or via environment variables:
```bash
export ANTHROPIC_API_KEY=your-key
export OPENAI_API_KEY=your-key
```

---

### 4. Run the System (CLI)
```bash
python cli.py
```

### Example Usage
```bash
python cli.py -m "I've been stressed lately"

python cli.py -m "My knee hurts when running" --age 28 --training-load 0.8

python cli.py -m "Therapy costs too much for me" --income 4000 --country CN
```

---

## System Architecture

### Input → Processing → Storage → Output

```
Input (Input)
    |
    ├─ LLM Text Input
    |     └─ User language input (mental health, emotions, symptom descriptions)
    |
    └─ Multi-modal Input
          ├─ Images (body photos, X-rays, etc.)
          ├─ Sensor data (heart rate, steps, sleep, etc.)
          └─ Tabular data (sports data, health metrics, etc.)
                 |
                 ↓
Processing (Processing)
    |
    ├─ Mental Health Agent (LLM)
    ├─ Physical Health Agent (Multi-modal)
    ├─ Economics Health Agent
    └─ Health Coordinator (Unified Coordination)
                 |
                 ↓
Storage (Memory)
    |
    └─ Memory System
          ├─ User Profile
          ├─ Session History
          └─ Health Experiences
                 |
                 ↓
Output (Output)
    |
    └─ Comprehensive Health Analysis Results
          ├─ Multi-dimensional analysis (mental, physical, economic)
          ├─ Overall health status
          ├─ Personalized recommendations
          ├─ Risk warnings
          └─ Health insights
```

---

## Directory Structure

```
Health/
├── core/
│   ├── psychology/
│   ├── sports/
│   ├── economics/
│   ├── health_agents.py
│   └── health_coordinator.py
│
├── cli.py
├── main.py
├── examples/
└── README.md
```

---

## Current Status

- Fully functional CLI interaction  
- Supports multi-agent reasoning  
- Python import usage available  
- No REST API required  

---

## Future Work

- Multi-modal image model integration (CLIP, ViT)  
- Full RLHF training pipeline  
- Expanded global health datasets  
- Web UI and dashboard  
- Health trend prediction models  
- Personalized long-term planning  

---

##  Disclaimer

This system is for **research and educational purposes only**.  
It is **not** a medical device and must not be used for diagnosis or treatment.  
Consult professionals for real medical issues.

---
I hope everyone can stay happy and free from anxiety, anger, or any other negative emotions — and keep healthy every single day ✨ .
