"""
Economics Health Module - 经济健康模块
考虑经济因素对健康的影响，包括国家健康国情、收入水平等
"""

from .economics_agent import EconomicsHealthAgent
from .country_health_profiles import CountryHealthProfile, get_country_profile

__all__ = [
    "EconomicsHealthAgent",
    "CountryHealthProfile",
    "get_country_profile",
]

