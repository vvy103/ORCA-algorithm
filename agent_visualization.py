#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多智能体路径可视化工具
支持读取XML格式的地图和智能体轨迹数据，生成动态可视化
"""

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Polygon
import argparse
import os
from typing import List, Dict, Tuple, Optional

class Agent:
    """智能体类，存储智能体的基本信息和路径"""
    def __init__(self, agent_id: int, start_pos: Tuple[float, float], 
                 goal_pos: Tuple[float, float], size: float = 0.3):
        self.id = agent_id
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.size = size
        self.path = []  # 存储路径点 [(x, y, time), ...]
        
    def add_path_point(self, x: float, y: float, step: int):
        """添加路径点"""
        self.path.append((x, y, step))
        
    def get_position_at_step(self, step: int) -> Tuple[float, float]:
        """获取指定步骤的位置"""
        if not self.path:
            return self.start_pos
            
        # 如果步骤超出路径范围，返回最后一个位置
        if step >= len(self.path):
            return (self.path[-1][0], self.path[-1][1])
            
        # 如果步骤小于0，返回起始位置
        if step < 0:
            return self.start_pos
            
        return (self.path[step][0], self.path[step][1])

class Map:
    """地图类，存储地图信息和障碍物"""
    def __init__(self, width: int, height: int, cellsize: float = 1.0):
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.grid = np.zeros((height, width))  # 0为可通行，1为障碍物
        self.obstacles = []  # 存储多边形障碍物
        
    def set_grid_cell(self, x: int, y: int, value: int):
        """设置网格单元格的值"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = value
            
    def add_obstacle(self, vertices: List[Tuple[float, float]]):
        """添加多边形障碍物"""
        self.obstacles.append(vertices)

class XMLParser:
    """XML文件解析器"""
    
    @staticmethod
    def parse_task_file(filename: str) -> Tuple[Map, List[Agent]]:
        """解析任务XML文件，返回地图和智能体列表"""
        tree = ET.parse(filename)
        root = tree.getroot()
        
        # 解析地图
        map_elem = root.find('map')
        width = int(map_elem.find('width').text)
        height = int(map_elem.find('height').text)
        cellsize_elem = map_elem.find('cellsize')
        cellsize = float(cellsize_elem.text) if cellsize_elem is not None else 1.0
        
        game_map = Map(width, height, cellsize)
        
        # 解析网格
        grid_elem = map_elem.find('grid')
        if grid_elem is not None:
            rows = grid_elem.findall('row')
            for y, row in enumerate(rows):
                if row.text:
                    values = list(map(int, row.text.split()))
                    for x, value in enumerate(values):
                        game_map.set_grid_cell(x, y, value)
        
        # 解析障碍物
        obstacles_elem = root.find('obstacles')
        if obstacles_elem is not None:
            for obstacle in obstacles_elem.findall('obstacle'):
                vertices = []
                for vertex in obstacle.findall('vertex'):
                    x = float(vertex.get('xr'))
                    y = float(vertex.get('yr'))
                    vertices.append((x, y))
                if vertices:
                    game_map.add_obstacle(vertices)
        
        # 解析智能体
        agents_elem = root.find('agents')
        default_params = agents_elem.find('default_parameters')
        default_size = float(default_params.get('size', 0.3))
        
        agents = []
        for agent_elem in agents_elem.findall('agent'):
            agent_id = int(agent_elem.get('id'))
            start_x = float(agent_elem.get('start.xr'))
            start_y = float(agent_elem.get('start.yr'))
            goal_x = float(agent_elem.get('goal.xr'))
            goal_y = float(agent_elem.get('goal.yr'))
            size = float(agent_elem.get('size', default_size))
            
            agent = Agent(agent_id, (start_x, start_y), (goal_x, goal_y), size)
            agents.append(agent)
            
        return game_map, agents
    
    @staticmethod
    def parse_log_file(filename: str, agents: List[Agent]) -> List[Agent]:
        """解析日志XML文件，为智能体添加路径信息"""
        tree = ET.parse(filename)
        root = tree.getroot()
        
        # 创建智能体ID到对象的映射
        agent_dict = {agent.id: agent for agent in agents}
        
        # 解析每个智能体的路径
        for agent_elem in root.findall('.//agent'):
            agent_number = int(agent_elem.get('number'))
            if agent_number in agent_dict:
                agent = agent_dict[agent_number]
                path_elem = agent_elem.find('path')
                if path_elem is not None:
                    for step_elem in path_elem.findall('step'):
                        step_num = int(step_elem.get('number'))
                        x = float(step_elem.get('x'))
                        y = float(step_elem.get('y'))
                        agent.add_path_point(x, y, step_num)
        
        return agents

class AgentVisualizer:
    """智能体可视化类"""
    
    def __init__(self, game_map: Map, agents: List[Agent]):
        self.map = game_map
        self.agents = agents
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.agent_circles = []
        self.agent_texts = []
        self.max_steps = self._calculate_max_steps()
        
    def _calculate_max_steps(self) -> int:
        """计算最大步数"""
        max_steps = 0
        for agent in self.agents:
            if agent.path:
                max_steps = max(max_steps, len(agent.path))
        return max_steps
    
    def setup_plot(self):
        """设置绘图环境"""
        # 设置坐标轴
        self.ax.set_xlim(-1, self.map.width * self.map.cellsize + 1)
        self.ax.set_ylim(-1, self.map.height * self.map.cellsize + 1)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('多智能体路径可视化')
        
        # 绘制网格障碍物
        self._draw_grid_obstacles()
        
        # 绘制多边形障碍物
        self._draw_polygon_obstacles()
        
        # 绘制起点和终点
        self._draw_start_goal_points()
        
        # 初始化智能体圆圈和标签
        self._initialize_agent_graphics()
        
    def _draw_grid_obstacles(self):
        """绘制网格障碍物"""
        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.grid[y, x] == 1:
                    rect = plt.Rectangle((x * self.map.cellsize, 
                                        (self.map.height - 1 - y) * self.map.cellsize),
                                       self.map.cellsize, self.map.cellsize,
                                       facecolor='black', alpha=0.8)
                    self.ax.add_patch(rect)
    
    def _draw_polygon_obstacles(self):
        """绘制多边形障碍物"""
        for vertices in self.map.obstacles:
            # 转换坐标系（XML中y轴向上，matplotlib中y轴向下）
            converted_vertices = [(x, self.map.height * self.map.cellsize - y) 
                                for x, y in vertices]
            polygon = Polygon(converted_vertices, facecolor='gray', 
                            alpha=0.5, edgecolor='black')
            self.ax.add_patch(polygon)
    
    def _draw_start_goal_points(self):
        """绘制起点和终点"""
        for agent in self.agents:
            # 起点（绿色）
            start_x, start_y = agent.start_pos
            start_y = self.map.height * self.map.cellsize - start_y  # 坐标转换
            self.ax.plot(start_x, start_y, 'go', markersize=8, alpha=0.7)
            
            # 终点（红色）
            goal_x, goal_y = agent.goal_pos
            goal_y = self.map.height * self.map.cellsize - goal_y  # 坐标转换
            self.ax.plot(goal_x, goal_y, 'rs', markersize=8, alpha=0.7)
    
    def _initialize_agent_graphics(self):
        """初始化智能体图形元素"""
        colors = plt.cm.tab10(np.linspace(0, 1, len(self.agents)))
        
        for i, agent in enumerate(self.agents):
            # 创建圆圈表示智能体
            circle = Circle((0, 0), agent.size, color=colors[i], alpha=0.7)
            self.ax.add_patch(circle)
            self.agent_circles.append(circle)
            
            # 创建文本标签
            text = self.ax.text(0, 0, str(agent.id), ha='center', va='center',
                              fontsize=8, fontweight='bold')
            self.agent_texts.append(text)
    
    def animate(self, frame):
        """动画更新函数"""
        for i, agent in enumerate(self.agents):
            x, y = agent.get_position_at_step(frame)
            # 坐标转换
            y = self.map.height * self.map.cellsize - y
            
            # 更新圆圈位置
            self.agent_circles[i].center = (x, y)
            
            # 更新文本位置
            self.agent_texts[i].set_position((x, y))
        
        # 更新标题显示当前步数
        self.ax.set_title(f'多智能体路径可视化 - 步骤: {frame}/{self.max_steps}')
        
        return self.agent_circles + self.agent_texts
    
    def create_animation(self, interval: int = 200, save_path: Optional[str] = None):
        """创建动画"""
        self.setup_plot()
        
        anim = animation.FuncAnimation(
            self.fig, self.animate, frames=self.max_steps + 1,
            interval=interval, blit=False, repeat=True
        )
        
        if save_path:
            print(f"正在保存动画到 {save_path}...")
            anim.save(save_path, writer='pillow', fps=5)
            print("动画保存完成！")
        
        plt.show()
        return anim

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='多智能体路径可视化工具')
    parser.add_argument('task_file', help='任务XML文件路径')
    parser.add_argument('--log_file', help='日志XML文件路径（可选）')
    parser.add_argument('--save', help='保存动画的文件路径（如 animation.gif）')
    parser.add_argument('--interval', type=int, default=200, 
                       help='动画帧间隔（毫秒），默认200')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.task_file):
        print(f"错误：任务文件 {args.task_file} 不存在")
        return
    
    try:
        # 解析任务文件
        print(f"正在解析任务文件: {args.task_file}")
        game_map, agents = XMLParser.parse_task_file(args.task_file)
        print(f"解析完成：地图大小 {game_map.width}x{game_map.height}，智能体数量 {len(agents)}")
        
        # 如果提供了日志文件，解析路径信息
        if args.log_file:
            if os.path.exists(args.log_file):
                print(f"正在解析日志文件: {args.log_file}")
                agents = XMLParser.parse_log_file(args.log_file, agents)
                print("日志文件解析完成")
            else:
                print(f"警告：日志文件 {args.log_file} 不存在，将只显示起点和终点")
        else:
            print("未提供日志文件，将只显示起点和终点")
        
        # 创建可视化
        visualizer = AgentVisualizer(game_map, agents)
        visualizer.create_animation(interval=args.interval, save_path=args.save)
        
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()