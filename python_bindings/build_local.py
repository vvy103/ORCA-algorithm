#!/usr/bin/env python3
"""
本地编译脚本 - 不安装到Python环境，直接在当前目录生成模块
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def build_local():
    """本地编译，生成.so/.pyd文件到当前目录"""
    
    print("🔨 本地编译ORCA Python绑定")
    print("=" * 40)
    
    # 检查pybind11
    try:
        import pybind11
        print(f"✅ 找到pybind11: {pybind11.__version__}")
    except ImportError:
        print("❌ 需要安装pybind11: pip install pybind11")
        return False
    
    # 设置编译参数
    system = platform.system()
    
    if system == "Windows":
        # Windows编译命令
        compile_cmd = [
            "python", "setup.py", "build_ext", "--inplace"
        ]
    else:
        # Linux/Mac编译命令
        compile_cmd = [
            "python", "setup.py", "build_ext", "--inplace"
        ]
    
    print(f"🔧 编译命令: {' '.join(compile_cmd)}")
    
    try:
        # 执行编译
        result = subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
        
        if result.stdout:
            print("编译输出:")
            print(result.stdout)
        
        # 检查生成的文件
        generated_files = []
        for ext in ['.so', '.pyd']:
            for file in Path('.').glob(f"*{ext}"):
                generated_files.append(file)
        
        if generated_files:
            print("✅ 编译成功! 生成的文件:")
            for file in generated_files:
                print(f"   📦 {file}")
            
            # 测试导入
            print("\n🧪 测试导入...")
            test_import()
            return True
        else:
            print("❌ 编译完成但未找到生成的模块文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 编译失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False

def test_import():
    """测试本地导入"""
    try:
        # 添加当前目录到Python路径
        sys.path.insert(0, '.')
        
        import orca_core
        print("✅ 成功导入orca_core")
        
        # 简单测试
        point = orca_core.Point(1.0, 2.0)
        print(f"✅ 创建Point成功: {point}")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def clean_build():
    """清理编译文件"""
    print("🧹 清理编译文件...")
    
    patterns = [
        "build/",
        "*.so",
        "*.pyd", 
        "*.egg-info/",
        "__pycache__/",
        "*.pyc"
    ]
    
    for pattern in patterns:
        if pattern.endswith('/'):
            # 目录
            for path in Path('.').glob(pattern):
                if path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    print(f"   删除目录: {path}")
        else:
            # 文件
            for path in Path('.').glob(pattern):
                if path.is_file():
                    path.unlink()
                    print(f"   删除文件: {path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ORCA本地编译工具")
    parser.add_argument("--clean", action="store_true", help="清理编译文件")
    parser.add_argument("--test", action="store_true", help="只测试导入")
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
    elif args.test:
        test_import()
    else:
        # 默认编译
        success = build_local()
        if not success:
            sys.exit(1)