#!/usr/bin/env python3
"""
Quick Start Script for ORCA Python Bindings
快速开始脚本 - 自动检查依赖、编译和测试
"""

import os
import sys
import subprocess
import platform

def print_header(title):
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)

def run_command(cmd, description=""):
    """运行命令并显示结果"""
    if description:
        print(f"\n🔄 {description}")
    print(f"执行: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {e}")
        if e.stderr:
            print(f"错误详情: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("需要Python 3.6或更高版本")
        return False

def check_compiler():
    """检查编译器"""
    system = platform.system()
    
    if system == "Windows":
        # 检查Visual Studio
        result = subprocess.run("cl", shell=True, capture_output=True)
        if result.returncode == 0 or "Microsoft" in result.stderr:
            print("✅ 找到Microsoft Visual C++编译器")
            return True
        else:
            print("❌ 未找到Visual C++编译器")
            print("请安装Visual Studio或Visual Studio Build Tools")
            return False
    else:
        # 检查g++或clang++
        for compiler in ["g++", "clang++"]:
            result = subprocess.run(f"{compiler} --version", shell=True, capture_output=True)
            if result.returncode == 0:
                print(f"✅ 找到编译器: {compiler}")
                return True
        
        print("❌ 未找到C++编译器")
        print("请安装g++或clang++")
        return False

def install_dependencies():
    """安装Python依赖"""
    print_header("安装Python依赖")
    
    dependencies = ["pybind11", "setuptools", "wheel"]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"安装 {dep}"):
            return False
    
    print("✅ 所有依赖安装完成")
    return True

def build_project():
    """编译项目"""
    print_header("编译ORCA Python绑定")
    
    # 清理之前的构建
    print("🧹 清理之前的构建文件...")
    cleanup_commands = [
        "rm -rf build dist *.egg-info",  # Linux/Mac
        "rmdir /s /q build dist 2>nul",  # Windows
        "del /q *.pyd 2>nul",  # Windows
        "rm -f *.so"  # Linux/Mac
    ]
    
    for cmd in cleanup_commands:
        subprocess.run(cmd, shell=True, capture_output=True)
    
    # 编译
    if run_command("pip install -e .", "编译并安装绑定"):
        print("✅ 编译成功!")
        return True
    else:
        print("❌ 编译失败")
        return False

def test_bindings():
    """测试绑定"""
    print_header("测试Python绑定")
    
    # 基本导入测试
    test_code = '''
import orca_core
print("✅ 成功导入 orca_core")
print("启用的模块:", orca_core.get_enabled_modules())

# 测试Point类
p1 = orca_core.Point(1.0, 2.0)
p2 = orca_core.Point(3.0, 4.0)
print(f"Point 1: {p1}")
print(f"Point 2: {p2}")

# 测试距离计算
distance = (p2 - p1).euclidean_norm()
print(f"距离: {distance:.2f}")

# 测试AgentParam
params = orca_core.AgentParam()
print(f"默认半径: {params.radius}")
print("✅ 所有基本测试通过!")
'''
    
    if run_command(f'python -c "{test_code}"', "运行基本功能测试"):
        print("✅ 测试通过!")
        return True
    else:
        print("❌ 测试失败")
        return False

def show_usage_examples():
    """显示使用示例"""
    print_header("使用示例")
    
    print("""
🎉 恭喜! ORCA Python绑定安装成功!

基本使用方法:

1. 导入模块:
   import orca_core

2. 创建几何对象:
   point = orca_core.Point(1.0, 2.0)
   
3. 设置Agent参数:
   params = orca_core.AgentParam()
   params.radius = 0.5
   params.max_speed = 2.0

4. 运行仿真 (需要XML配置文件):
   # result = orca_core.run_simulation("scenario.xml", num_agents=10)

📁 示例文件位置:
   - examples/basic_usage.py - 基本使用示例
   - examples/config_test.py - 配置系统测试

🔧 配置系统:
   - 编辑 config.json 来启用/禁用模块
   - 修改后重新运行: pip install -e .

📚 更多信息请查看 README.md
""")

def main():
    """主函数"""
    print_header("ORCA Python绑定 - 快速开始")
    
    # 检查系统要求
    if not check_python_version():
        return 1
    
    if not check_compiler():
        return 1
    
    # 安装依赖
    if not install_dependencies():
        return 1
    
    # 编译项目
    if not build_project():
        return 1
    
    # 测试
    if not test_bindings():
        return 1
    
    # 显示使用说明
    show_usage_examples()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 意外错误: {e}")
        sys.exit(1)