"""
Health Client - User-facing interface
用户接口，接收消息并返回健康分析
"""

from typing import Dict, Any, Optional
import logging
import asyncio

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.health_coordinator import HealthCoordinator

logger = logging.getLogger(__name__)


class HealthClient:
    """
    健康客户端
    提供简单的接口供用户发送消息并获取健康分析
    """
    
    def __init__(self):
        """初始化客户端"""
        self.coordinator = HealthCoordinator()
        logger.info("✓ Health Client initialized")
    
    async def send_message(
        self,
        message: str,
        user_id: str,
        sports_data: Optional[Dict[str, Any]] = None,
        behavior_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送消息并获取健康分析
        
        Args:
            message: 用户消息
            user_id: 用户ID
            sports_data: 运动数据（可选）
            behavior_data: 行为数据（可选）
            
        Returns:
            健康分析结果
        """
        # 构建上下文
        context = {}
        if sports_data:
            context['sports_data'] = sports_data
        if behavior_data:
            context['behavior_data'] = behavior_data
        
        # 处理消息
        result = await self.coordinator.process_message(
            message=message,
            user_id=user_id,
            context=context if context else None
        )
        
        return result
    
    def send_message_sync(
        self,
        message: str,
        user_id: str,
        sports_data: Optional[Dict[str, Any]] = None,
        behavior_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        同步版本的消息发送
        
        Args:
            message: 用户消息
            user_id: 用户ID
            sports_data: 运动数据（可选）
            behavior_data: 行为数据（可选）
            
        Returns:
            健康分析结果
        """
        return asyncio.run(self.send_message(message, user_id, sports_data, behavior_data))
    
    def get_health_summary(
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
        return self.coordinator.get_user_health_summary(user_id, days)
    
    def format_response(self, result: Dict[str, Any]) -> str:
        """
        格式化响应为可读文本
        
        Args:
            result: 分析结果
            
        Returns:
            格式化的文本响应
        """
        output = []
        
        # 基本信息
        output.append(f"📅 时间: {result.get('timestamp', 'N/A')}")
        output.append(f"👤 用户: {result.get('user_id', 'N/A')}")
        output.append("")
        
        # 综合状态
        if 'synthesis' in result:
            synthesis = result['synthesis']
            status = synthesis.get('overall_health_status', 'unknown')
            status_emoji = {
                'good': '💚',
                'attention_needed': '💛',
                'critical': '🔴'
            }.get(status, '⚪')
            
            output.append(f"{status_emoji} 整体健康状态: {status}")
            output.append("")
            
            # 警告
            if synthesis.get('warnings'):
                output.append("⚠️  警告:")
                for warning in synthesis['warnings']:
                    output.append(f"  • {warning}")
                output.append("")
            
            # 建议
            if synthesis.get('recommendations'):
                output.append("💡 建议:")
                for rec in synthesis['recommendations']:
                    output.append(f"  • {rec}")
                output.append("")
            
            # 洞察
            if synthesis.get('insights'):
                output.append("🔍 洞察:")
                for insight in synthesis['insights']:
                    output.append(f"  • {insight}")
                output.append("")
        
        # Agent分析结果
        if 'agents' in result:
            agents = result['agents']
            
            # 心理健康
            if 'mental_health' in agents:
                mental = agents['mental_health']
                if 'analysis' in mental and 'response' in mental['analysis']:
                    output.append("🧠 心理健康分析:")
                    output.append(f"  {mental['analysis']['response']}")
                    output.append("")
            
            # 身体健康
            if 'physical_health' in agents:
                physical = agents['physical_health']
                if 'injury_risk' in physical:
                    risk = physical['injury_risk']
                    output.append("💪 身体健康分析:")
                    output.append(f"  风险等级: {risk.get('risk_level', 'N/A')}")
                    output.append(f"  风险分数: {risk.get('risk_score', 0.0):.2f}")
                    if risk.get('risk_factors'):
                        output.append(f"  风险因素: {', '.join(risk['risk_factors'])}")
                    output.append("")
        
        return "\n".join(output)

