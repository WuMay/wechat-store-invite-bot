#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置测试脚本 - 帮助用户测试配置是否正确
"""

import json
import os


def test_config():
    """测试配置文件"""
    print("="*60)
    print("配置测试")
    print("="*60)

    # 检查配置文件是否存在
    if not os.path.exists("config.json"):
        print("✗ 配置文件不存在: config.json")
        return False

    print("\n✓ 配置文件存在")

    # 加载配置
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ 配置文件格式正确")
    except json.JSONDecodeError as e:
        print(f"✗ 配置文件格式错误: {e}")
        return False

    # 检查必要配置项
    required_fields = [
        'headless', 'implicit_wait', 'page_load_timeout',
        'min_delay', 'max_delay', 'max_retries',
        'record_file', 'log_file'
    ]

    missing_fields = [field for field in required_fields if field not in config]

    if missing_fields:
        print(f"✗ 缺少配置项: {', '.join(missing_fields)}")
        return False

    print("✓ 所有必要配置项都存在")

    # 显示配置
    print("\n当前配置：")
    print("-"*60)
    for key, value in config.items():
        print(f"  {key}: {value}")
    print("-"*60)

    # 验证配置值
    warnings = []

    if config['min_delay'] < 0.5:
        warnings.append("⚠ 最小延迟过小，可能导致被检测（建议 ≥ 1.0秒）")

    if config['max_delay'] < config['min_delay']:
        warnings.append("⚠ 最大延迟小于最小延迟，配置无效")

    if config['max_retries'] < 1:
        warnings.append("⚠ 最大重试次数过小（建议 ≥ 3）")

    if warnings:
        print("\n警告：")
        for warning in warnings:
            print(f"  {warning}")

    # 检查记录文件目录
    record_dir = os.path.dirname(config['record_file'])
    if record_dir and not os.path.exists(record_dir):
        print(f"\n⚠ 记录文件目录不存在: {record_dir}")
        print("  程序运行时会自动创建")

    # 检查日志文件目录
    log_dir = os.path.dirname(config['log_file'])
    if log_dir and not os.path.exists(log_dir):
        print(f"\n⚠ 日志文件目录不存在: {log_dir}")
        print("  程序运行时会自动创建")

    print("\n" + "="*60)
    print("配置测试完成")
    print("="*60)

    return True


def test_main_config():
    """测试主程序配置"""
    print("\n" + "="*60)
    print("主程序配置测试")
    print("="*60)

    # 读取main.py
    try:
        with open("main.py", 'r', encoding='utf-8') as f:
            content = f.read()
        print("✓ main.py 文件存在")
    except Exception as e:
        print(f"✗ 无法读取 main.py: {e}")
        return False

    # 检查START_URL
    if 'START_URL = "https://你的达人广场URL"' in content:
        print("\n⚠ 警告：START_URL 未修改")
        print("  请将 'https://你的达人广场URL' 替换为实际的URL")
    elif 'START_URL' in content:
        print("\n✓ START_URL 已配置")
    else:
        print("\n⚠ 未找到 START_URL 配置")

    # 检查选择器
    if 'talent-item' in content:
        print("⚠ 达人卡片选择器使用默认值，可能需要修改")
    if 'talent-name' in content:
        print("⚠ 达人名称选择器使用默认值，可能需要修改")

    print("\n提示：")
    print("  - 请确保 START_URL 已修改为正确的URL")
    print("  - 请根据实际页面调整选择器（使用 selector_helper.py）")
    print("  - 建议先测试少量邀约，确认流程正常")

    print("\n" + "="*60)
    print("主程序配置测试完成")
    print("="*60)

    return True


def test_dependencies():
    """测试依赖包"""
    print("\n" + "="*60)
    print("依赖包测试")
    print("="*60)

    dependencies = [
        'selenium',
        'webdriver_manager',
        'pillow'
    ]

    missing = []

    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"✗ {dep} 未安装")
            missing.append(dep)

    if missing:
        print(f"\n⚠ 缺少依赖包: {', '.join(missing)}")
        print("  请运行: pip install -r requirements.txt")
        return False

    print("\n✓ 所有依赖包都已安装")

    print("\n" + "="*60)
    print("依赖包测试完成")
    print("="*60)

    return True


def main():
    """主函数"""
    print("\n" + "="*60)
    print("微信小店达人广场邀约机器人 - 配置测试")
    print("="*60)
    print()

    results = []

    # 测试配置文件
    results.append(("配置文件", test_config()))

    # 测试主程序配置
    results.append(("主程序配置", test_main_config()))

    # 测试依赖包
    results.append(("依赖包", test_dependencies()))

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {name}: {status}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n✓ 所有测试通过！")
        print("\n下一步：")
        print("  1. 确认 START_URL 已修改为正确的URL")
        print("  2. 根据实际页面调整选择器（使用 selector_helper.py）")
        print("  3. 运行 python3 main.py 开始邀约")
    else:
        print("\n✗ 部分测试失败，请根据提示进行修改")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
