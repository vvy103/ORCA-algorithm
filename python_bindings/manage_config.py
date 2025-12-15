#!/usr/bin/env python3
"""
Configuration management script for ORCA Python bindings
配置管理脚本 - 用于动态修改编译配置
"""

import json
import os
import sys
from pathlib import Path

CONFIG_FILE = "config.json"

def load_config():
    """加载配置文件"""
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        print(f"❌ 配置文件 {CONFIG_FILE} 不存在")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return None

def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ 保存配置文件失败: {e}")
        return False

def show_current_config():
    """显示当前配置"""
    print("当前配置状态:")
    print("-" * 30)
    
    config = load_config()
    if not config:
        return
    
    modules = config.get('modules', {})
    for module_name, module_config in modules.items():
        status = "启用" if module_config.get('enabled', False) else "禁用"
        print(f"📦 {module_name}: {status}")
        
        if module_config.get('description'):
            print(f"   描述: {module_config['description']}")
        
        if module_config.get('classes'):
            classes = ', '.join(module_config['classes'])
            print(f"   类: {classes}")
        
        if module_config.get('functions'):
            functions = ', '.join(module_config['functions'])
            print(f"   函数: {functions}")
        print()

def toggle_module(module_name):
    """切换模块启用状态"""
    config = load_config()
    if not config:
        return False
    
    if module_name not in config.get('modules', {}):
        print(f"❌ 模块 '{module_name}' 不存在")
        available_modules = list(config.get('modules', {}).keys())
        print(f"可用模块: {available_modules}")
        return False
    
    current_status = config['modules'][module_name].get('enabled', False)
    new_status = not current_status
    
    config['modules'][module_name]['enabled'] = new_status
    
    if save_config(config):
        status_text = "启用" if new_status else "禁用"
        print(f"✅ 模块 '{module_name}' 已{status_text}")
        return True
    else:
        return False

def enable_module(module_name):
    """启用模块"""
    config = load_config()
    if not config:
        return False
    
    if module_name not in config.get('modules', {}):
        print(f"❌ 模块 '{module_name}' 不存在")
        return False
    
    config['modules'][module_name]['enabled'] = True
    
    if save_config(config):
        print(f"✅ 模块 '{module_name}' 已启用")
        return True
    else:
        return False

def disable_module(module_name):
    """禁用模块"""
    config = load_config()
    if not config:
        return False
    
    if module_name not in config.get('modules', {}):
        print(f"❌ 模块 '{module_name}' 不存在")
        return False
    
    config['modules'][module_name]['enabled'] = False
    
    if save_config(config):
        print(f"✅ 模块 '{module_name}' 已禁用")
        return True
    else:
        return False

def reset_to_defaults():
    """重置为默认配置"""
    default_config = {
        "modules": {
            "core": {
                "enabled": True,
                "description": "Core ORCA functionality",
                "classes": ["Point", "Agent", "Mission", "AgentParam"],
                "functions": ["create_agent", "run_simulation"]
            },
            "geometry": {
                "enabled": True,
                "description": "Geometric utilities",
                "classes": ["Point", "Node", "ObstacleSegment"],
                "functions": ["euclidean_distance", "point_operations"]
            },
            "experimental": {
                "enabled": False,
                "description": "Experimental features for testing",
                "classes": [],
                "functions": []
            }
        },
        "build_options": {
            "debug": False,
            "optimization_level": "O2",
            "include_full_logging": True
        }
    }
    
    if save_config(default_config):
        print("✅ 配置已重置为默认值")
        return True
    else:
        return False

def interactive_mode():
    """交互式配置模式"""
    print("🔧 ORCA配置管理 - 交互模式")
    print("=" * 40)
    
    while True:
        print("\n可用操作:")
        print("1. 显示当前配置 (show)")
        print("2. 启用模块 (enable <module>)")
        print("3. 禁用模块 (disable <module>)")
        print("4. 切换模块状态 (toggle <module>)")
        print("5. 重置为默认配置 (reset)")
        print("6. 退出 (quit)")
        
        try:
            command = input("\n请输入命令: ").strip().lower()
            
            if command == "quit" or command == "q":
                break
            elif command == "show" or command == "s":
                show_current_config()
            elif command == "reset" or command == "r":
                if input("确认重置配置? (y/N): ").lower() == 'y':
                    reset_to_defaults()
            elif command.startswith("enable "):
                module = command.split(" ", 1)[1]
                enable_module(module)
            elif command.startswith("disable "):
                module = command.split(" ", 1)[1]
                disable_module(module)
            elif command.startswith("toggle "):
                module = command.split(" ", 1)[1]
                toggle_module(module)
            else:
                print("❌ 未知命令")
                
        except KeyboardInterrupt:
            print("\n\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

def main():
    """主函数"""
    if len(sys.argv) == 1:
        # 无参数，显示当前配置
        show_current_config()
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_config()
    elif command == "interactive" or command == "i":
        interactive_mode()
    elif command == "reset":
        reset_to_defaults()
    elif command == "enable" and len(sys.argv) > 2:
        enable_module(sys.argv[2])
    elif command == "disable" and len(sys.argv) > 2:
        disable_module(sys.argv[2])
    elif command == "toggle" and len(sys.argv) > 2:
        toggle_module(sys.argv[2])
    else:
        print("ORCA配置管理工具")
        print("=" * 20)
        print("用法:")
        print("  python manage_config.py                    # 显示当前配置")
        print("  python manage_config.py show               # 显示当前配置")
        print("  python manage_config.py interactive        # 交互模式")
        print("  python manage_config.py enable <module>    # 启用模块")
        print("  python manage_config.py disable <module>   # 禁用模块")
        print("  python manage_config.py toggle <module>    # 切换模块状态")
        print("  python manage_config.py reset              # 重置为默认配置")
        print()
        print("可用模块: core, geometry, experimental")

if __name__ == "__main__":
    main()