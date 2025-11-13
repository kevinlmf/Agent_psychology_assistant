"""
Health Coordinator - Multi-Agent LLM for Health
统一协调器，整合所有健康Agent
"""

from typing import Dict, Any, Optional, List
import logging
import asyncio
from datetime import datetime

from .health_agents import MentalHealthAgent, PhysicalHealthAgent, HealthMemoryAgent, EconomicsHealthAgent

logger = logging.getLogger(__name__)


class HealthCoordinator:
    """
    健康协调器
    统一协调心理健康、身体健康、经济健康和记忆Agent
    """
    
    def __init__(self):
        """初始化协调器"""
        self.mental_agent = MentalHealthAgent()
        self.physical_agent = PhysicalHealthAgent()
        self.economics_agent = EconomicsHealthAgent()
        self.memory_agent = HealthMemoryAgent()
        
        logger.info("✓ Health Coordinator initialized")
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        处理用户消息，整合所有Agent的分析
        
        Args:
            message: 用户消息
            user_id: 用户ID
            context: 上下文信息（可包含sports_data, behavior_data等）
            
        Returns:
            综合健康分析结果
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'message': message,
            'agents': {},
            'synthesis': {}
        }
        
        # 1. 检索相关记忆
        relevant_memories = self.memory_agent.retrieve_relevant_memories(
            user_id=user_id,
            query=message,
            top_k=5
        )
        result['agents']['memory'] = {
            'relevant_memories_count': len(relevant_memories),
            'memories': relevant_memories[:3]  # 只返回前3个
        }
        
        # 2. 并行调用心理健康、身体健康和经济健康Agent
        mental_task = self.mental_agent.analyze(message, user_id, context)
        
        # Physical agent is synchronous, run in thread
        physical_task = asyncio.to_thread(
            self.physical_agent.analyze,
            message,
            user_id,
            context.get('sports_data') if context else None
        )
        
        # Economics agent is synchronous, run in thread
        economics_task = asyncio.to_thread(
            self.economics_agent.analyze,
            context.get('user_income') if context else None,
            context.get('country_code') if context else None,
            context.get('health_concerns') if context else None,
            context
        )
        
        # 等待三个Agent完成
        mental_result, physical_result, economics_result = await asyncio.gather(
            mental_task,
            physical_task,
            economics_task,
            return_exceptions=True
        )
        
        # 处理结果
        if isinstance(mental_result, Exception):
            logger.error(f"Mental agent error: {mental_result}")
            result['agents']['mental_health'] = {'error': str(mental_result)}
        else:
            result['agents']['mental_health'] = mental_result
        
        if isinstance(physical_result, Exception):
            logger.error(f"Physical agent error: {physical_result}")
            result['agents']['physical_health'] = {'error': str(physical_result)}
        else:
            result['agents']['physical_health'] = physical_result
        
        if isinstance(economics_result, Exception):
            logger.error(f"Economics agent error: {economics_result}")
            result['agents']['economics_health'] = {'error': str(economics_result)}
        else:
            result['agents']['economics_health'] = economics_result
        
        # 3. 综合分析和建议
        result['synthesis'] = self._synthesize_results(
            mental_result if not isinstance(mental_result, Exception) else {},
            physical_result if not isinstance(physical_result, Exception) else {},
            economics_result if not isinstance(economics_result, Exception) else {},
            relevant_memories
        )
        
        # 4. 存储经验到记忆
        memory_id = self.memory_agent.store_experience(
            user_id=user_id,
            message=message,
            analysis_result=result,
            context=context
        )
        if memory_id:
            result['memory_id'] = memory_id
        
        return result
    
    def _synthesize_results(
        self,
        mental_result: Dict[str, Any],
        physical_result: Dict[str, Any],
        economics_result: Dict[str, Any],
        memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        综合各Agent的结果，生成最终建议
        
        Args:
            mental_result: 心理健康分析结果
            physical_result: 身体健康分析结果
            economics_result: 经济健康分析结果
            memories: 相关记忆
            
        Returns:
            综合结果
        """
        synthesis = {
            'overall_health_status': 'good',
            'priority': [],
            'recommendations': [],
            'warnings': [],
            'insights': []
        }
        
        # 分析心理健康
        if 'risk_assessment' in mental_result:
            mental_risk = mental_result['risk_assessment'].get('risk_level', 'low')
            if mental_risk == 'high':
                synthesis['overall_health_status'] = 'critical'
                synthesis['warnings'].append('⚠️ 检测到心理健康高风险，建议立即寻求专业帮助')
                synthesis['priority'].append('心理健康')
            elif mental_risk == 'medium':
                if synthesis['overall_health_status'] == 'good':
                    synthesis['overall_health_status'] = 'attention_needed'
                synthesis['recommendations'].extend(mental_result.get('recommendations', []))
        
        # 分析身体健康
        if 'injury_risk' in physical_result:
            physical_risk = physical_result['injury_risk'].get('risk_level', 'low')
            if physical_risk == 'high':
                if synthesis['overall_health_status'] == 'good':
                    synthesis['overall_health_status'] = 'attention_needed'
                synthesis['warnings'].append('⚠️ 运动损伤风险较高')
                synthesis['priority'].append('身体健康')
                synthesis['recommendations'].extend(physical_result.get('recommendations', []))
            elif physical_risk == 'medium':
                synthesis['recommendations'].extend(physical_result.get('recommendations', []))
        
        # 分析经济健康
        if economics_result and 'economic_assessment' in economics_result:
            econ_assessment = economics_result['economic_assessment']
            
            # 检查经济障碍
            if economics_result.get('barriers'):
                barriers = economics_result['barriers']
                if len(barriers) > 0:
                    synthesis['warnings'].append('💰 检测到经济障碍可能影响健康')
                    synthesis['insights'].extend(barriers[:2])  # 添加前2个障碍作为洞察
            
            # 添加经济相关的建议
            if economics_result.get('recommendations'):
                # 标记为经济相关建议
                econ_recs = [f"💰 {rec}" if not rec.startswith('💰') else rec 
                            for rec in economics_result['recommendations']]
                synthesis['recommendations'].extend(econ_recs)
            
            # 医疗可及性洞察
            if 'healthcare_accessibility' in economics_result:
                accessibility = economics_result['healthcare_accessibility']
                if accessibility.get('overall_score', 0.5) < 0.5:
                    synthesis['warnings'].append('⚠️ 医疗可及性较低，可能影响获得医疗服务')
                elif accessibility.get('overall_score', 0.5) > 0.7:
                    synthesis['insights'].append('✅ 医疗可及性良好，可以充分利用医疗资源')
        
        # 基于记忆的洞察
        if memories:
            synthesis['insights'].append(f'基于历史记录，发现{len(memories)}条相关经验')
        
        # 生成综合建议
        if synthesis['overall_health_status'] == 'good':
            synthesis['recommendations'].append('💚 整体健康状况良好，继续保持')
        elif synthesis['overall_health_status'] == 'attention_needed':
            synthesis['recommendations'].append('💛 建议关注身心健康，适当调整生活方式')
        else:
            synthesis['recommendations'].append('🔴 建议尽快咨询专业医疗人员')
        
        return synthesis
    
    def get_user_health_summary(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        获取用户健康摘要
        
        Args:
            user_id: 用户ID
            days: 查询天数
            
        Returns:
            健康摘要
        """
        # 检索最近的相关记忆
        memories = self.memory_agent.retrieve_relevant_memories(
            user_id=user_id,
            query="health summary",
            top_k=20
        )
        
        return {
            'user_id': user_id,
            'period_days': days,
            'total_interactions': len(memories),
            'summary': '基于历史交互的健康摘要'
        }

