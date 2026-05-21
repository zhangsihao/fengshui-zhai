"""
住宅户型分析 - Flask 后端服务
基于 AI Agent 架构，调用大模型分析户型图
"""

import os
import json
import yaml
import base64
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import FengShuiAgent

app = Flask(__name__)
CORS(app)

# 设置上传文件大小限制为 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# 加载配置
def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "未找到 config.yaml 配置文件，请复制 config.example.yaml 为 config.yaml 并填入你的模型配置"
        )
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 初始化 Agent
config = load_config()
agent = FengShuiAgent(
    base_url=config["model"]["base_url"],
    api_key=config["model"]["api_key"],
    model_name=config["model"]["model_name"],
)


@app.route("/api/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "message": "户型分析服务运行中"})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """分析户型图"""
    if "image" not in request.files:
        return jsonify({"error": "请上传户型图"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "未选择文件"}), 400

    try:
        # 读取图片并转为 base64
        image_data = file.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # 获取文件扩展名确定 MIME 类型
        ext = os.path.splitext(file.filename)[1].lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
        mime_type = mime_map.get(ext, "image/jpeg")

        # 调用 AI Agent 分析
        report = agent.analyze(image_base64, mime_type)

        return jsonify({
            "success": True,
            "report": report,
            "timestamp": datetime.now().isoformat(),
        })

    except Exception as e:
        import traceback
        error_detail = f"分析失败: {str(e)}\n\n详细错误:\n{traceback.format_exc()}"
        print(f"[ERROR] {error_detail}")  # 同时打印到控制台
        return jsonify({"error": error_detail}), 500


if __name__ == "__main__":
    port = config.get("server", {}).get("backend_port", 5000)
    print(f"🏠 户型分析后端服务启动: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)