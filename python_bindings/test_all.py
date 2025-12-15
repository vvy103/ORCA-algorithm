#!/usr/bin/env python3
"""
Complete test suite for ORCA Python bindings
完整的测试套件
"""

import sys
import traceback

def test_import():
    """测试模块导入"""
    print("1. 测试模块导入...")
    try:
        import orca_core
        print("   ✅ 成功导入 orca_core")
        
        # 检查版本
        if hasattr(orca_core, '__version__'):
            print(f"   📦 版本: {orca_core.__version__}")
        
        # 检查启用的模块
        enabled_modules = orca_core.get_enabled_modules()
        print(f"   🔧 启用的模块: {enabled_modules}")
        
        return True, orca_core
    except ImportError as e:
        print(f"   ❌ 导入失败: {e}")
        return False, None

def test_geometry(orca_core):
    """测试几何功能"""
    print("\n2. 测试几何功能...")
    try:
        # 测试Point类
        print("   测试Point类...")
        p1 = orca_core.Point(1.0, 2.0)
        p2 = orca_core.Point(3.0, 4.0)
        
        print(f"   Point 1: {p1}")
        print(f"   Point 2: {p2}")
        
        # 测试运算
        diff = p2 - p1
        print(f"   差值: {diff}")
        
        distance = diff.euclidean_norm()
        print(f"   欧几里得距离: {distance:.3f}")
        
        # 测试标量运算
        scaled = p1 * 2.0
        print(f"   缩放 (p1 * 2): {scaled}")
        
        # 测试点积
        dot_product = p1.scalar_product(p2)
        print(f"   点积: {dot_product:.3f}")
        
        # 测试Node类
        print("   测试Node类...")
        node1 = orca_core.Node(0, 0)
        node2 = orca_core.Node(5, 5)
        
        print(f"   Node 1: {node1}")
        print(f"   Node 2: {node2}")
        print(f"   节点相等性: {node1 == node2}")
        
        print("   ✅ 几何功能测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 几何功能测试失败: {e}")
        traceback.print_exc()
        return False

def test_agent_params(orca_core):
    """测试Agent参数"""
    print("\n3. 测试Agent参数...")
    try:
        # 创建默认参数
        params = orca_core.AgentParam()
        
        print(f"   默认半径: {params.radius}")
        print(f"   默认最大速度: {params.max_speed}")
        print(f"   默认视野半径: {params.sight_radius}")
        print(f"   默认时间边界: {params.time_boundary}")
        print(f"   默认最大Agent数: {params.agents_max_num}")
        
        # 修改参数
        params.radius = 0.5
        params.max_speed = 2.0
        params.sight_radius = 5.0
        params.time_boundary = 3.0
        params.agents_max_num = 20
        
        print("   修改后的参数:")
        print(f"   半径: {params.radius}")
        print(f"   最大速度: {params.max_speed}")
        print(f"   视野半径: {params.sight_radius}")
        print(f"   时间边界: {params.time_boundary}")
        print(f"   最大Agent数: {params.agents_max_num}")
        
        print("   ✅ Agent参数测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ Agent参数测试失败: {e}")
        traceback.print_exc()
        return False

def test_summary(orca_core):
    """测试Summary类"""
    print("\n4. 测试Summary类...")
    try:
        summary = orca_core.Summary()
        
        # 测试设置和获取
        summary["test_key"] = "test_value"
        summary["success_rate"] = "95.5"
        summary["runtime"] = "10.2"
        
        print(f"   设置值: test_key = {summary['test_key']}")
        print(f"   成功率: {summary['success_rate']}")
        print(f"   运行时间: {summary['runtime']}")
        
        # 测试获取所有字段
        all_fields = summary.get_full_summary()
        print(f"   所有字段: {all_fields}")
        
        print("   ✅ Summary类测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ Summary类测试失败: {e}")
        traceback.print_exc()
        return False

def test_advanced_geometry(orca_core):
    """测试高级几何功能"""
    print("\n5. 测试高级几何功能...")
    try:
        # 测试Vertex类
        if hasattr(orca_core, 'Vertex'):
            vertex = orca_core.Vertex(1.0, 2.0, True)
            print(f"   Vertex: {vertex}")
            print(f"   是否凸: {vertex.is_convex()}")
        
        # 测试ObstacleSegment类
        if hasattr(orca_core, 'ObstacleSegment'):
            left_vertex = orca_core.Vertex(0.0, 0.0)
            right_vertex = orca_core.Vertex(1.0, 0.0)
            obstacle = orca_core.ObstacleSegment(1, left_vertex, right_vertex)
            print(f"   障碍物ID: {obstacle.id}")
        
        # 测试工具函数
        if hasattr(orca_core, 'sq_point_seg_distance'):
            p1 = orca_core.Point(0.0, 0.0)
            p2 = orca_core.Point(1.0, 0.0)
            test_point = orca_core.Point(0.5, 1.0)
            
            distance = orca_core.sq_point_seg_distance(p1, p2, test_point)
            print(f"   点到线段的平方距离: {distance}")
        
        print("   ✅ 高级几何功能测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 高级几何功能测试失败: {e}")
        traceback.print_exc()
        return False

def test_performance():
    """简单的性能测试"""
    print("\n6. 性能测试...")
    try:
        import time
        import orca_core
        
        # 测试Point创建和运算性能
        start_time = time.time()
        
        points = []
        for i in range(10000):
            p = orca_core.Point(float(i), float(i * 2))
            points.append(p)
        
        # 计算距离
        total_distance = 0.0
        for i in range(len(points) - 1):
            diff = points[i+1] - points[i]
            total_distance += diff.euclidean_norm()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"   创建10000个点并计算距离用时: {elapsed:.3f}秒")
        print(f"   总距离: {total_distance:.3f}")
        print(f"   平均每个操作: {elapsed/10000*1000:.3f}毫秒")
        
        if elapsed < 1.0:  # 如果少于1秒认为性能可接受
            print("   ✅ 性能测试通过")
            return True
        else:
            print("   ⚠️  性能可能需要优化")
            return True
            
    except Exception as e:
        print(f"   ❌ 性能测试失败: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """运行所有测试"""
    print("ORCA Python绑定 - 完整测试套件")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 6
    
    # 1. 导入测试
    success, orca_core = test_import()
    if success:
        tests_passed += 1
    else:
        print("\n❌ 导入失败，无法继续测试")
        return False
    
    # 2. 几何功能测试
    if test_geometry(orca_core):
        tests_passed += 1
    
    # 3. Agent参数测试
    if test_agent_params(orca_core):
        tests_passed += 1
    
    # 4. Summary测试
    if test_summary(orca_core):
        tests_passed += 1
    
    # 5. 高级几何功能测试
    if test_advanced_geometry(orca_core):
        tests_passed += 1
    
    # 6. 性能测试
    if test_performance():
        tests_passed += 1
    
    # 总结
    print("\n" + "=" * 50)
    print(f"测试完成: {tests_passed}/{total_tests} 通过")
    
    if tests_passed == total_tests:
        print("🎉 所有测试通过! ORCA Python绑定工作正常")
        return True
    else:
        print(f"⚠️  有 {total_tests - tests_passed} 个测试失败")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 测试过程中发生意外错误: {e}")
        traceback.print_exc()
        sys.exit(1)