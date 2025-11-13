"""
LLM Configuration and Model Management
Supports multiple LLM providers: OpenAI, Anthropic Claude, local model
整合自psychology_agent/models/llm_configs.py
"""

from enum import Enum
from typing import Optional, Dict, Any
import os
from dataclasses import dataclass

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables


class ModelProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class TaskType(Enum):
    """Task types for model routing"""
    CRISIS_DETECTION = "crisis_detection"
    CASUAL_CHAT = "casual_chat"
    BEHAVIOR_ANALYSIS = "behavior_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    INTERVENTION_PLANNING = "intervention_planning"
    COGNITIVE_ASSESSMENT = "cognitive_assessment"


@dataclass
class ModelConfig:
    """Model configuration"""
    provider: ModelProvider
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000
    api_key: Optional[str] = None

    def __post_init__(self):
        # Automatically read API key from environment variables
        if self.api_key is None:
            if self.provider == ModelProvider.OPENAI:
                self.api_key = os.getenv("OPENAI_API_KEY")
            elif self.provider == ModelProvider.ANTHROPIC:
                self.api_key = os.getenv("ANTHROPIC_API_KEY")


class ModelRouter:
    """
    Intelligent model router
    Select optimal model based on task type, complexity, and privacy requirements
    """

    # Task type to model mapping
    TASK_MODEL_MAP = {
        TaskType.CRISIS_DETECTION: ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-opus-20240229",
            temperature=0.3,
            max_tokens=2000
        ),
        TaskType.CASUAL_CHAT: ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=500
        ),
        TaskType.BEHAVIOR_ANALYSIS: ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-sonnet-20240229",
            temperature=0.5,
            max_tokens=1500
        ),
        TaskType.RISK_ASSESSMENT: ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-opus-20240229",
            temperature=0.2,
            max_tokens=2000
        ),
        TaskType.INTERVENTION_PLANNING: ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-sonnet-20240229",
            temperature=0.6,
            max_tokens=1500
        ),
        TaskType.COGNITIVE_ASSESSMENT: ModelConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-4",
            temperature=0.4,
            max_tokens=1000
        ),
    }

    @classmethod
    def get_model_config(cls, task_type: TaskType, use_local: bool = False) -> ModelConfig:
        """Get appropriate Model configuration for task"""
        if use_local:
            return ModelConfig(
                provider=ModelProvider.LOCAL,
                model_name="llama-3-70b",
                temperature=0.7,
                max_tokens=1000
            )
        return cls.TASK_MODEL_MAP.get(task_type, cls.TASK_MODEL_MAP[TaskType.CASUAL_CHAT])


class SystemPrompts:
    """System prompt template library"""

    THERAPIST_BASE = """You are a professional mental health assistant, using Cognitive Behavioral Therapy (CBT) principles.

Core principles:
1. Empathetic listening, build trust
2. Identify cognitive distortions and automatic thoughts
3. Guide rather than lecture
4. Focus on present feelings and thoughts
5. Provide concrete and actionable coping strategies

Safety boundaries:
- You cannot replace professional therapists
- Must transfer to human experts in crisis situations
- Do not make medical diagnoses
- Respect user privacy

Tone: Warm, professional, non-judgmental"""

    CRISIS_DETECTOR = """You are a crisis detection expert. Analyze user messages and identify risk signals.

Output JSON format with risk_level, signals, immediate_action, confidence."""

    BEHAVIOR_ANALYST = """You are a user behavior pattern analysis expert. Analyze multimodal data and identify mental health indicators.

Output structured JSON analysis with evidence and confidence."""

    INTERVENTION_PLANNER = """You are a personalized intervention design expert. Design effective intervention strategies based on user profile and current state."""

