"""
Conversation Manager
Handles Conversation Flow control, State management, Context maintenance
整合自psychology_agent/agent/conversation_manager.py
"""

from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from .models import (
    get_orchestrator,
    ModelRouter,
    TaskType,
    SystemPrompts,
)
from .memory import (
    get_memory_system,
    Session,
    ConversationTurn,
)


class ConversationState:
    """Conversation state"""

    def __init__(self):
        self.current_topic: Optional[str] = None
        self.detected_emotions: list = []
        self.risk_flags: list = []
        self.intervention_mode: Optional[str] = None  # 'crisis', 'assessment', 'therapy', 'casual'


class ConversationManager:
    """
    Conversation Manager
    Handles overall Conversation Flow orchestration
    """

    def __init__(self, user_id: str, session_id: Optional[str] = None):
        self.user_id = user_id
        self.session_id = session_id or str(uuid.uuid4())
        self.state = ConversationState()

        # Initialize dependencies
        self.llm = get_orchestrator()
        self.memory = get_memory_system()

        # Create or load conversation
        self.session = Session(
            session_id=self.session_id,
            user_id=user_id,
            start_time=datetime.now(),
        )

        # Load User profile
        self.user_profile = self.memory.get_or_create_profile(user_id)

    async def process_message(self, user_message: str) -> str:
        """
        Handle user message main process

        Args:
            user_message: user input

        Returns:
            agent response
        """
        # 1. Quick Crisis Detection (highest priority)
        risk_assessment = await self._quick_risk_check(user_message)

        if risk_assessment['risk_level'] == 'high':
            # Crisis mode: use strongest model, immediate response
            response = await self._handle_crisis(user_message, risk_assessment)
            self.state.intervention_mode = 'crisis'
        else:
            # 2. Normal Conversation Flow
            response = await self._generate_therapeutic_response(user_message)

        # 3. Record conversation
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_message=user_message,
            agent_response=response,
            risk_level=risk_assessment.get('risk_level'),
        )
        self.session.turns.append(turn)

        # 4. Save session (periodically)
        if len(self.session.turns) % 5 == 0:  # Save every 5 turns
            self.memory.save_session(self.session)

        return response

    async def _quick_risk_check(self, message: str) -> Dict[str, Any]:
        """
        Quick Risk detection using Keywords + LLM dual detection
        """
        # First layer: Keyword Rapid screening
        high_risk_keywords = [
            'suicide', '死', 'end生命', 'not想活', '轻生', '伤害自己',
            'self-harm', '割腕', '跳楼',
        ]

        has_risk_keyword = any(kw in message for kw in high_risk_keywords)

        if has_risk_keyword:
            # Second layer: LLM precise determination
            from .crisis_detection import CrisisDetector
            detector = CrisisDetector()
            return await detector.assess_risk(message, self.user_id)

        # No obvious Risk
        return {'risk_level': 'low', 'signals': []}

    async def _handle_crisis(self, message: str, risk_info: Dict[str, Any]) -> str:
        """
        Crisis handling pattern
        """
        config = ModelRouter.get_model_config(TaskType.CRISIS_DETECTION)

        crisis_prompt = f"""
User message: {message}

Detected Risk signals: {risk_info['signals']}

Please immediately provide:
1. Empathy and support
2. Confirm user safety
3. Guidance to seek professional help (suicide hotline, emergency)
4. Do not ignore or minimize user feelings

Tone: Warm, firm, Non-judgmental
"""

        response = await self.llm.generate(
            prompt=crisis_prompt,
            config=config,
            system_prompt=SystemPrompts.THERAPIST_BASE,
        )

        # Add resource info
        response += "\n\n---\nEmergency resources:\n"
        response += "🆘 24-hour psychological crisis hotline: 400-161-9995\n"
        response += "🏥 If there is immediate danger, please call 120 or go to nearest emergency room"

        return response

    async def _generate_therapeutic_response(self, user_message: str) -> str:
        """
        Generate therapeutic Response combining User profile, historical context
        """
        config = ModelRouter.get_model_config(TaskType.CASUAL_CHAT)

        # Build context
        user_summary = self.memory.get_user_summary(self.user_id)
        recent_context = self.memory.get_recent_context(self.user_id, days=7)

        # Get recent conversation turns
        recent_turns = self.session.turns[-3:]  # Last 3 turns
        conversation_history = "\n".join([
            f"User: {turn.user_message}\nAssistant: {turn.agent_response}"
            for turn in recent_turns
        ])

        prompt = f"""
User profile:
{user_summary}

Recent Conversation history:
{recent_context}

Current conversation context:
{conversation_history}

User current message: {user_message}

Please respond based on CBT principles:
1. First show empathy, confirm user feelings
2. If cognitive distortions are identified, gently guide awareness
3. Ask open-ended questions, guide deeper exploration
4. When appropriate, provide specific coping strategies

Note: Natural conversation, not too textbook-like
"""

        response = await self.llm.generate(
            prompt=prompt,
            config=config,
            system_prompt=SystemPrompts.THERAPIST_BASE,
        )

        return response

    async def end_session(self, user_satisfaction: Optional[int] = None) -> str:
        """
        End conversation, generate Summary
        """
        self.session.end_time = datetime.now()
        self.session.user_satisfaction = user_satisfaction

        # Generate conversation Summary
        summary = await self._generate_session_summary()
        self.session.summary = summary

        # Save session
        self.memory.save_session(self.session)

        # Update User profile
        self.memory.update_profile_from_session(self.user_id, self.session)

        return summary

    async def _generate_session_summary(self) -> str:
        """Use LLM to generate conversation Summary"""
        if not self.session.turns:
            return "No Conversation content"

        # Extract all conversations
        all_messages = "\n\n".join([
            f"User: {turn.user_message}\nAssistant: {turn.agent_response}"
            for turn in self.session.turns
        ])

        config = ModelRouter.get_model_config(TaskType.BEHAVIOR_ANALYSIS)

        prompt = f"""
Please summarize the following psychological counseling conversation:

{all_messages}

Please provide:
1. Main discussion Topics (tag form)
2. User Emotional state
3. Identified Cognitive patterns or distress
4. Intervention strategies used
5. User response and progress

Format: concise JSON
"""

        result = await self.llm.generate_structured(
            prompt=prompt,
            config=config,
        )

        # Extract Topics
        if 'themes' in result or 'topics' in result:
            themes = result.get('themes') or result.get('topics', [])
            self.session.identified_themes = themes if isinstance(themes, list) else [themes]

        return str(result)

    def get_conversation_history(self, last_n: int = 5) -> str:
        """Get recent N turns conversation (used for display)"""
        recent = self.session.turns[-last_n:]
        return "\n\n".join([
            f"**User**: {turn.user_message}\n**Assistant**: {turn.agent_response}"
            for turn in recent
        ])

