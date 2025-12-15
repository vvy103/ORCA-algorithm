#!/usr/bin/env python3
"""
类似Makefile的便捷构建脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_cmd(cmd, description=""):
    """运行命令"""
    if description:
        print(f"🔄 {description}")
    print(f"   执行: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 失败: {e}")
        return False

def target_clean():
    """清理编译文件"""
    print("🧹 清理编译文件...")
    
    patterns = ["build", "dist", "*.egg-info", "*.so", "*.pyd", "__pycache__"]
    
    for pattern in patterns:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   删除目录: {path}")
            elif path.is_file():
                path.unlink()
                print(f"   删除文件: {path}")

def target_build():
    """本地编译"""
    print("🔨 本地编译...")
    
    # 检查依赖
    try:
        import pybind11
        print(f"   ✅ pybind11: {pybind11.__version__}")
    except ImportError:
        print("   ❌ 需要安装: pip install pybind11")
        return False
    
    # 编译
    return run_cmd("python setup.py build_ext --inplace", "编译扩展模块")

def target_test():
    """测试模块"""
    print("🧪 测试模块...")
    
    # 检查模块文件
    module_files = list(Path('.').glob("orca_core*.so")) + list(Path('.').glob("orca_core*.pyd"))
    
    if not module_files:
        print("   ❌ 未找到模块文件，请先编译")
        return False
    
    # 测试导入
    test_code = '''
import sys
sys.path.insert(0, ".")
import orca_core

print("✅ 导入成功")
print("启用模块:", orca_core.get_enabled_modules())

# 基本测试
p = orca_core.Point(1, 2)
print("Point测试:", p)

params = orca_core.AgentParam()
print("AgentParam测试:", params.radius)

print("✅ 所有测试通过")
'''
    
    return run_cmd(f'python -c "{test_code}"', "运行基本测试")

def target_demo():
    """运行演示"""
    print("🎬 运行演示...")
    return run_cmd("python use_local.py --demo", "运行使用演示")

def target_interactive():
    """交互模式"""
    print("🔧 启动交互模式...")
    return run_cmd("python use_local.py --interactive", "启动交互模式")

def target_all():
    """完整构建流程"""
    print("🚀 完整构建流程...")
    
    steps = [
        ("清理", target_clean),
        ("编译", target_build), 
        ("测试", target_test),
        ("演示", target_demo)
    ]
    
    for name, func in steps:
        print(f"\n--- {name} ---")
        if not func():
            print(f"❌ {name}失败，停止构建")
            return False
    
    print("\n🎉 完整构建成功!")
    return True

def target_help():
    """显示帮助"""
    print("ORCA Python绑定 - 构建工具")
    print("=" * 30)
    print("用法: python make.py <target>")
    print()
    print("可用目标:")
    print("  clean       - 清理编译文件")
    print("  build       - 本地编译模块")
    print("  test        - 测试编译的模块")
    print("  demo        - 运行使用演示")
    print("  interactive - 启动交互模式")
    print("  all         - 完整构建流程 (clean + build + test + demo)")
    print("  help        - 显示此帮助")
    print()
    print("示例:")
    print("  python make.py build    # 只编译")
    print("  python make.py all      # 完整流程")
    print("  python make.py clean    # 清理文件")

def main():
    """主函数"""
    targets = {
        'clean': target_clean,
        'build': target_build,
        'test': target_test,
        'demo': target_demo,
        'interactive': target_interactive,
        'all': target_all,
        'help': target_help
    }
    
    if len(sys.argv) < 2:
        target = 'help'
    else:
        target = sys.argv[1].lower()
    
    if target not in targets:
        print(f"❌ 未知目标: {target}")
        target_help()
        return 1
    
    try:
        success = targets[target]()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
        return 1
    except Exception as e:
        print(f"💥 意外错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())