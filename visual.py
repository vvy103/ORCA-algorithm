#!/usr/bin/env python3
"""
ORCA Algorithm Visualization Script
动态展示多智能体路径规划的可视化工具

使用方法:
python visual.py task_examples/e_task_10_log.xml

功能:
- 显示地图和障碍物
- 显示智能体的起点、终点和实时位置
- 动态播放智能体移动过程
- 支持暂停/继续、速度调节等控制
"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import numpy as np
import argparse
import sys
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors

class ORCAVisualizer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.agents = {}
        self.obstacles = []
        self.map_data = {}
        self.grid = []
        self.agent_paths = {}
        self.max_steps = 0
        
        # 可视化参数
        self.agent_radius = 0.3  # 智能体半径
        self.colors = plt.cm.tab10(np.linspace(0, 1, 10))  # 智能体颜色
        
        # 动画控制
        self.current_step = 0
        self.is_paused = False
        self.animation_speed = 100  # 毫秒
        self.slider = None
        self.animation = None
        
        self.parse_log_file()
        self.setup_plot()
    
    def parse_log_file(self):
        """解析XML日志文件"""
        try:
            tree = ET.parse(self.log_file)
            root = tree.getroot()
            
            # 解析智能体信息
            agents_elem = root.find('agents')
            if agents_elem is not None:
                for agent_elem in agents_elem.findall('agent'):
                    agent_id = int(agent_elem.get('id'))
                    start_x = float(agent_elem.get('start.xr'))
                    start_y = float(agent_elem.get('start.yr'))
                    goal_x = float(agent_elem.get('goal.xr'))
                    goal_y = float(agent_elem.get('goal.yr'))
                    
                    self.agents[agent_id] = {
                        'start': (start_x, start_y),
                        'goal': (goal_x, goal_y),
                        'color': self.colors[agent_id % len(self.colors)]
                    }
            
            # 解析障碍物信息
            obstacles_elem = root.find('obstacles')
            if obstacles_elem is not None:
                for obstacle_elem in obstacles_elem.findall('obstacle'):
                    vertices = []
                    for vertex_elem in obstacle_elem.findall('vertex'):
                        x = float(vertex_elem.get('xr'))
                        y = float(vertex_elem.get('yr'))
                        vertices.append((x, y))
                    if vertices:
                        self.obstacles.append(vertices)
            
            # 解析地图信息
            map_elem = root.find('map')
            if map_elem is not None:
                self.map_data['width'] = int(map_elem.find('width').text)
                self.map_data['height'] = int(map_elem.find('height').text)
                self.map_data['cellsize'] = float(map_elem.find('cellsize').text)
                
                # 解析网格数据
                grid_elem = map_elem.find('grid')
                if grid_elem is not None:
                    for row_elem in grid_elem.findall('row'):
                        row_data = [int(x) for x in row_elem.text.split()]
                        self.grid.append(row_data)
            
            # 解析智能体路径
            log_elem = root.find('log')
            if log_elem is not None:
                for agent_elem in log_elem.findall('agent'):
                    agent_id = int(agent_elem.get('id'))
                    path_elem = agent_elem.find('path')
                    
                    if path_elem is not None:
                        pathfound = path_elem.get('pathfound') == 'true'
                        steps = []
                        for step_elem in path_elem.findall('step'):
                            step_num = int(step_elem.get('number'))
                            x = float(step_elem.get('xr'))
                            y = float(step_elem.get('yr'))
                            steps.append((step_num, x, y))
                        
                        # 无论pathfound是true还是false，只要有steps数据就使用
                        if steps:
                            self.agent_paths[agent_id] = sorted(steps, key=lambda x: x[0])
                            self.max_steps = max(self.max_steps, max(step[0] for step in steps))
                        # 只有在完全没有steps数据时才使用起始位置
                        elif agent_id in self.agents:
                            start_x, start_y = self.agents[agent_id]['start']
                            self.agent_paths[agent_id] = [(0, start_x, start_y)]
                            self.max_steps = max(self.max_steps, 10)  # 设置最小步数用于显示
            
            # 统计成功找到路径的智能体数量
            successful_agents = 0
            if log_elem is not None:
                for agent_elem in log_elem.findall('agent'):
                    path_elem = agent_elem.find('path')
                    if path_elem is not None and path_elem.get('pathfound') == 'true':
                        successful_agents += 1
            
            print(f"Parsing complete: {len(self.agents)} agents, {successful_agents} successful paths, {len(self.obstacles)} obstacles, max steps: {self.max_steps}")
            if successful_agents == 0:
                print("WARNING: No agents reached their goals successfully!")
                if self.max_steps > 10:
                    print("However, agents did move and their trajectories will be displayed.")
                else:
                    print("Agents will be shown at their starting positions.")
                print("This might indicate:")
                print("  - Algorithm failed to find complete paths to goals")
                print("  - Map configuration issues or unreachable goals")
                print("  - Time limit reached before reaching goals")
            
        except Exception as e:
            print(f"Error parsing XML file: {e}")
            sys.exit(1)
    
    def setup_plot(self):
        """设置绘图环境"""
        # 创建图形和子图，为进度条留出空间
        self.fig = plt.figure(figsize=(12, 11))
        self.ax = plt.subplot(111)
        
        # 调整子图位置，为进度条留出空间
        plt.subplots_adjust(bottom=0.15)
        
        self.ax.set_xlim(-2, self.map_data['width'] + 2)
        self.ax.set_ylim(-2, self.map_data['height'] + 2)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('ORCA Algorithm Visualization', fontsize=16, fontweight='bold')
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        
        # 绘制网格地图（障碍物）
        self.draw_grid_map()
        
        # 绘制障碍物边界
        self.draw_obstacles()
        
        # 绘制智能体起点和终点
        self.draw_start_goal_points()
        
        # 初始化智能体圆圈
        self.agent_circles = {}
        self.agent_trails = {}
        for agent_id in self.agents:
            # 智能体圆圈
            circle = plt.Circle((0, 0), self.agent_radius, 
                              color=self.agents[agent_id]['color'], 
                              alpha=0.7, zorder=5)
            self.ax.add_patch(circle)
            self.agent_circles[agent_id] = circle
            
            # 智能体轨迹
            trail_line, = self.ax.plot([], [], '--', 
                                     color=self.agents[agent_id]['color'], 
                                     alpha=0.5, linewidth=1, zorder=3)
            self.agent_trails[agent_id] = trail_line
        
        # 添加时间步显示
        self.time_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                    fontsize=12, verticalalignment='top',
                                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 添加控制说明
        control_text = "Controls: Space=Pause/Resume, Drag slider to navigate"
        self.ax.text(0.02, 0.02, control_text, transform=self.ax.transAxes, 
                    fontsize=10, verticalalignment='bottom',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # 创建进度条滑块
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        self.slider = Slider(slider_ax, 'Progress', 0, self.max_steps, 
                           valinit=0, valfmt='%d', valstep=1)
        self.slider.on_changed(self.on_slider_change)
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
    
    def draw_grid_map(self):
        """绘制网格地图"""
        if not self.grid:
            return
            
        height = len(self.grid)
        width = len(self.grid[0]) if height > 0 else 0
        
        # 创建障碍物网格图像
        grid_array = np.array(self.grid)
        
        # 使用imshow显示网格，1为障碍物（黑色），0为自由空间（白色）
        self.ax.imshow(grid_array, cmap='gray_r', alpha=0.3, 
                      extent=[0, width, 0, height], origin='lower', zorder=1)
        
        # 绘制网格线
        self.draw_grid_lines(width, height)
    
    def draw_grid_lines(self, width, height):
        """绘制网格线显示每个格子"""
        # 绘制垂直线
        for i in range(width + 1):
            self.ax.axvline(x=i, color='lightgray', linewidth=0.5, alpha=0.7, zorder=0)
        
        # 绘制水平线
        for j in range(height + 1):
            self.ax.axhline(y=j, color='lightgray', linewidth=0.5, alpha=0.7, zorder=0)
    
    def draw_obstacles(self):
        """绘制障碍物边界"""
        for vertices in self.obstacles:
            if len(vertices) >= 3:
                # 创建多边形障碍物
                polygon = Polygon(vertices, closed=True, 
                                fill=False, edgecolor='red', 
                                linewidth=2, zorder=2)
                self.ax.add_patch(polygon)
    
    def draw_start_goal_points(self):
        """绘制智能体的起点和终点"""
        for agent_id, agent_info in self.agents.items():
            color = agent_info['color']
            start_x, start_y = agent_info['start']
            goal_x, goal_y = agent_info['goal']
            
            # 起点 (方形)
            start_marker = patches.Rectangle((start_x - 0.2, start_y - 0.2), 0.4, 0.4,
                                           facecolor=color, edgecolor='black', 
                                           linewidth=1, alpha=0.8, zorder=4)
            self.ax.add_patch(start_marker)
            
            # 终点 (星形)
            self.ax.scatter(goal_x, goal_y, s=100, c=[color], marker='*', 
                          edgecolors='black', linewidth=1, alpha=0.8, zorder=4)
            
            # 添加智能体ID标签
            self.ax.text(start_x, start_y - 0.5, f'A{agent_id}', 
                        ha='center', va='top', fontsize=8, fontweight='bold')
    
    def get_agent_position(self, agent_id, step):
        """获取指定步数时智能体的位置"""
        if agent_id not in self.agent_paths:
            return self.agents[agent_id]['start']
        
        path = self.agent_paths[agent_id]
        if not path:
            return self.agents[agent_id]['start']
        
        # 找到对应步数的位置
        for i, (step_num, x, y) in enumerate(path):
            if step_num >= step:
                if i == 0 or step_num == step:
                    return (x, y)
                else:
                    # 线性插值
                    prev_step, prev_x, prev_y = path[i-1]
                    ratio = (step - prev_step) / (step_num - prev_step)
                    interp_x = prev_x + ratio * (x - prev_x)
                    interp_y = prev_y + ratio * (y - prev_y)
                    return (interp_x, interp_y)
        
        # 如果步数超过路径长度，返回最后一个位置
        return (path[-1][1], path[-1][2])
    
    def get_agent_trail(self, agent_id, step):
        """获取智能体到指定步数的轨迹"""
        if agent_id not in self.agent_paths:
            return [], []
        
        path = self.agent_paths[agent_id]
        if not path:
            return [], []
        
        trail_x, trail_y = [], []
        for step_num, x, y in path:
            if step_num <= step:
                trail_x.append(x)
                trail_y.append(y)
            else:
                break
        
        return trail_x, trail_y
    
    def update_frame(self, frame):
        """更新动画帧"""
        if self.is_paused:
            return []
        
        self.current_step = frame
        self.update_visualization()
        
        # 更新滑块位置（不触发回调）
        self.slider.set_val(self.current_step)
        
        return list(self.agent_circles.values()) + list(self.agent_trails.values()) + [self.time_text]
    
    def update_visualization(self):
        """更新可视化显示"""
        # 更新时间显示
        self.time_text.set_text(f'Step: {self.current_step}/{self.max_steps}\n'
                               f'Time: {self.current_step * 0.1:.1f}s')
        
        # 更新每个智能体的位置和轨迹
        for agent_id in self.agents:
            # 更新位置
            x, y = self.get_agent_position(agent_id, self.current_step)
            self.agent_circles[agent_id].center = (x, y)
            
            # 更新轨迹
            trail_x, trail_y = self.get_agent_trail(agent_id, self.current_step)
            self.agent_trails[agent_id].set_data(trail_x, trail_y)
        
        # 刷新画布
        self.fig.canvas.draw_idle()
    
    def on_slider_change(self, val):
        """滑块值改变时的回调函数"""
        self.current_step = int(val)
        self.update_visualization()
    
    def on_key_press(self, event):
        """处理键盘事件"""
        if event.key == ' ':  # 空格键暂停/继续
            self.is_paused = not self.is_paused
            print("Animation", "Paused" if self.is_paused else "Resumed")
    
    def start_animation(self):
        """开始动画"""
        print("Starting animation...")
        print("Controls:")
        print("  Space: Pause/Resume")
        print("  Drag slider: Navigate to specific time")
        
        self.animation = FuncAnimation(
            self.fig, self.update_frame, 
            frames=range(self.max_steps + 1),
            interval=self.animation_speed,
            blit=False, repeat=True
        )
        
        plt.tight_layout()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='ORCA Algorithm Visualization')
    parser.add_argument('log_file', help='Path to the XML log file')
    
    args = parser.parse_args()
    
    print(f"Loading log file: {args.log_file}")
    
    try:
        visualizer = ORCAVisualizer(args.log_file)
        visualizer.start_animation()
    except KeyboardInterrupt:
        print("\nAnimation stopped")
    except Exception as e:
        print(f"Runtime error: {e}")

if __name__ == "__main__":
    main()