# 多智能体路径可视化工具

这个Python工具可以读取XML格式的地图和智能体轨迹数据，生成动态的可视化展示。

## 功能特性

- 📊 **地图可视化**：显示网格地图和多边形障碍物
- 🤖 **智能体动画**：实时显示多个智能体的移动轨迹
- 🎯 **起点终点**：清晰标记每个智能体的起始和目标位置
- 💾 **动画保存**：支持将动画保存为GIF文件
- 🎨 **颜色区分**：不同智能体使用不同颜色标识

## 安装依赖

```bash
pip install matplotlib numpy
```

## 使用方法

### 1. 命令行使用

```bash
# 基本用法：只显示起点和终点
python agent_visualization.py task_examples/empty_task.xml

# 包含路径轨迹的完整可视化
python agent_visualization.py task_examples/empty_task.xml --log_file task_examples/1_task_10_log.xml

# 保存动画为GIF文件
python agent_visualization.py task_examples/empty_task.xml --log_file task_examples/1_task_10_log.xml --save animation.gif

# 调整动画速度（毫秒）
python agent_visualization.py task_examples/empty_task.xml --log_file task_examples/1_task_10_log.xml --interval 100
```

### 2. 直接运行示例

```bash
python visualization_example.py
```

### 3. 在代码中使用

```python
from agent_visualization import XMLParser, AgentVisualizer

# 解析XML文件
game_map, agents = XMLParser.parse_task_file("task_file.xml")

# 如果有日志文件，加载路径数据
agents = XMLParser.parse_log_file("log_file.xml", agents)

# 创建可视化
visualizer = AgentVisualizer(game_map, agents)
anim = visualizer.create_animation(interval=200, save_path="output.gif")
```

## 文件格式说明

### 任务文件格式 (task.xml)
```xml
<root>
    <agents number="10" type="orca">
        <default_parameters size="0.3" movespeed="1" .../>
        <agent id="0" start.xr="37.5" start.yr="51.5" goal.xr="41.5" goal.yr="29.5"/>
        ...
    </agents>
    <map>
        <width>64</width>
        <height>64</height>
        <cellsize>1</cellsize>
        <grid>
            <row>0 0 0 1 1 0 0 ...</row>
            ...
        </grid>
    </map>
    <obstacles number="1">
        <obstacle>
            <vertex xr="0" yr="0"/>
            <vertex xr="0" yr="64"/>
            ...
        </obstacle>
    </obstacles>
</root>
```

### 日志文件格式 (log.xml)
```xml
<root>
    <!-- 包含任务文件的所有信息，plus: -->
    <agent number="0">
        <path pathfound="true" steps="4">
            <step number="0" x="33.18066" y="9.1728058"/>
            <step number="1" x="33.36132" y="9.3456116"/>
            ...
        </path>
    </agent>
    ...
</root>
```

## 可视化元素说明

- 🟢 **绿色圆点**：智能体起始位置
- 🔴 **红色方块**：智能体目标位置  
- 🔵 **彩色圆圈**：智能体当前位置（不同颜色区分不同智能体）
- 🔢 **圆圈内数字**：智能体ID编号
- ⬛ **黑色方块**：网格障碍物
- 🔘 **灰色多边形**：多边形障碍物

## 参数说明

- `task_file`: 必需，XML任务文件路径
- `--log_file`: 可选，XML日志文件路径（包含路径轨迹）
- `--save`: 可选，保存动画的文件路径（如 animation.gif）
- `--interval`: 可选，动画帧间隔（毫秒），默认200

## 注意事项

1. **坐标系转换**：XML文件中的坐标系原点在左下角，matplotlib的原点在左上角，程序会自动处理转换
2. **文件路径**：确保XML文件路径正确，支持相对路径和绝对路径
3. **内存使用**：大量智能体或长路径可能消耗较多内存
4. **动画保存**：保存GIF文件需要pillow库：`pip install pillow`

## 示例输出

运行后会显示一个matplotlib窗口，展示：
- 静态的地图、障碍物、起点和终点
- 动态的智能体移动动画
- 窗口标题显示当前步数

## 故障排除

1. **ImportError**: 安装缺失的依赖包
2. **FileNotFoundError**: 检查XML文件路径是否正确
3. **XML解析错误**: 确保XML文件格式正确
4. **动画不显示**: 检查matplotlib后端设置

## 扩展功能

可以根据需要扩展以下功能：
- 添加轨迹线显示
- 支持更多文件格式
- 添加交互式控制
- 性能优化
- 3D可视化支持