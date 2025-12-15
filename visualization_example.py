#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的多智能体可视化示例
直接运行此文件来测试可视化功能
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agent_visualization import XMLParser, AgentVisualizer
import os

def run_example():
    """运行示例"""
    # 检查示例文件是否存在
    task_file = "task_examples/empty_task.xml"
    log_file = "task_examples/1_task_10_log.xml"
    
    if not os.path.exists(task_file):
        print(f"示例文件 {task_file} 不存在")
        print("请确保在项目根目录运行此脚本")
        return
    
    try:
        print("=== 多智能体路径可视化示例 ===")
        print(f"正在加载任务文件: {task_file}")
        
        # 解析任务文件
        game_map, agents = XMLParser.parse_task_file(task_file)
        print(f"地图大小: {game_map.width} x {game_map.height}")
        print(f"智能体数量: {len(agents)}")
        
        # 如果有日志文件，加载路径数据
        if os.path.exists(log_file):
            print(f"正在加载日志文件: {log_file}")
            agents = XMLParser.parse_log_file(log_file, agents)
            
            # 显示路径信息
            for agent in agents[:5]:  # 只显示前5个智能体的信息
                print(f"智能体 {agent.id}: 路径长度 {len(agent.path)} 步")
        else:
            print("未找到日志文件，将只显示起点和终点")
        
        # 创建可视化
        print("正在创建可视化...")
        visualizer = AgentVisualizer(game_map, agents)
        
        # 显示动画
        print("显示动画窗口...")
        print("提示：")
        print("- 绿色圆点：起点")
        print("- 红色方块：终点") 
        print("- 彩色圆圈：智能体当前位置")
        print("- 圆圈内数字：智能体ID")
        
        anim = visualizer.create_animation(interval=300)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_example()