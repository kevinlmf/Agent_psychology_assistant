"""
Country Health Profiles - 国家健康国情数据
不同国家的健康国情、医疗资源、经济水平等信息
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class IncomeLevel(Enum):
    """收入水平分类"""
    LOW = "low"           # 低收入国家
    LOWER_MIDDLE = "lower_middle"  # 中低收入国家
    UPPER_MIDDLE = "upper_middle"  # 中高收入国家
    HIGH = "high"         # 高收入国家


@dataclass
class CountryHealthProfile:
    """国家健康国情档案"""
    country_code: str
    country_name: str
    income_level: IncomeLevel
    
    # 医疗资源
    healthcare_accessibility: float  # 0-1, 医疗可及性
    healthcare_quality: float        # 0-1, 医疗质量
    public_healthcare_coverage: float  # 0-1, 公共医保覆盖率
    
    # 健康指标
    life_expectancy: float           # 预期寿命
    infant_mortality_rate: float     # 婴儿死亡率（每1000人）
    health_expenditure_gdp: float    # 健康支出占GDP百分比
    
    # 经济指标
    gdp_per_capita: float            # 人均GDP（美元）
    poverty_rate: float              # 贫困率（百分比）
    
    # 健康国情特点
    common_health_issues: list       # 常见健康问题
    healthcare_system_type: str      # 医疗体系类型
    cultural_health_beliefs: list   # 文化健康观念


# 国家健康国情数据库
COUNTRY_HEALTH_DATABASE = {
    # 高收入国家
    "US": CountryHealthProfile(
        country_code="US",
        country_name="United States",
        income_level=IncomeLevel.HIGH,
        healthcare_accessibility=0.7,  # 高但昂贵
        healthcare_quality=0.9,
        public_healthcare_coverage=0.5,  # 部分公共医保
        life_expectancy=78.5,
        infant_mortality_rate=5.7,
        health_expenditure_gdp=17.8,
        gdp_per_capita=63000,
        poverty_rate=11.8,
        common_health_issues=["obesity", "diabetes", "heart_disease", "mental_health"],
        healthcare_system_type="mixed",
        cultural_health_beliefs=["preventive_care", "fitness_culture"]
    ),
    
    "CN": CountryHealthProfile(
        country_code="CN",
        country_name="China",
        income_level=IncomeLevel.UPPER_MIDDLE,
        healthcare_accessibility=0.8,
        healthcare_quality=0.75,
        public_healthcare_coverage=0.95,  # 高覆盖率
        life_expectancy=77.0,
        infant_mortality_rate=6.8,
        health_expenditure_gdp=5.4,
        gdp_per_capita=10500,
        poverty_rate=0.6,
        common_health_issues=["respiratory_disease", "diabetes", "hypertension", "cancer"],
        healthcare_system_type="public_dominant",
        cultural_health_beliefs=["traditional_medicine", "preventive_care"]
    ),
    
    "IN": CountryHealthProfile(
        country_code="IN",
        country_name="India",
        income_level=IncomeLevel.LOWER_MIDDLE,
        healthcare_accessibility=0.5,
        healthcare_quality=0.6,
        public_healthcare_coverage=0.3,
        life_expectancy=70.0,
        infant_mortality_rate=28.3,
        health_expenditure_gdp=3.5,
        gdp_per_capita=2100,
        poverty_rate=21.9,
        common_health_issues=["infectious_disease", "malnutrition", "diabetes", "tuberculosis"],
        healthcare_system_type="mixed",
        cultural_health_beliefs=["ayurveda", "yoga", "traditional_medicine"]
    ),
    
    "BR": CountryHealthProfile(
        country_code="BR",
        country_name="Brazil",
        income_level=IncomeLevel.UPPER_MIDDLE,
        healthcare_accessibility=0.7,
        healthcare_quality=0.7,
        public_healthcare_coverage=0.8,
        life_expectancy=75.5,
        infant_mortality_rate=12.4,
        health_expenditure_gdp=9.6,
        gdp_per_capita=8500,
        poverty_rate=21.4,
        common_health_issues=["dengue", "diabetes", "hypertension", "mental_health"],
        healthcare_system_type="public_universal",
        cultural_health_beliefs=["preventive_care", "community_health"]
    ),
    
    # 可以添加更多国家...
}


def get_country_profile(country_code: str) -> Optional[CountryHealthProfile]:
    """
    获取国家健康国情档案
    
    Args:
        country_code: 国家代码（如 "US", "CN", "IN"）
        
    Returns:
        国家健康档案，如果不存在返回None
    """
    return COUNTRY_HEALTH_DATABASE.get(country_code.upper())


def get_income_level_threshold(income_level: IncomeLevel) -> Dict[str, float]:
    """
    获取不同收入水平的阈值
    
    Returns:
        收入阈值字典
    """
    thresholds = {
        IncomeLevel.LOW: {"min": 0, "max": 1045},
        IncomeLevel.LOWER_MIDDLE: {"min": 1046, "max": 4095},
        IncomeLevel.UPPER_MIDDLE: {"min": 4096, "max": 12695},
        IncomeLevel.HIGH: {"min": 12696, "max": float('inf')}
    }
    return thresholds.get(income_level, {"min": 0, "max": float('inf')})

