#!/usr/bin/env python3
"""
本地使用脚本 - 无需安装，直接使用编译好的模块
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径，这样可以直接导入编译好的模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_module():
    """检查模块是否存在"""
    # 查找编译好的模块文件
    module_files = []
    for ext in ['.so', '.pyd']:
        for file in current_dir.glob(f"orca_core*{ext}"):
            module_files.append(file)
    
    if not module_files:
        print("❌ 未找到编译好的模块文件")
        print("请先运行: python build_local.py")
        return False
    
    print("✅ 找到模块文件:")
    for file in module_files:
        print(f"   📦 {file.name}")
    return True

def demo_usage():
    """演示使用方法"""
    if not check_module():
        return
    
    try:
        # 导入模块
        import orca_core
        print("\n🎉 成功导入ORCA模块!")
        
        # 显示可用功能
        print(f"📦 模块版本: {getattr(orca_core, '__version__', '未知')}")
        print(f"🔧 启用的模块: {orca_core.get_enabled_modules()}")
        
        print("\n🧪 基本功能演示:")
        
        # 1. Point操作
        print("1. Point几何操作:")
        p1 = orca_core.Point(0.0, 0.0)
        p2 = orca_core.Point(3.0, 4.0)
        
        print(f"   Point 1: ({p1.x()}, {p1.y()})")
        print(f"   Point 2: ({p2.x()}, {p2.y()})")
        
        distance = (p2 - p1).euclidean_norm()
        print(f"   距离: {distance}")
        
        # 2. Agent参数
        print("\n2. Agent参数设置:")
        params = orca_core.AgentParam()
        print(f"   默认半径: {params.radius}")
        print(f"   默认最大速度: {params.max_speed}")
        
        params.radius = 0.5
        params.max_speed = 2.0
        print(f"   修改后半径: {params.radius}")
        print(f"   修改后最大速度: {params.max_speed}")
        
        # 3. Node操作
        print("\n3. Node网格操作:")
        node1 = orca_core.Node(0, 0)
        node2 = orca_core.Node(5, 5)
        print(f"   Node 1: ({node1.i}, {node1.j})")
        print(f"   Node 2: ({node2.i}, {node2.j})")
        
        print("\n✅ 所有基本功能正常!")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已经编译模块: python build_local.py")
    except Exception as e:
        print(f"❌ 运行错误: {e}")

def interactive_mode():
    """交互模式"""
    if not check_module():
        return
    
    try:
        import orca_core
        
        print("\n🔧 进入交互模式 (输入'quit'退出)")
        print("可用对象: orca_core, Point, AgentParam, Node")
        print("示例: p = orca_core.Point(1, 2)")
        
        # 导入到全局命名空间方便使用
        globals()['orca_core'] = orca_core
        globals()['Point'] = orca_core.Point
        globals()['AgentParam'] = orca_core.AgentParam
        globals()['Node'] = orca_core.Node
        
        while True:
            try:
                cmd = input(">>> ").strip()
                if cmd.lower() in ['quit', 'exit', 'q']:
                    break
                elif cmd:
                    result = eval(cmd)
                    if result is not None:
                        print(result)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"错误: {e}")
        
        print("👋 退出交互模式")
        
    except ImportError as e:
        print(f"❌ 无法进入交互模式: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ORCA本地使用工具")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--check", action="store_true", help="检查模块")
    
    args = parser.parse_args()
    
    if args.check:
        check_module()
    elif args.interactive:
        interactive_mode()
    elif args.demo:
        demo_usage()
    else:
        # 默认运行演示
        demo_usage()