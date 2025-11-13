"""
Sports Feature Engineer
运动数据特征工程
整合自Sports_Injury_Risk的特征工程功能
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class SportsFeatureEngineer:
    """
    运动特征工程器
    处理运动数据，提取特征
    """
    
    def __init__(self):
        """初始化特征工程器"""
        self.initialized = True
    
    def transform(self, sports_data: Dict[str, Any]) -> pd.DataFrame:
        """
        转换运动数据为特征向量
        
        Args:
            sports_data: 原始运动数据
            
        Returns:
            特征DataFrame
        """
        features = {}
        
        # 基础特征
        if 'age' in sports_data:
            features['age'] = sports_data['age']
        
        if 'height' in sports_data and 'weight' in sports_data:
            height = sports_data['height'] / 100  # 转换为米
            weight = sports_data['weight']
            features['bmi'] = weight / (height ** 2)
        
        # 位置编码
        if 'position' in sports_data:
            position = sports_data['position']
            position_map = {'GK': 0, 'DEF': 1, 'MID': 2, 'FWD': 3}
            features['position_encoded'] = position_map.get(position, 2)
        
        # 比赛相关特征
        if 'games_played' in sports_data:
            features['games_played'] = sports_data['games_played']
        
        if 'minutes_played' in sports_data:
            features['minutes_played'] = sports_data['minutes_played']
            if 'games_played' in sports_data and sports_data['games_played'] > 0:
                features['avg_minutes_per_game'] = (
                    sports_data['minutes_played'] / sports_data['games_played']
                )
        
        # 训练负荷特征
        if 'training_load' in sports_data:
            features['training_load'] = sports_data['training_load']
        
        if 'match_intensity' in sports_data:
            features['match_intensity'] = sports_data['match_intensity']
        
        # 伤病历史特征
        if 'recent_injury' in sports_data:
            features['recent_injury'] = 1 if sports_data['recent_injury'] else 0
        
        if 'injury_history' in sports_data:
            features['injury_count'] = len(sports_data.get('injury_history', []))
        
        # 负荷比率特征
        if 'training_load' in sports_data and 'match_intensity' in sports_data:
            features['total_load'] = (
                sports_data.get('training_load', 0) + 
                sports_data.get('match_intensity', 0)
            )
        
        # 创建DataFrame
        if features:
            df = pd.DataFrame([features])
            return df
        else:
            # 如果没有特征，返回空DataFrame
            return pd.DataFrame()
    
    def extract_risk_indicators(self, sports_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取风险指标
        
        Args:
            sports_data: 运动数据
            
        Returns:
            风险指标字典
        """
        indicators = {
            'high_load': False,
            'high_intensity': False,
            'fatigue_risk': False,
            'injury_history_risk': False
        }
        
        # 高负荷
        if sports_data.get('training_load', 0) > 0.8:
            indicators['high_load'] = True
        
        # 高强度
        if sports_data.get('match_intensity', 0) > 0.8:
            indicators['high_intensity'] = True
        
        # 疲劳风险（高负荷+高强度）
        if (sports_data.get('training_load', 0) > 0.7 and 
            sports_data.get('match_intensity', 0) > 0.7):
            indicators['fatigue_risk'] = True
        
        # 伤病历史风险
        if sports_data.get('recent_injury', False):
            indicators['injury_history_risk'] = True
        
        return indicators

