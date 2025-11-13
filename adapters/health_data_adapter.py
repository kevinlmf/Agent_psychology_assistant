"""
Health Data Adapter - Converts health data between different subsystem formats
健康数据适配器 - 在不同子系统格式之间转换健康数据
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np


class HealthDataAdapter:
    """
    健康数据适配器
    
    负责在不同子系统之间转换数据格式：
    - 感知记忆系统的数据格式
    - 多智能体推理系统的数据格式
    - 心理健康系统的数据格式
    - 运动损伤预测系统的数据格式
    """
    
    @staticmethod
    def convert_to_perception_format(
        health_data: Dict[str, Any],
        data_type: str = "general"
    ) -> Dict[str, Any]:
        """
        将健康数据转换为感知系统格式
        
        Args:
            health_data: 原始健康数据
            data_type: 数据类型 (general, sports, mental, medical)
            
        Returns:
            感知系统格式的数据
        """
        observation = ""
        
        if data_type == "sports":
            observation = f"运动数据: 年龄{health_data.get('age', 'N/A')}, "
            observation += f"位置{health_data.get('position', 'N/A')}, "
            observation += f"训练负荷{health_data.get('training_load', 'N/A')}, "
            observation += f"比赛强度{health_data.get('match_intensity', 'N/A')}"
            
        elif data_type == "mental":
            observation = f"心理健康数据: {health_data.get('query', '')}"
            if 'emotion' in health_data:
                observation += f" 情绪状态: {health_data['emotion']}"
            if 'stress_level' in health_data:
                observation += f" 压力水平: {health_data['stress_level']}"
                
        elif data_type == "medical":
            observation = f"医疗数据: {health_data.get('symptoms', [])}"
            if 'vitals' in health_data:
                observation += f" 生命体征: {health_data['vitals']}"
        
        return {
            'observation': observation,
            'source': f"health_{data_type}",
            'metadata': health_data
        }
    
    @staticmethod
    def convert_to_injury_prediction_format(
        health_data: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        将健康数据转换为运动损伤预测系统格式
        
        Args:
            health_data: 原始健康数据
            
        Returns:
            DataFrame格式的运动数据
        """
        # 提取运动相关字段
        sports_fields = {
            'age': health_data.get('age', 25),
            'position': health_data.get('position', 'MID'),
            'height': health_data.get('height', 175),
            'weight': health_data.get('weight', 70),
            'games_played': health_data.get('games_played', 0),
            'minutes_played': health_data.get('minutes_played', 0),
            'recent_injury': health_data.get('recent_injury', False),
            'training_load': health_data.get('training_load', 0.0),
            'match_intensity': health_data.get('match_intensity', 0.0)
        }
        
        return pd.DataFrame([sports_fields])
    
    @staticmethod
    def convert_to_psychology_format(
        health_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        将健康数据转换为心理健康系统格式
        
        Args:
            health_data: 原始健康数据
            
        Returns:
            心理健康系统格式的数据
        """
        return {
            'query': health_data.get('query', ''),
            'user_id': health_data.get('user_id', 'default_user'),
            'behavior_data': {
                'search_history': health_data.get('search_history', []),
                'app_usage': health_data.get('app_usage', {}),
                'conversation_summary': health_data.get('conversation_summary', [])
            }
        }
    
    @staticmethod
    def convert_to_reasoning_format(
        health_data: Dict[str, Any],
        query: str
    ) -> Dict[str, Any]:
        """
        将健康数据转换为推理系统格式
        
        Args:
            health_data: 原始健康数据
            query: 用户查询
            
        Returns:
            推理系统格式的数据
        """
        context = {
            'question': query,
            'context': {
                'health_data': health_data,
                'user_id': health_data.get('user_id', 'default_user')
            }
        }
        
        return context
    
    @staticmethod
    def synthesize_health_context(
        perception_result: Optional[Dict[str, Any]] = None,
        memory_result: Optional[List[Dict[str, Any]]] = None,
        psychology_result: Optional[Dict[str, Any]] = None,
        injury_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        综合各子系统的结果，生成统一的健康上下文
        
        Args:
            perception_result: 感知系统结果
            memory_result: 记忆系统结果
            psychology_result: 心理健康系统结果
            injury_result: 运动损伤预测结果
            
        Returns:
            综合的健康上下文
        """
        context = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'components': {}
        }
        
        if perception_result:
            context['components']['perception'] = perception_result
        
        if memory_result:
            context['components']['memory'] = {
                'recent_memories': memory_result[:5] if len(memory_result) > 5 else memory_result,
                'total_memories': len(memory_result)
            }
        
        if psychology_result:
            context['components']['psychology'] = {
                'risk_level': psychology_result.get('crisis_risk', 'low'),
                'emotional_state': psychology_result.get('behavior_pattern', {}).get('emotional_state', 'neutral')
            }
        
        if injury_result:
            context['components']['injury'] = {
                'risk_score': injury_result.get('risk_score', 0.0),
                'risk_level': injury_result.get('risk_level', 'low')
            }
        
        # 生成综合健康评分
        context['overall_health_score'] = HealthDataAdapter._calculate_overall_score(context)
        
        return context
    
    @staticmethod
    def _calculate_overall_score(context: Dict[str, Any]) -> float:
        """计算综合健康评分"""
        score = 0.5  # 基础分
        
        # 心理健康影响
        if 'psychology' in context['components']:
            psych = context['components']['psychology']
            risk_level = psych.get('risk_level', 'low')
            if risk_level == 'high':
                score -= 0.3
            elif risk_level == 'medium':
                score -= 0.15
        
        # 运动损伤影响
        if 'injury' in context['components']:
            injury = context['components']['injury']
            risk_score = injury.get('risk_score', 0.0)
            score -= risk_score * 0.2
        
        # 确保分数在0-1之间
        return max(0.0, min(1.0, score))

