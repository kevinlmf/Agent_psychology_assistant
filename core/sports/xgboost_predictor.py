"""
XGBoost Predictor (Optional)
如果需要使用训练好的XGBoost模型，可以加载使用
"""

from typing import Dict, Any, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class XGBoostPredictor:
    """
    XGBoost预测器包装
    用于加载和使用训练好的XGBoost模型
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        初始化XGBoost预测器
        
        Args:
            model_path: 模型文件路径（可选）
        """
        self.model = None
        self.model_path = model_path
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """加载训练好的模型"""
        try:
            import joblib
            self.model = joblib.load(model_path)
            logger.info(f"✓ XGBoost model loaded from {model_path}")
        except Exception as e:
            logger.warning(f"Failed to load XGBoost model: {e}")
            self.model = None
    
    def predict(self, data: pd.DataFrame) -> float:
        """
        使用模型预测
        
        Args:
            data: 特征DataFrame
            
        Returns:
            风险分数
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please load a model first.")
        
        if hasattr(self.model, 'predict_proba'):
            risk_proba = self.model.predict_proba(data)[0, 1]
        else:
            risk_proba = self.model.predict(data)[0]
        
        return float(risk_proba)

