"""
Health Specialized Agents
专门处理身心健康问题的Agent
"""

from typing import Dict, Any, Optional, List
import logging
import sys
import os

# 使用本地整合的模块，不再依赖外部子系统
# Psychology模块已整合到 core/psychology/
# Sports模块已整合到 core/sports/
# Economics模块已整合到 core/economics/

logger = logging.getLogger(__name__)


class MentalHealthAgent:
    """
    心理健康Agent
    使用RLHF优化的心理健康助手
    """
    
    def __init__(self):
        """初始化心理健康Agent"""
        try:
            # 使用本地整合的psychology模块
            from .psychology.conversation import ConversationManager
            from .psychology.behavior_analyzer import BehaviorAnalyzer
            from .psychology.crisis_detection import CrisisDetector
            
            self.conversation_manager = ConversationManager
            self.analyzer = BehaviorAnalyzer()
            self.crisis_detector = CrisisDetector()
            self.initialized = True
            logger.info("✓ Mental Health Agent initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Mental Health Agent: {e}")
            import traceback
            traceback.print_exc()
            self.initialized = False
    
    async def analyze(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        分析心理健康问题
        
        Args:
            message: 用户消息
            user_id: 用户ID
            context: 上下文信息
            
        Returns:
            心理健康分析结果
        """
        if not self.initialized:
            return {'error': 'Mental Health Agent not initialized'}
        
        result = {
            'agent_type': 'mental_health',
            'analysis': {},
            'risk_assessment': {},
            'recommendations': []
        }
        
        try:
            # 1. 危机检测
            import asyncio
            import inspect
            
            if inspect.iscoroutinefunction(self.crisis_detector.assess_risk):
                crisis_assessment = await self.crisis_detector.assess_risk(message, user_id)
            else:
                crisis_assessment = self.crisis_detector.assess_risk(message, user_id)
            
            result['risk_assessment'] = {
                'risk_level': crisis_assessment.get('risk_level', 'low'),
                'confidence': crisis_assessment.get('confidence', 0.0),
                'signals': crisis_assessment.get('signals', [])
            }
            
            # 2. 对话分析（使用RLHF优化的对话管理器）
            conversation_manager = self.conversation_manager(user_id=user_id)
            if inspect.iscoroutinefunction(conversation_manager.process_message):
                response = await conversation_manager.process_message(message)
            else:
                response = conversation_manager.process_message(message)
            
            result['analysis']['response'] = response
            result['analysis']['conversation_style'] = 'cbt_based'
            
            # 3. 行为模式分析（如果有上下文）
            if context and 'behavior_data' in context:
                behavior_pattern = await self.analyzer.analyze_recent_activity(
                    user_id=user_id,
                    **context['behavior_data']
                )
                result['analysis']['behavior_pattern'] = {
                    'emotional_state': behavior_pattern.emotional_state,
                    'risk_factors': behavior_pattern.risk_factors,
                    'protective_factors': behavior_pattern.protective_factors
                }
            
            # 4. 生成建议
            if result['risk_assessment']['risk_level'] == 'high':
                result['recommendations'].append('建议立即寻求专业心理健康帮助')
                result['recommendations'].append('可以联系心理健康热线或专业咨询师')
            elif result['risk_assessment']['risk_level'] == 'medium':
                result['recommendations'].append('建议关注心理健康，考虑咨询专业人士')
                result['recommendations'].append('尝试放松技巧和压力管理')
            else:
                result['recommendations'].append('保持良好的心理健康习惯')
                result['recommendations'].append('定期进行自我反思和情绪管理')
            
        except Exception as e:
            logger.error(f"Mental Health Agent error: {e}")
            result['error'] = str(e)
        
        return result


class PhysicalHealthAgent:
    """
    身体健康Agent
    使用整合的Sports模块分析身体问题
    """
    
    def __init__(self):
        """初始化身体健康Agent"""
        try:
            # 使用本地整合的sports模块
            from .sports.injury_predictor import InjuryRiskPredictor
            from .sports.feature_engineer import SportsFeatureEngineer
            
            self.predictor = InjuryRiskPredictor()
            self.feature_engineer = SportsFeatureEngineer()
            self.initialized = True
            logger.info("✓ Physical Health Agent initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Physical Health Agent: {e}")
            import traceback
            traceback.print_exc()
            self.initialized = False
    
    def analyze(
        self,
        message: str,
        user_id: str,
        sports_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        分析身体健康问题
        
        Args:
            message: 用户消息
            user_id: 用户ID
            sports_data: 运动数据（可选）
            
        Returns:
            身体健康分析结果
        """
        if not self.initialized:
            return {'error': 'Physical Health Agent not initialized'}
        
        result = {
            'agent_type': 'physical_health',
            'analysis': {},
            'injury_risk': {},
            'recommendations': []
        }
        
        try:
            # 提取运动相关信息
            if sports_data:
                # 使用整合的预测器
                risk_prediction = self.predictor.predict_risk(sports_data)
                
                result['injury_risk'] = {
                    'risk_score': risk_prediction['risk_score'],
                    'risk_level': risk_prediction['risk_level'],
                    'risk_factors': risk_prediction['risk_factors'],
                    'confidence': risk_prediction['confidence']
                }
                
                # 生成建议
                recommendations = self.predictor.generate_recommendations(
                    risk_prediction['risk_score'],
                    risk_prediction['risk_factors']
                )
                result['recommendations'].extend(recommendations)
            
            # 从消息中提取身体相关关键词
            body_keywords = ['疼', '痛', '不适', '疲劳', '受伤', '膝盖', '脚踝', '肌肉', '关节']
            detected_keywords = [kw for kw in body_keywords if kw in message]
            
            if detected_keywords:
                result['analysis']['detected_symptoms'] = detected_keywords
                result['analysis']['symptom_severity'] = 'moderate' if len(detected_keywords) > 1 else 'mild'
                result['recommendations'].append('如果症状持续，建议咨询医疗专业人士')
            
        except Exception as e:
            logger.error(f"Physical Health Agent error: {e}")
            result['error'] = str(e)
        
        return result


class EconomicsHealthAgent:
    """
    经济健康Agent
    考虑经济因素对健康的影响
    """
    
    def __init__(self):
        """初始化经济健康Agent"""
        try:
            from .economics.economics_agent import EconomicsHealthAgent as EconAgent
            
            self.econ_agent = EconAgent()
            self.initialized = True
            logger.info("✓ Economics Health Agent initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Economics Health Agent: {e}")
            import traceback
            traceback.print_exc()
            self.initialized = False
    
    def analyze(
        self,
        user_income: Optional[float] = None,
        country_code: Optional[str] = None,
        health_concerns: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        分析经济因素对健康的影响
        
        Args:
            user_income: 用户收入（年收入，美元）
            country_code: 国家代码
            health_concerns: 健康关注点
            context: 上下文信息
            
        Returns:
            经济健康分析结果
        """
        if not self.initialized:
            return {'error': 'Economics Health Agent not initialized'}
        
        # 从context中提取信息
        if context:
            user_income = user_income or context.get('user_income')
            country_code = country_code or context.get('country_code')
            health_concerns = health_concerns or context.get('health_concerns')
        
        return self.econ_agent.analyze_economic_health(
            user_income=user_income,
            country_code=country_code,
            health_concerns=health_concerns,
            context=context
        )


class HealthMemoryAgent:
    """
    健康记忆Agent
    使用整合的Psychology Memory系统管理长期健康记忆
    """
    
    def __init__(self):
        """初始化健康记忆Agent"""
        try:
            # 使用整合的psychology memory系统
            from .psychology.memory import get_memory_system
            
            self.memory_system = get_memory_system()
            self.initialized = True
            logger.info("✓ Health Memory Agent initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Health Memory Agent: {e}")
            import traceback
            traceback.print_exc()
            self.initialized = False
    
    def store_experience(
        self,
        user_id: str,
        message: str,
        analysis_result: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        存储健康经验到记忆系统
        
        Args:
            user_id: 用户ID
            message: 用户消息
            analysis_result: 分析结果
            context: 上下文
            
        Returns:
            会话ID（如果成功）
        """
        if not self.initialized:
            return None
        
        try:
            # 使用psychology memory系统存储
            # 获取或创建用户profile
            profile = self.memory_system.get_or_create_profile(user_id)
            
            # 如果有会话，添加到会话中
            # 这里简化处理，实际可以创建新的会话
            sessions = self.memory_system.get_sessions(user_id, recent_n=1)
            if sessions:
                session = sessions[0]
            else:
                from .psychology.memory import Session
                from datetime import datetime
                import uuid
                session = Session(
                    session_id=str(uuid.uuid4()),
                    user_id=user_id,
                    start_time=datetime.now()
                )
            
            # 添加对话轮次
            from .psychology.memory import ConversationTurn
            from datetime import datetime
            
            turn = ConversationTurn(
                timestamp=datetime.now(),
                user_message=message,
                agent_response=str(analysis_result.get('analysis', {}).get('response', '')),
                risk_level=analysis_result.get('risk_assessment', {}).get('risk_level')
            )
            session.turns.append(turn)
            
            # 保存会话
            self.memory_system.save_session(session)
            
            return session.session_id
        except Exception as e:
            logger.error(f"Memory storage error: {e}")
            return None
    
    def retrieve_relevant_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        检索相关记忆
        
        Args:
            user_id: 用户ID
            query: 查询
            top_k: 返回数量
            
        Returns:
            相关记忆列表
        """
        if not self.initialized:
            return []
        
        try:
            # 获取最近的会话
            sessions = self.memory_system.get_sessions(user_id, recent_n=top_k)
            
            # 转换为记忆格式
            memories = []
            for session in sessions:
                for turn in session.turns[-3:]:  # 每个会话取最近3轮
                    if query.lower() in turn.user_message.lower() or query.lower() in turn.agent_response.lower():
                        memories.append({
                            'timestamp': turn.timestamp.isoformat(),
                            'user_message': turn.user_message,
                            'agent_response': turn.agent_response,
                            'risk_level': turn.risk_level
                        })
            
            return memories[:top_k]
        except Exception as e:
            logger.error(f"Memory retrieval error: {e}")
            return []
