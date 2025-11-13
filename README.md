# Multi-Agent LLM for Health

Unified Multi-Agent Health AI System - Four-Dimensional Health Analysis

## System Overview

Multi-Agent LLM for Health is a **four-dimensional health AI system** that considers:
1. **Mental Health** - RLHF-optimized mental health support
2. **Physical Health** - Sports injury risk prediction
3. **Economic Health** - Economic factors affecting health
4. **Long-term Memory** - Health experience tracking

### Core Design Philosophy

- **LLM processes user speech** - Uses LLM to understand user language input, extract mental health and emotional information
- **Multi-modal models capture physical problems** - Uses multi-modal models (vision + text + sensors) to analyze physical issues
- **Economic factors consideration** - Considers income and country health profiles to provide practical health advice
- **Fully integrated** - All code is within the Health system, runs independently
- **Direct usage** - Works via CLI and Python code, no REST API service needed (REST API is future work)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kevinlmf/Multi-Agent-LLM-for-Health.git
cd Multi-Agent-LLM-for-Health/Health
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

**Required**: The system uses LLM APIs for text processing. API keys are **required** for the system to work.

**Option 1: Use .env file (Recommended)**
```bash
cp env.example .env
# Edit .env and add your API keys
```

**Option 2: Use system environment variables**
```bash
export ANTHROPIC_API_KEY=your-anthropic-key-here
export OPENAI_API_KEY=your-openai-key-here  # optional
```
Get API keys from:
- Anthropic: https://console.anthropic.com/settings/keys (recommended, system default)
- OpenAI: https://platform.openai.com/api-keys (optional)

### 4. Run the System

#### Method 1: Interactive Mode (Recommended)
```bash
python cli.py
```

Then follow the prompts to enter your health questions.

#### Method 2: Command Line Arguments
```bash
# Basic query
python cli.py -m "I've been feeling stressed lately"

# With economic information
python cli.py -m "I want to see a psychologist but worried about cost" --income 5000 --country CN

# With sports data
python cli.py -m "My knee hurts when exercising" --age 28 --training-load 0.8
```

```

## System Architecture

### Input → Processing → Storage → Output Flow

```
Input (Input)
    │
    ├─ LLM Text Input
    │   └─ User language input (mental health, emotions, symptom descriptions)
    │
    └─ Multi-modal Input
        ├─ Images (body photos, X-rays, etc.)
        ├─ Sensor data (heart rate, steps, sleep, etc.)
        └─ Tabular data (sports data, health metrics, etc.)
            │
            ↓
Processing (Processing)
    │
    ├─ Mental Health Agent (LLM)
    ├─ Physical Health Agent (Multi-modal)
    ├─ Economics Health Agent
    └─ Health Coordinator (Unified Coordination)
            │
            ↓
Storage (Memory)
    │
    └─ Memory System
        ├─ User Profile
        ├─ Session History
        └─ Health Experiences
            │
            ↓
Output (Output)
    │
    └─ Comprehensive Health Analysis Results
        ├─ Multi-dimensional analysis (mental, physical, economic)
        ├─ Overall health status
        ├─ Personalized recommendations
        ├─ Risk warnings
        └─ Health insights
```

### Directory Structure

```
Health/
├── core/
│   ├── psychology/          # Psychology module (LLM processing)
│   ├── sports/              # Sports module (Multi-modal processing)
│   ├── economics/           # Economics module
│   ├── health_agents.py    # Agent definitions
│   └── health_coordinator.py # Coordinator
│
├── cli.py                   # Command-line interface
├── main.py                  # Demo program
├── examples/                # Example code
└── README.md                # This document
```



**Purpose**: Provide personalized recommendations based on historical records, track long-term health changes



## Current Status

The system currently works via:
- **CLI Interface** (`cli.py`) - Direct terminal usage
- **Python Code** - Direct import and use in Python scripts

**No REST API service is needed or provided.** The system is designed to be used directly without HTTP endpoints.



## Future Work


1. **Complete Multi-modal Model Integration**
   - [ ] Full integration of vision models (CLIP, ViT) for image analysis
   - [ ] Sensor data processing pipeline integration
   - [ ] Multi-modal data fusion algorithm implementation

2. **Complete RLHF Implementation**
   - [ ] Complete RLHF training pipeline
   - [ ] User feedback collection mechanism
   - [ ] Personalized conversation strategy optimization

3. **Expand Country Health Profile Data**
   - [ ] Add more countries (Europe, Africa, Asia, etc.)
   - [ ] Real-time health data API integration


4. **Web Interface**
   - [ ] User-friendly web interface
   - [ ] Health data visualization
   - [ ] Mobile adaptation

5. **Advanced Analysis Features**
   - [ ] Health trend prediction
   - [ ] Disease risk assessment models
   - [ ] Personalized health plan generation

---


## Disclaimer

This system is for research and educational purposes only. It should not be used for actual medical diagnosis or treatment. If you have health problems, please consult professional medical personnel. 

---
 I hope everyone can stay happy and free from anxiety, anger, or any other negative emotions — and keep healthy every single day ✨ .