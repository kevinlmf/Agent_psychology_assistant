"""
Economics Health Agent - 经济健康Agent
考虑经济因素对健康的影响，包括收入、国家健康国情等
"""

from typing import Dict, Any, Optional, List
import logging

from .country_health_profiles import (
    CountryHealthProfile,
    get_country_profile,
    IncomeLevel,
    get_income_level_threshold
)

logger = logging.getLogger(__name__)


class EconomicsHealthAgent:
    """
    经济健康Agent
    分析经济因素对健康的影响，提供基于经济状况的健康建议
    """
    
    def __init__(self):
        """初始化经济健康Agent"""
        self.initialized = True
        logger.info("✓ Economics Health Agent initialized")
    
    def analyze_economic_health(
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
            country_code: 国家代码（如 "US", "CN", "IN"）
            health_concerns: 健康关注点列表
            context: 其他上下文信息
            
        Returns:
            经济健康分析结果
        """
        result = {
            'agent_type': 'economics_health',
            'economic_assessment': {},
            'healthcare_accessibility': {},
            'recommendations': [],
            'barriers': [],
            'opportunities': []
        }
        
        try:
            # 1. 获取国家健康国情
            country_profile = None
            if country_code:
                country_profile = get_country_profile(country_code)
                if country_profile:
                    result['economic_assessment']['country'] = {
                        'name': country_profile.country_name,
                        'income_level': country_profile.income_level.value,
                        'gdp_per_capita': country_profile.gdp_per_capita
                    }
            
            # 2. 分析收入水平
            income_assessment = self._assess_income_level(user_income, country_profile)
            result['economic_assessment']['income'] = income_assessment
            
            # 3. 评估医疗可及性
            accessibility = self._assess_healthcare_accessibility(
                user_income, country_profile
            )
            result['healthcare_accessibility'] = accessibility
            
            # 4. 识别经济障碍
            barriers = self._identify_economic_barriers(
                user_income, country_profile, health_concerns
            )
            result['barriers'] = barriers
            
            # 5. 识别机会和资源
            opportunities = self._identify_opportunities(
                user_income, country_profile
            )
            result['opportunities'] = opportunities
            
            # 6. 生成基于经济的健康建议
            recommendations = self._generate_economic_recommendations(
                user_income, country_profile, barriers, opportunities
            )
            result['recommendations'] = recommendations
            
        except Exception as e:
            logger.error(f"Economics Health Agent error: {e}")
            result['error'] = str(e)
        
        return result
    
    def _assess_income_level(
        self,
        user_income: Optional[float],
        country_profile: Optional[CountryHealthProfile]
    ) -> Dict[str, Any]:
        """评估收入水平"""
        assessment = {
            'income': user_income,
            'relative_level': 'unknown',
            'affordability': {}
        }
        
        if user_income is None:
            return assessment
        
        # 如果有国家信息，进行相对评估
        if country_profile:
            gdp_per_capita = country_profile.gdp_per_capita
            
            if user_income < gdp_per_capita * 0.5:
                assessment['relative_level'] = 'low'
            elif user_income < gdp_per_capita:
                assessment['relative_level'] = 'below_average'
            elif user_income < gdp_per_capita * 1.5:
                assessment['relative_level'] = 'average'
            elif user_income < gdp_per_capita * 2:
                assessment['relative_level'] = 'above_average'
            else:
                assessment['relative_level'] = 'high'
            
            # 评估可负担性
            assessment['affordability'] = {
                'healthcare': self._can_afford_healthcare(user_income, country_profile),
                'preventive_care': self._can_afford_preventive(user_income, country_profile),
                'mental_health': self._can_afford_mental_health(user_income, country_profile)
            }
        else:
            # 使用世界银行标准
            thresholds = {
                IncomeLevel.LOW: 1045,
                IncomeLevel.LOWER_MIDDLE: 4095,
                IncomeLevel.UPPER_MIDDLE: 12695,
                IncomeLevel.HIGH: 12696
            }
            
            if user_income < thresholds[IncomeLevel.LOW]:
                assessment['relative_level'] = 'very_low'
            elif user_income < thresholds[IncomeLevel.LOWER_MIDDLE]:
                assessment['relative_level'] = 'low'
            elif user_income < thresholds[IncomeLevel.UPPER_MIDDLE]:
                assessment['relative_level'] = 'middle'
            else:
                assessment['relative_level'] = 'high'
        
        return assessment
    
    def _can_afford_healthcare(
        self,
        income: float,
        country_profile: Optional[CountryHealthProfile]
    ) -> bool:
        """评估是否能负担医疗费用"""
        if not country_profile:
            return income > 5000  # 简单阈值
        
        # 基于国家医疗支出和收入水平
        if country_profile.public_healthcare_coverage > 0.8:
            return True  # 高公共医保覆盖率
        
        # 估算医疗费用（年收入的10-20%）
        estimated_healthcare_cost = income * 0.15
        
        # 如果收入足够覆盖医疗费用
        return income - estimated_healthcare_cost > country_profile.gdp_per_capita * 0.3
    
    def _can_afford_preventive(
        self,
        income: float,
        country_profile: Optional[CountryHealthProfile]
    ) -> bool:
        """评估是否能负担预防性医疗"""
        return self._can_afford_healthcare(income, country_profile)
    
    def _can_afford_mental_health(
        self,
        income: float,
        country_profile: Optional[CountryHealthProfile]
    ) -> bool:
        """评估是否能负担心理健康服务"""
        # 心理健康服务通常更昂贵且覆盖率更低
        if country_profile and country_profile.public_healthcare_coverage > 0.9:
            return True
        
        return income > 10000  # 心理健康服务需要更高收入
    
    def _assess_healthcare_accessibility(
        self,
        user_income: Optional[float],
        country_profile: Optional[CountryHealthProfile]
    ) -> Dict[str, Any]:
        """评估医疗可及性"""
        accessibility = {
            'overall_score': 0.5,
            'factors': {},
            'barriers': []
        }
        
        if not country_profile:
            return accessibility
        
        # 基础可及性（基于国家医疗系统）
        base_accessibility = country_profile.healthcare_accessibility
        accessibility['factors']['country_system'] = base_accessibility
        
        # 收入因素
        if user_income:
            income_factor = min(1.0, user_income / country_profile.gdp_per_capita)
            accessibility['factors']['income'] = income_factor
            
            # 如果收入低，可及性降低
            if income_factor < 0.5:
                accessibility['barriers'].append('收入不足影响医疗可及性')
        else:
            accessibility['factors']['income'] = 0.5
        
        # 公共医保覆盖率
        accessibility['factors']['public_coverage'] = country_profile.public_healthcare_coverage
        
        # 计算综合可及性分数
        accessibility['overall_score'] = (
            base_accessibility * 0.4 +
            accessibility['factors'].get('income', 0.5) * 0.3 +
            country_profile.public_healthcare_coverage * 0.3
        )
        
        return accessibility
    
    def _identify_economic_barriers(
        self,
        user_income: Optional[float],
        country_profile: Optional[CountryHealthProfile],
        health_concerns: Optional[List[str]]
    ) -> List[str]:
        """识别经济障碍"""
        barriers = []
        
        if not user_income:
            barriers.append('收入信息未知，无法准确评估经济障碍')
            return barriers
        
        if not country_profile:
            if user_income < 5000:
                barriers.append('低收入可能限制医疗选择')
            return barriers
        
        # 基于收入和国家的障碍分析
        gdp_per_capita = country_profile.gdp_per_capita
        
        if user_income < gdp_per_capita * 0.5:
            barriers.append('收入远低于国家平均水平，可能难以负担医疗费用')
            barriers.append('可能无法获得优质医疗服务')
        
        if country_profile.public_healthcare_coverage < 0.5:
            barriers.append('公共医保覆盖率低，需要自费医疗')
        
        if user_income < 10000 and 'mental_health' in (health_concerns or []):
            barriers.append('心理健康服务费用较高，可能难以负担')
        
        if country_profile.healthcare_accessibility < 0.6:
            barriers.append('国家医疗可及性较低')
        
        return barriers
    
    def _identify_opportunities(
        self,
        user_income: Optional[float],
        country_profile: Optional[CountryHealthProfile]
    ) -> List[str]:
        """识别机会和可用资源"""
        opportunities = []
        
        if not country_profile:
            return opportunities
        
        # 公共医保机会
        if country_profile.public_healthcare_coverage > 0.8:
            opportunities.append('国家提供高覆盖率的公共医保')
            opportunities.append('可以优先使用公共医疗服务')
        
        # 预防性医疗机会
        if country_profile.healthcare_accessibility > 0.7:
            opportunities.append('医疗可及性较高，可以方便获得预防性医疗')
        
        # 文化健康资源
        if country_profile.cultural_health_beliefs:
            opportunities.append(f'可以利用文化健康资源: {", ".join(country_profile.cultural_health_beliefs)}')
        
        # 基于收入的机会
        if user_income and user_income > country_profile.gdp_per_capita:
            opportunities.append('收入高于平均水平，有更多医疗选择')
        
        return opportunities
    
    def _generate_economic_recommendations(
        self,
        user_income: Optional[float],
        country_profile: Optional[CountryHealthProfile],
        barriers: List[str],
        opportunities: List[str]
    ) -> List[str]:
        """生成基于经济的健康建议"""
        recommendations = []
        
        if not country_profile:
            if user_income and user_income < 5000:
                recommendations.append('💡 建议优先使用公共医疗资源')
                recommendations.append('💡 寻找社区健康服务和免费筛查项目')
            return recommendations
        
        # 基于国家健康国情的建议
        if country_profile.public_healthcare_coverage > 0.8:
            recommendations.append('✅ 优先使用公共医保系统，可以大幅降低医疗成本')
        
        if country_profile.healthcare_accessibility < 0.6:
            recommendations.append('⚠️ 医疗可及性较低，建议提前规划医疗需求')
        
        # 基于收入水平的建议
        if user_income:
            gdp_per_capita = country_profile.gdp_per_capita
            
            if user_income < gdp_per_capita * 0.5:
                recommendations.append('💰 收入较低，建议：')
                recommendations.append('  - 充分利用公共医疗资源')
                recommendations.append('  - 寻找免费或低成本的健康筛查')
                recommendations.append('  - 关注预防性医疗，避免昂贵治疗')
                recommendations.append('  - 考虑社区健康服务')
            
            elif user_income < gdp_per_capita:
                recommendations.append('💰 收入中等，建议：')
                recommendations.append('  - 平衡使用公共和私人医疗')
                recommendations.append('  - 考虑购买补充医疗保险')
                recommendations.append('  - 定期进行健康检查')
            
            else:
                recommendations.append('💰 收入较高，建议：')
                recommendations.append('  - 可以选择优质医疗服务')
                recommendations.append('  - 投资预防性医疗和健康管理')
                recommendations.append('  - 考虑私人医疗保险以获得更好服务')
        
        # 基于文化健康观念的建议
        if 'traditional_medicine' in country_profile.cultural_health_beliefs:
            recommendations.append('🌿 可以考虑结合传统医学和现代医疗')
        
        if 'preventive_care' in country_profile.cultural_health_beliefs:
            recommendations.append('🛡️ 重视预防性医疗，这是成本效益最高的健康投资')
        
        # 基于常见健康问题的建议
        if 'diabetes' in country_profile.common_health_issues:
            recommendations.append('⚠️ 注意糖尿病预防，这是本地区常见健康问题')
        
        if 'mental_health' in country_profile.common_health_issues:
            if user_income and user_income > country_profile.gdp_per_capita:
                recommendations.append('🧠 考虑投资心理健康服务')
            else:
                recommendations.append('🧠 寻找社区心理健康资源或在线咨询服务')
        
        return recommendations

