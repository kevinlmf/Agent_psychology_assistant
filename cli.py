#!/usr/bin/env python3
"""
Health System CLI - 命令行接口
在terminal中使用Health系统
"""

import asyncio
import sys
import json
import argparse
from typing import Optional, Dict, Any

from core.health_coordinator import HealthCoordinator


def print_result(result: Dict[str, Any], verbose: bool = False):
    """打印分析结果"""
    print("\n" + "=" * 60)
    print("健康分析结果")
    print("=" * 60)
    
    # 基本信息
    print(f"\n📅 时间: {result.get('timestamp', 'N/A')}")
    print(f"👤 用户ID: {result.get('user_id', 'N/A')}")
    print(f"💬 消息: {result.get('message', 'N/A')}")
    
    # 各Agent分析结果
    if 'agents' in result:
        agents = result['agents']
        
        # 心理健康
        if 'mental_health' in agents:
            mental = agents['mental_health']
            print("\n🧠 心理健康分析:")
            if 'risk_assessment' in mental:
                risk = mental['risk_assessment']
                print(f"  风险等级: {risk.get('risk_level', 'N/A')}")
                print(f"  置信度: {risk.get('confidence', 0):.2f}")
            if 'recommendations' in mental:
                print("  建议:")
                for rec in mental['recommendations'][:3]:
                    print(f"    • {rec}")
        
        # 身体健康
        if 'physical_health' in agents:
            physical = agents['physical_health']
            print("\n💪 身体健康分析:")
            if 'injury_risk' in physical:
                risk = physical['injury_risk']
                print(f"  风险等级: {risk.get('risk_level', 'N/A')}")
                print(f"  风险分数: {risk.get('risk_score', 0):.2f}")
                if risk.get('risk_factors'):
                    print(f"  风险因素: {', '.join(risk['risk_factors'])}")
            if 'recommendations' in physical:
                print("  建议:")
                for rec in physical['recommendations'][:3]:
                    print(f"    • {rec}")
        
        # 经济健康
        if 'economics_health' in agents:
            econ = agents['economics_health']
            print("\n💰 经济健康分析:")
            if 'economic_assessment' in econ:
                assessment = econ['economic_assessment']
                if 'country' in assessment:
                    print(f"  国家: {assessment['country'].get('name', 'N/A')}")
                if 'income' in assessment:
                    income = assessment['income']
                    print(f"  收入水平: {income.get('relative_level', 'N/A')}")
            if 'healthcare_accessibility' in econ:
                access = econ['healthcare_accessibility']
                print(f"  医疗可及性: {access.get('overall_score', 0):.2f}")
            if 'barriers' in econ and econ['barriers']:
                print("  经济障碍:")
                for barrier in econ['barriers'][:2]:
                    print(f"    • {barrier}")
            if 'recommendations' in econ:
                print("  建议:")
                for rec in econ['recommendations'][:3]:
                    print(f"    • {rec}")
    
    # 综合分析
    if 'synthesis' in result:
        synthesis = result['synthesis']
        print("\n📊 综合分析:")
        print(f"  整体健康状态: {synthesis.get('overall_health_status', 'N/A')}")
        
        if synthesis.get('warnings'):
            print("\n  ⚠️  警告:")
            for warning in synthesis['warnings']:
                print(f"    • {warning}")
        
        if synthesis.get('recommendations'):
            print("\n  💡 综合建议:")
            for rec in synthesis['recommendations'][:5]:
                print(f"    • {rec}")
        
        if synthesis.get('insights'):
            print("\n  🔍 洞察:")
            for insight in synthesis['insights'][:3]:
                print(f"    • {insight}")
    
    print("\n" + "=" * 60)


async def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("Health System - 交互式模式")
    print("=" * 60)
    print("\n输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看帮助\n")
    
    coordinator = HealthCoordinator()
    user_id = "cli_user"
    
    while True:
        try:
            # 获取用户输入
            message = input("\n💬 请输入您的健康问题: ").strip()
            
            if not message:
                continue
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            if message.lower() == 'help':
                print_help()
                continue
            
            # 询问是否需要经济信息
            print("\n是否需要提供经济信息？(y/n，直接回车跳过)")
            econ_input = input("> ").strip().lower()
            
            context = {}
            if econ_input == 'y':
                try:
                    income = float(input("  年收入（美元）: "))
                    country = input("  国家代码（如 CN/US/IN，直接回车跳过）: ").strip()
                    
                    context['user_income'] = income
                    if country:
                        context['country_code'] = country.upper()
                except ValueError:
                    print("  ⚠️ 收入格式错误，跳过经济分析")
            
            # 询问是否需要运动数据
            print("\n是否需要提供运动数据？(y/n，直接回车跳过)")
            sports_input = input("> ").strip().lower()
            
            if sports_input == 'y':
                try:
                    age = int(input("  年龄: "))
                    training_load = float(input("  训练负荷 (0-1): "))
                    match_intensity = float(input("  比赛强度 (0-1): "))
                    
                    context['sports_data'] = {
                        'age': age,
                        'training_load': training_load,
                        'match_intensity': match_intensity
                    }
                except ValueError:
                    print("  ⚠️ 数据格式错误，跳过运动分析")
            
            # 分析
            print("\n🔍 正在分析...")
            result = await coordinator.process_message(
                message=message,
                user_id=user_id,
                context=context if context else None
            )
            
            # 打印结果
            print_result(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()


def print_help():
    """打印帮助信息"""
    print("""
📖 使用帮助:

1. 基本使用:
   直接输入您的健康问题，系统会自动分析

2. 提供经济信息:
   输入 'y' 后，可以输入：
   - 年收入（美元）
   - 国家代码（CN/US/IN/BR等）

3. 提供运动数据:
   输入 'y' 后，可以输入：
   - 年龄
   - 训练负荷 (0-1)
   - 比赛强度 (0-1)

4. 命令:
   - quit/exit/q: 退出
   - help: 显示帮助

示例:
   💬 请输入您的健康问题: 我最近压力很大
   💬 请输入您的健康问题: 我运动时膝盖疼，年收入5000美元，在中国
""")


async def single_query(
    message: str,
    user_id: str = "cli_user",
    income: Optional[float] = None,
    country: Optional[str] = None,
    age: Optional[int] = None,
    training_load: Optional[float] = None,
    match_intensity: Optional[float] = None,
    json_output: bool = False
):
    """单次查询"""
    coordinator = HealthCoordinator()
    
    context = {}
    if income is not None:
        context['user_income'] = income
    if country:
        context['country_code'] = country.upper()
    if age is not None:
        context['sports_data'] = {
            'age': age,
            'training_load': training_load or 0.5,
            'match_intensity': match_intensity or 0.5
        }
    
    result = await coordinator.process_message(
        message=message,
        user_id=user_id,
        context=context if context else None
    )
    
    if json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_result(result)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Health System CLI - 健康系统命令行接口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式模式
  python cli.py

  # 单次查询
  python cli.py -m "我最近压力很大"

  # 带经济信息
  python cli.py -m "我想看心理医生但担心费用" --income 5000 --country CN

  # 带运动数据
  python cli.py -m "我运动时膝盖疼" --age 28 --training-load 0.8

  # JSON输出
  python cli.py -m "我最近压力大" --json
        """
    )
    
    parser.add_argument(
        '-m', '--message',
        type=str,
        help='用户消息'
    )
    
    parser.add_argument(
        '-u', '--user-id',
        type=str,
        default='cli_user',
        help='用户ID（默认: cli_user）'
    )
    
    parser.add_argument(
        '--income',
        type=float,
        help='年收入（美元）'
    )
    
    parser.add_argument(
        '--country',
        type=str,
        help='国家代码（如 CN/US/IN/BR）'
    )
    
    parser.add_argument(
        '--age',
        type=int,
        help='年龄'
    )
    
    parser.add_argument(
        '--training-load',
        type=float,
        help='训练负荷 (0-1)'
    )
    
    parser.add_argument(
        '--match-intensity',
        type=float,
        help='比赛强度 (0-1)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='以JSON格式输出结果'
    )
    
    args = parser.parse_args()
    
    # 如果没有提供消息，进入交互式模式
    if not args.message:
        asyncio.run(interactive_mode())
    else:
        asyncio.run(single_query(
            message=args.message,
            user_id=args.user_id,
            income=args.income,
            country=args.country,
            age=args.age,
            training_load=args.training_load,
            match_intensity=args.match_intensity,
            json_output=args.json
        ))


if __name__ == "__main__":
    main()

