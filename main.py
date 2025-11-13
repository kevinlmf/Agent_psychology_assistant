"""
Multi-Agent LLM for Health - Main Entry Point
统一的多智能体健康AI系统主入口
"""

import asyncio
import sys
import os
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client.health_client import HealthClient


class HealthApp:
    """
    Multi-Agent LLM for Health 主应用程序
    """
    
    def __init__(self):
        """初始化应用"""
        logger.info("Initializing Multi-Agent LLM for Health System...")
        self.client = HealthClient()
        logger.info("✓ System initialized")
    
    async def process_query(
        self,
        message: str,
        user_id: str = "default_user",
        sports_data: Optional[Dict[str, Any]] = None,
        behavior_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        处理健康查询
        
        Args:
            message: 用户消息
            user_id: 用户ID
            sports_data: 运动数据（可选）
            behavior_data: 行为数据（可选）
            
        Returns:
            健康分析结果
        """
        return await self.client.send_message(
            message=message,
            user_id=user_id,
            sports_data=sports_data,
            behavior_data=behavior_data
        )
    
    def get_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """获取用户健康摘要"""
        return self.client.get_health_summary(user_id, days)


async def demo_comprehensive():
    """综合演示"""
    print("\n" + "=" * 60)
    print("Multi-Agent LLM for Health - Comprehensive Demo")
    print("=" * 60)
    
    app = HealthApp()
    
    # 示例1: 综合健康查询
    print("\n📝 示例1: 综合健康查询")
    print("-" * 60)
    
    message = "我最近工作压力很大，睡眠不好，而且运动时膝盖有点疼"
    
    sports_data = {
        'age': 28,
        'position': 'MID',
        'height': 175,
        'weight': 70,
        'games_played': 10,
        'minutes_played': 900,
        'recent_injury': False,
        'training_load': 0.8,
        'match_intensity': 0.7
    }
    
    behavior_data = {
        'search_history': ['失眠怎么办', '工作压力大', '膝盖疼'],
        'app_usage': {
            'screen_time': 8.5,
            'sleep_tracking': 5.5
        }
    }
    
    print(f"用户消息: {message}")
    print("\n处理中...")
    
    result = await app.process_query(
        message=message,
        user_id="demo_user_001",
        sports_data=sports_data,
        behavior_data=behavior_data
    )
    
    # 格式化输出
    formatted = app.client.format_response(result)
    print(formatted)
    
    print("\n" + "=" * 60)


async def demo_mental_health():
    """心理健康演示"""
    print("\n" + "=" * 60)
    print("Multi-Agent LLM for Health - Mental Health Demo")
    print("=" * 60)
    
    app = HealthApp()
    
    message = "我最近工作压力很大，经常感到焦虑，不知道该怎么办"
    
    behavior_data = {
        'search_history': ['焦虑症', '工作压力', '失眠'],
        'app_usage': {
            'screen_time': 10,
            'sleep_tracking': 4.5
        }
    }
    
    print(f"用户消息: {message}")
    print("\n处理中...")
    
    result = await app.process_query(
        message=message,
        user_id="demo_user_mental",
        behavior_data=behavior_data
    )
    
    formatted = app.client.format_response(result)
    print(formatted)
    
    print("\n" + "=" * 60)


async def demo_physical_health():
    """身体健康演示"""
    print("\n" + "=" * 60)
    print("Multi-Agent LLM for Health - Physical Health Demo")
    print("=" * 60)
    
    app = HealthApp()
    
    message = "我想了解我的运动损伤风险"
    
    sports_data = {
        'age': 25,
        'position': 'FWD',
        'height': 180,
        'weight': 75,
        'games_played': 20,
        'minutes_played': 1800,
        'recent_injury': True,
        'training_load': 0.9,
        'match_intensity': 0.85
    }
    
    print(f"用户消息: {message}")
    print("\n处理中...")
    
    result = await app.process_query(
        message=message,
        user_id="demo_user_sports",
        sports_data=sports_data
    )
    
    formatted = app.client.format_response(result)
    print(formatted)
    
    print("\n" + "=" * 60)


async def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 60)
    print("Multi-Agent LLM for Health - Interactive Mode")
    print("=" * 60)
    print("\n输入 'quit' 或 'exit' 退出")
    print("输入 'summary' 查看健康摘要")
    print("-" * 60)
    
    app = HealthApp()
    user_id = input("\n请输入用户ID (默认: demo_user): ").strip() or "demo_user"
    
    while True:
        try:
            message = input("\n您: ").strip()
            
            if not message:
                continue
            
            if message.lower() in ['quit', 'exit']:
                print("\n感谢使用Multi-Agent LLM for Health系统！")
                break
            
            if message.lower() == 'summary':
                summary = app.get_summary(user_id)
                print(f"\n健康摘要: {summary}")
                continue
            
            print("\n处理中...")
            result = await app.process_query(message, user_id=user_id)
            
            # 显示格式化结果
            formatted = app.client.format_response(result)
            print("\n" + formatted)
        
        except KeyboardInterrupt:
            print("\n\n退出...")
            break
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Multi-Agent LLM for Health")
    print("统一的多智能体健康AI系统")
    print("=" * 60)
    print("\n请选择模式:")
    print("1. 综合健康查询演示")
    print("2. 心理健康演示")
    print("3. 身体健康演示")
    print("4. 交互模式")
    print("5. 运行所有演示")
    
    try:
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == '1':
            asyncio.run(demo_comprehensive())
        elif choice == '2':
            asyncio.run(demo_mental_health())
        elif choice == '3':
            asyncio.run(demo_physical_health())
        elif choice == '4':
            asyncio.run(interactive_mode())
        elif choice == '5':
            asyncio.run(demo_comprehensive())
            asyncio.run(demo_mental_health())
            asyncio.run(demo_physical_health())
        else:
            print("无效选择")
    
    except KeyboardInterrupt:
        print("\n\n退出")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
