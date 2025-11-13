"""
Sports Injury Risk Predictor
整合自Sports_Injury_Risk的核心预测功能
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class InjuryRiskPredictor:
    """
    运动损伤风险预测器
    整合了Sports_Injury_Risk的核心预测逻辑
    """
    
    def __init__(self):
        """初始化预测器"""
        self.initialized = False
        self.model = None
        
        # 尝试加载XGBoost模型（如果可用）
        try:
            from .xgboost_predictor import XGBoostPredictor
            self.xgboost_predictor = XGBoostPredictor
            self.initialized = True
            logger.info("✓ Injury Risk Predictor initialized")
        except Exception as e:
            logger.warning(f"XGBoost predictor not available, using rule-based: {e}")
            self.initialized = False
    
    def predict_risk(
        self,
        sports_data: Dict[str, Any],
        use_model: bool = False
    ) -> Dict[str, Any]:
        """
        预测运动损伤风险
        
        Args:
            sports_data: 运动数据字典
            use_model: 是否使用训练好的模型（如果有）
            
        Returns:
            风险预测结果
        """
        result = {
            'risk_score': 0.0,
            'risk_level': 'low',
            'risk_factors': [],
            'confidence': 0.0
        }
        
        try:
            # 如果使用模型且有训练好的模型
            if use_model and self.initialized and self.model is not None:
                return self._predict_with_model(sports_data)
            
            # 否则使用基于规则的预测
            return self._predict_with_rules(sports_data)
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return result
    
    def _predict_with_rules(self, sports_data: Dict[str, Any]) -> Dict[str, Any]:
        """基于规则的预测（不需要训练模型）"""
        risk_factors = []
        risk_score = 0.0
        
        # 1. 伤病历史
        if sports_data.get('recent_injury', False):
            risk_factors.append('近期有伤病历史')
            risk_score += 0.3
        
        # 2. 训练负荷
        training_load = sports_data.get('training_load', 0.0)
        if training_load > 0.8:
            risk_factors.append('训练负荷过高')
            risk_score += 0.2
        elif training_load > 0.6:
            risk_factors.append('训练负荷较高')
            risk_score += 0.1
        
        # 3. 比赛强度
        match_intensity = sports_data.get('match_intensity', 0.0)
        if match_intensity > 0.8:
            risk_factors.append('比赛强度过大')
            risk_score += 0.2
        elif match_intensity > 0.6:
            risk_factors.append('比赛强度较高')
            risk_score += 0.1
        
        # 4. 比赛场次
        games_played = sports_data.get('games_played', 0)
        if games_played > 20:
            risk_factors.append('比赛场次过多')
            risk_score += 0.1
        
        # 5. 年龄因素
        age = sports_data.get('age', 25)
        if age > 30:
            risk_factors.append('年龄因素')
            risk_score += 0.05
        
        # 6. 恢复时间
        if 'recovery_days' in sports_data:
            recovery = sports_data['recovery_days']
            if recovery < 2:
                risk_factors.append('恢复时间不足')
                risk_score += 0.15
        
        # 限制风险分数在0-1之间
        risk_score = min(1.0, risk_score)
        
        # 计算风险等级
        if risk_score < 0.3:
            risk_level = 'low'
        elif risk_score < 0.6:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        # 计算置信度（基于风险因素数量）
        confidence = min(0.9, 0.5 + len(risk_factors) * 0.1)
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'confidence': confidence
        }
    
    def _predict_with_model(self, sports_data: Dict[str, Any]) -> Dict[str, Any]:
        """使用训练好的模型预测"""
        # 如果有训练好的模型，使用模型预测
        # 这里需要将sports_data转换为模型需要的格式
        try:
            player_df = pd.DataFrame([sports_data])
            
            # 使用模型预测
            if hasattr(self.model, 'predict_proba'):
                risk_proba = self.model.predict_proba(player_df)[0, 1]
            else:
                risk_proba = self.model.predict(player_df)[0]
            
            risk_score = float(risk_proba)
            
            if risk_score < 0.3:
                risk_level = 'low'
            elif risk_score < 0.6:
                risk_level = 'medium'
            else:
                risk_level = 'high'
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_factors': [],
                'confidence': 0.85
            }
        except Exception as e:
            logger.error(f"Model prediction error: {e}")
            return self._predict_with_rules(sports_data)
    
    def load_model(self, model_path: str):
        """加载训练好的模型"""
        try:
            import joblib
            self.model = joblib.load(model_path)
            logger.info(f"✓ Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
    
    def generate_recommendations(
        self,
        risk_score: float,
        risk_factors: List[str]
    ) -> List[str]:
        """生成预防建议"""
        recommendations = []
        
        if risk_score > 0.6:
            recommendations.extend([
                '⚠️ 建议立即减少训练强度，增加休息时间',
                '进行全面的身体评估',
                '关注恢复和营养补充',
                '考虑咨询运动医学专家'
            ])
        elif risk_score > 0.3:
            recommendations.extend([
                '适度调整训练计划',
                '加强热身和拉伸',
                '监控身体反应',
                '确保充足的睡眠和营养'
            ])
        else:
            recommendations.extend([
                '保持当前训练计划',
                '继续监控身体状况',
                '保持良好的运动习惯'
            ])
        
        # 根据具体风险因素添加针对性建议
        if '训练负荷过高' in risk_factors:
            recommendations.append('建议降低训练强度，增加恢复时间')
        
        if '比赛强度过大' in risk_factors:
            recommendations.append('考虑减少比赛频率，给身体更多恢复时间')
        
        if '近期有伤病历史' in risk_factors:
            recommendations.append('建议进行专业的康复训练，避免重复受伤')
        
        return recommendations

