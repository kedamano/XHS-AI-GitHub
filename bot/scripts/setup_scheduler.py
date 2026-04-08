#!/usr/bin/env python3
"""
定时任务设置脚本
支持 Windows 任务计划程序和 macOS/Linux crontab
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def get_script_path():
    """获取主脚本路径"""
    return Path(__file__).parent / 'main.py'


def setup_windows():
    """设置 Windows 定时任务"""
    script_path = get_script_path()
    python_path = sys.executable

    task_name = "GitHubAITrendingBot"

    # 删除已存在的任务
    subprocess.run(
        f'schtasks /delete /tn "{task_name}" /f',
        shell=True,
        capture_output=True
    )

    # 创建新任务
    # 每天 9:00 执行
    command = f'schtasks /create /tn "{task_name}" /tr "\"{python_path}\" \\"{script_path}\\"" /sc daily /st 09:00'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Windows 定时任务设置成功！")
        print(f"   任务名称: {task_name}")
        print(f"   执行时间: 每天 09:00")
        print(f"   执行脚本: {script_path}")
        print("\n💡 你可以运行 'schtasks /run /tn \"GitHubAITrendingBot\"' 手动执行")
    else:
        print(f"❌ 设置失败: {result.stderr}")


def setup_macos_linux():
    """设置 macOS/Linux 定时任务"""
    script_path = get_script_path()
    cron_dir = Path.home() / '.github-trending-bot'

    # 创建日志目录
    cron_dir.mkdir(parents=True, exist_ok=True)
    log_file = cron_dir / 'cron.log'

    # crontab 条目
    cron_entry = f"# GitHub AI Trending Bot - 每天 9:00 执行\n"
    cron_entry += f"0 9 * * * cd {script_path.parent.parent} && python3 {script_path} >> {log_file} 2>&1\n"

    print(f"📝 Crontab 条目:")
    print(cron_entry)

    # 获取当前 crontab
    try:
        current_cron = subprocess.run(
            ['crontab', '-l'],
            capture_output=True,
            text=True
        ).stdout
    except:
        current_cron = ""

    # 检查是否已存在
    if "GitHubAITrendingBot" in current_cron:
        print("⚠️ 定时任务已存在，正在更新...")

        # 移除旧的
        lines = current_cron.split('\n')
        lines = [l for l in lines if "GitHubAITrendingBot" not in l and l.strip()]
        new_cron = '\n'.join(lines) + '\n' + cron_entry
    else:
        new_cron = current_cron + cron_entry

    # 安装新的 crontab
    subprocess.run(
        ['crontab', '-'],
        input=new_cron,
        text=True
    )

    print("✅ macOS/Linux 定时任务设置成功！")
    print(f"   执行时间: 每天 09:00")
    print(f"   日志文件: {log_file}")
    print(f"\n💡 查看日志: tail -f {log_file}")
    print(f"💡 查看任务: crontab -l")
    print(f"💡 删除任务: crontab -e (手动删除)")


def setup_workbuddy_automation():
    """设置 WorkBuddy 自动化任务"""
    print("\n📋 WorkBuddy 自动化设置说明:")
    print("-" * 50)
    print("1. 打开 WorkBuddy")
    print("2. 进入「自动化」功能")
    print("3. 创建新自动化任务")
    print("4. 设置:")
    print("   - 触发条件: 定时触发 (每天)")
    print("   - 执行时间: 09:00")
    print("   - 执行命令: python /path/to/scripts/main.py")
    print("5. 保存并启用")


def main():
    """主函数"""
    print("🚀 GitHub AI Trending Bot 定时任务设置")
    print("=" * 50)

    system = platform.system()

    if system == "Windows":
        setup_windows()
    elif system in ["Darwin", "Linux"]:
        setup_macos_linux()
    else:
        print(f"❌ 不支持的操作系统: {system}")

    # 显示其他选项
    print("\n" + "=" * 50)
    print("💡 其他定时任务设置方式:")
    print("-" * 50)
    setup_workbuddy_automation()

    print("\n" + "=" * 50)
    print("📌 手动测试运行:")
    print(f"   python {get_script_path()}")


if __name__ == '__main__':
    main()
