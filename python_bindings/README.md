# ORCA Algorithm Python Bindings

这是一个灵活的Python绑定项目，用于将ORCA（Optimal Reciprocal Collision Avoidance）C++库包装成Python模块。

## 项目结构

```
python_bindings/
├── config.json              # 动态配置文件 - 控制哪些模块被编译
├── setup.py                 # Python打包配置
├── CMakeLists.txt           # CMake构建配置
├── main_binding.cpp         # 主绑定文件 - 根据配置组合模块
├── core/                    # 核心功能模块
│   ├── __init__.py
│   ├── geometry_bindings.cpp    # 几何类绑定 (Point, Node, etc.)
│   ├── agent_bindings.cpp       # Agent相关绑定
│   └── mission_bindings.cpp     # Mission和仿真绑定
├── experimental/            # 实验性功能
│   ├── __init__.py
│   └── new_features.cpp         # 新功能测试
└── README.md               # 本文件
```

## 动态配置系统

通过修改 `config.json` 文件，你可以控制哪些功能被编译到Python模块中：

```json
{
  "modules": {
    "core": {
      "enabled": true,
      "description": "Core ORCA functionality", 
      "classes": ["Point", "Agent", "Mission", "AgentParam"],
      "functions": ["create_agent", "run_simulation"]
    },
    "geometry": {
      "enabled": true,
      "description": "Geometric utilities",
      "classes": ["Point", "Node", "ObstacleSegment"],
      "functions": ["euclidean_distance", "point_operations"]
    },
    "experimental": {
      "enabled": false,
      "description": "Experimental features for testing",
      "classes": [],
      "functions": []
    }
  }
}
```

## 环境要求

### 必需依赖
- **Python 3.6+** 
- **C++14兼容编译器** (gcc/clang/MSVC)
- **pybind11** - Python绑定库

### 安装pybind11
```bash
pip install pybind11
```

### C++编译器安装

**Windows:**
- Visual Studio 2019/2022 (包含C++工具)
- 或 Visual Studio Build Tools

**Linux:**
```bash
sudo apt-get install build-essential
```

**macOS:**
```bash
xcode-select --install
```

## 🚀 快速开始 (本地编译，无需安装)

### 方法1: 一键构建 (推荐)

```bash
# 进入绑定目录
cd ORCA-algorithm/python_bindings

# 完整构建流程 (清理 + 编译 + 测试 + 演示)
python make.py all
```

### 方法2: 分步构建

```bash
cd ORCA-algorithm/python_bindings

# 1. 清理之前的编译文件
python make.py clean

# 2. 本地编译 (生成.so/.pyd文件到当前目录)
python make.py build

# 3. 测试编译结果
python make.py test

# 4. 运行使用演示
python make.py demo
```

### 方法3: 直接编译

```bash
cd ORCA-algorithm/python_bindings

# 使用setup.py本地编译
python setup.py build_ext --inplace

# 或使用专用脚本
python build_local.py
```

## 📖 使用方法

### 快速体验

```bash
# 编译完成后，直接运行演示
python use_local.py --demo

# 或进入交互模式
python use_local.py --interactive
```

### Python代码使用

```python
# 方式1: 使用便捷脚本
# 运行: python use_local.py
# 然后按提示操作

# 方式2: 直接在Python中使用
import sys
sys.path.insert(0, '.')  # 添加当前目录到路径
import orca_core

# 检查启用的模块
print("启用的模块:", orca_core.get_enabled_modules())

# 创建几何对象
point1 = orca_core.Point(1.0, 2.0)
point2 = orca_core.Point(3.0, 4.0)

# 计算距离
distance = (point2 - point1).euclidean_norm()
print(f"距离: {distance}")

# 创建Agent参数
params = orca_core.AgentParam()
params.radius = 0.5
params.max_speed = 2.0
params.sight_radius = 5.0

print(f"Agent半径: {params.radius}")
print(f"最大速度: {params.max_speed}")

# 网格节点操作
node1 = orca_core.Node(0, 0)
node2 = orca_core.Node(5, 5)
print(f"节点1: ({node1.i}, {node1.j})")
print(f"节点2: ({node2.i}, {node2.j})")
```

### 在自己的项目中使用

```python
# your_project.py
import sys
import os

# 添加ORCA绑定路径
orca_path = "path/to/ORCA-algorithm/python_bindings"
sys.path.insert(0, orca_path)

import orca_core

# 现在可以使用ORCA功能了
def your_pathfinding_function():
    # 创建Agent参数
    params = orca_core.AgentParam()
    params.radius = 0.3
    params.max_speed = 1.5
    
    # 创建起点和终点
    start = orca_core.Point(0.0, 0.0)
    goal = orca_core.Point(10.0, 10.0)
    
    # 你的路径规划逻辑...
    return start, goal, params
```

## 🔄 开发工作流程

### 日常开发流程

```bash
# 1. 修改C++绑定代码
# 编辑 core/*.cpp 或 experimental/*.cpp

# 2. 重新编译
python make.py build

# 3. 测试功能
python make.py test
# 或
python use_local.py --demo

# 4. 使用新功能
python use_local.py --interactive
```

### 添加新功能的步骤

1. **实验阶段**: 在 `experimental/new_features.cpp` 中添加新绑定
2. **启用实验模块**: 修改 `config.json` 设置 `"experimental": {"enabled": true}`
3. **重新编译**: `python make.py build`
4. **测试功能**: `python make.py test`

### 稳定化功能

1. **移动到核心**: 将稳定的绑定从 `experimental/` 移动到 `core/`
2. **更新配置**: 在 `config.json` 中更新相应模块
3. **重新编译**: `python make.py build`

### 模块化开发指南

- **几何功能** → `core/geometry_bindings.cpp`
- **Agent功能** → `core/agent_bindings.cpp`  
- **仿真功能** → `core/mission_bindings.cpp`
- **新功能测试** → `experimental/new_features.cpp`

## 🔧 故障排除

### 编译问题

**找不到pybind11**
```bash
pip install pybind11
```

**编译器错误**
- Windows: 安装 Visual Studio Build Tools
- Linux: `sudo apt-get install build-essential`
- macOS: `xcode-select --install`

**找不到头文件**
```bash
# 检查路径是否正确
ls ../include/agent.h
ls ../src/agent.cpp
```

### 运行时问题

**导入失败**
```bash
# 检查是否有编译产物
ls orca_core*.so orca_core*.pyd

# 如果没有，重新编译
python make.py build
```

**函数不存在**
```bash
# 检查启用的模块
python manage_config.py show

# 启用需要的模块
python manage_config.py enable core
python make.py build
```

### 常见错误解决

**"No module named 'orca_core'"**
```python
# 确保添加了路径
import sys
sys.path.insert(0, '.')
import orca_core
```

**编译很慢**
```bash
# 使用并行编译
python setup.py build_ext --inplace -j4
```

**模块功能不完整**
```bash
# 检查配置并重新编译
python manage_config.py show
python make.py clean
python make.py build
```

## 扩展指南

### 添加新的C++类绑定

1. 在相应的 `*_bindings.cpp` 文件中添加:
```cpp
py::class_<YourClass>(m, "YourClass")
    .def(py::init<>())
    .def("method_name", &YourClass::method_name)
    .def_readwrite("property", &YourClass::property);
```

2. 更新 `config.json` 中的类列表

3. 重新编译和测试

### 添加新的模块

1. 创建新目录和绑定文件
2. 在 `main_binding.cpp` 中添加绑定函数声明和调用
3. 更新 `config.json` 添加新模块配置
4. 更新 `setup.py` 和 `CMakeLists.txt` 包含新文件

## 🧪 测试和验证

### 快速测试
```bash
# 基本功能测试
python make.py test

# 完整测试套件
python test_all.py
```

### 交互式测试
```bash
# 进入交互模式，直接测试功能
python use_local.py --interactive

# 在交互模式中可以直接使用:
# >>> p = Point(1, 2)
# >>> print(p)
# >>> params = AgentParam()
# >>> params.radius = 0.5
```

### 配置管理

```bash
# 显示当前配置
python manage_config.py

# 交互式配置管理
python manage_config.py interactive

# 启用/禁用模块
python manage_config.py enable experimental
python manage_config.py disable geometry

# 重置为默认配置
python manage_config.py reset
```

## 📁 项目文件说明

```
python_bindings/
├── 📋 README.md              # 本文档
├── ⚙️  config.json            # 动态配置文件
├── 🔨 make.py                # 类Makefile构建工具 (推荐)
├── 🏗️  build_local.py         # 本地编译脚本
├── 🎮 use_local.py           # 本地使用和演示脚本
├── 🧪 test_all.py            # 完整测试套件
├── 🔧 manage_config.py       # 配置管理工具
├── 📦 setup.py               # Python打包配置
├── 🏗️  CMakeLists.txt         # CMake构建配置 (可选)
├── 🔗 main_binding.cpp       # 主绑定文件
├── core/                     # 核心功能模块
│   ├── __init__.py           # Python包初始化
│   ├── geometry_bindings.cpp # 几何类绑定
│   ├── agent_bindings.cpp    # Agent相关绑定
│   └── mission_bindings.cpp  # Mission和仿真绑定
├── experimental/             # 实验性功能
│   ├── __init__.py           # Python包初始化
│   └── new_features.cpp      # 新功能测试
└── examples/                 # 使用示例
    ├── basic_usage.py        # 基本使用示例
    └── config_test.py        # 配置系统测试
```

## 🎯 常用命令速查

### 构建相关
```bash
python make.py all          # 完整构建 (推荐新用户)
python make.py build        # 只编译
python make.py clean        # 清理文件
python make.py test         # 测试功能
```

### 使用相关
```bash
python use_local.py --demo        # 运行演示
python use_local.py --interactive # 交互模式
python use_local.py --check       # 检查模块状态
```

### 配置相关
```bash
python manage_config.py show              # 显示配置
python manage_config.py toggle core       # 切换模块
python manage_config.py interactive       # 交互配置
```

## 🚀 推荐工作流程

### 新用户首次使用
```bash
cd ORCA-algorithm/python_bindings
python make.py all                    # 一键完成所有步骤
python use_local.py --interactive     # 体验功能
```

### 日常开发
```bash
# 修改绑定代码后
python make.py build                  # 重新编译
python use_local.py --demo           # 快速测试

# 或者
python make.py test                   # 运行测试套件
```

### 添加新功能
```bash
# 1. 编辑 experimental/new_features.cpp
# 2. 启用实验模块
python manage_config.py enable experimental

# 3. 编译测试
python make.py build
python make.py test

# 4. 稳定后移动到 core/ 目录
```

## 常见问题解决

### 编译错误
- **找不到pybind11**: `pip install pybind11`
- **编译器错误**: 确保安装了C++14兼容的编译器
- **链接错误**: 检查tinyxml2依赖是否正确

### 运行时错误
- **导入失败**: 确保编译成功，检查Python路径
- **函数不存在**: 检查config.json中模块是否启用
- **参数错误**: 查看绑定代码中的参数定义

### 性能问题
- **编译慢**: 使用 `pip install .` 而不是 `-e` 进行发布版本编译
- **运行慢**: 检查是否启用了优化选项

## 版本信息

- 📦 当前版本: 0.1.0
- 🐍 Python要求: >= 3.6
- ⚙️ C++标准: C++14 (匹配原项目)
- 📚 依赖: pybind11 >= 2.6.0

## 许可证

遵循原ORCA项目的许可证。

---

## 🎉 总结

你现在拥有一个**本地化、模块化**的ORCA Python绑定系统！

### ✨ 核心特性
- 🏠 **本地编译**: 无需安装到Python环境，所有文件在项目目录
- 🔧 **灵活配置**: 通过config.json动态控制编译内容  
- 🚀 **一键构建**: `python make.py all` 完成所有步骤
- 🧪 **渐进开发**: 从实验功能到稳定功能的清晰路径
- 🎮 **便捷使用**: 交互模式和演示脚本
- 📊 **完整测试**: 自动化测试确保代码质量

### 🚀 立即开始
```bash
cd ORCA-algorithm/python_bindings
python make.py all                    # 一键构建
python use_local.py --interactive     # 开始使用
```

### 🤖 开始你的多智能体路径规划之旅！

现在你可以：
- 🛤️ 实现复杂的多智能体路径规划
- 🚫 避免智能体间的碰撞
- ⚡ 高效的ORCA算法计算
- 🔄 动态调整算法参数
- 📈 分析仿真结果和性能

Happy coding! 🎯