#!/usr/bin/env python3
"""
住宅户型分析 - 一键启动脚本
同时启动 Flask 后端和 Streamlit 前端
"""

import os
import sys
import time
import signal
import subprocess
import shutil

# 确保在项目根目录运行
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)


def check_config():
    """检查配置文件是否存在"""
    if not os.path.exists("config.yaml"):
        if os.path.exists("config.example.yaml"):
            print("=" * 50)
            print("⚠️  未找到 config.yaml 配置文件")
            print("请执行以下命令创建配置文件：")
            print("  cp config.example.yaml config.yaml")
            print("然后编辑 config.yaml 填入你的模型配置")
            print("=" * 50)
            sys.exit(1)
        else:
            print("❌ 缺少配置文件，请检查项目完整性")
            sys.exit(1)


def install_deps():
    """检查并安装依赖"""
    try:
        import flask
        import streamlit
        import openai
        import yaml
    except ImportError:
        print("📦 正在安装依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")


def main():
    """启动服务"""
    check_config()
    install_deps()

    processes = []

    def cleanup(signum=None, frame=None):
        print("\n🛑 正在关闭服务...")
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                p.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        # 启动 Flask 后端
        print("🚀 启动后端服务...")
        backend = subprocess.Popen(
            [sys.executable, "backend/app.py"],
            cwd=ROOT_DIR,
        )
        processes.append(backend)

        # 等后端启动
        time.sleep(2)

        # 启动 Streamlit 前端
        print("🚀 启动前端服务...")
        streamlit_path = shutil.which("streamlit")
        if streamlit_path:
            frontend = subprocess.Popen(
                [
                    streamlit_path, "run", "frontend/app.py",
                    "--server.port", "8501",
                    "--server.headless", "true",
                    "--browser.gatherUsageStats", "false",
                ],
                cwd=ROOT_DIR,
            )
        else:
            frontend = subprocess.Popen(
                [
                    sys.executable, "-m", "streamlit", "run", "frontend/app.py",
                    "--server.port", "8501",
                    "--server.headless", "true",
                    "--browser.gatherUsageStats", "false",
                ],
                cwd=ROOT_DIR,
            )
        processes.append(frontend)

        print("=" * 50)
        print("✅ 服务已启动！")
        print("   前端地址: http://localhost:8501")
        print("   后端地址: http://localhost:5000")
        print("   按 Ctrl+C 停止服务")
        print("=" * 50)

        # 自动打开浏览器
        time.sleep(3)
        try:
            import webbrowser
            webbrowser.open("http://localhost:8501")
        except Exception:
            pass

        # 等待子进程
        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()