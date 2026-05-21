"""
住宅户型分析 - Streamlit 前端
简洁的界面：上传户型图 -> 预览 -> 分析 -> 查看报告
"""

import streamlit as st
import requests
import base64
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="住宅户型分析",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 隐藏 Streamlit 默认元素
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 标题
st.title("🏠 住宅户型分析")
st.markdown("上传户型图，AI 为你解读住宅户型")

# 后端地址
BACKEND_URL = "http://localhost:5000"

# 上传图片
uploaded_file = st.file_uploader(
    "上传户型图",
    type=["jpg", "jpeg", "png", "webp"],
    help="支持 JPG、PNG、WebP 格式",
)

# 图片预览
if uploaded_file is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="户型图预览", width='stretch')

    st.divider()

    # 分析按钮
    if st.button("🔍 分析户型", type="primary", width='stretch'):
        with st.spinner("AI 正在分析中，请稍候..."):
            try:
                # 上传图片到后端
                uploaded_file.seek(0)
                files = {"image": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
                response = requests.post(f"{BACKEND_URL}/api/analyze", files=files, timeout=120)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        report = data["report"]
                        timestamp = data.get("timestamp", "")

                        st.divider()
                        st.subheader("📋 户型分析报告")

                        # 展示报告
                        st.markdown(report)

                        # 下载报告
                        st.divider()
                        report_text = f"住宅户型分析报告\n分析时间: {timestamp}\n\n{report}"
                        st.download_button(
                            label="📥 下载分析报告",
                            data=report_text,
                            file_name=f"户型分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            width='stretch',
                        )
                    else:
                        st.error(f"分析失败: {data.get('error', '未知错误')}")
                else:
                    # 尝试解析错误响应
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', '未知错误')
                        st.error(f"❌ 请求失败 (状态码: {response.status_code})\n\n**错误详情:**\n{error_msg}")
                    except:
                        st.error(f"❌ 请求失败 (状态码: {response.status_code})\n\n响应内容: {response.text[:500]}")

            except requests.exceptions.ConnectionError:
                st.error("⚠️ 无法连接到后端服务，请确保后端已启动 (python backend/app.py)")
            except Exception as e:
                st.error(f"分析出错: {str(e)}")
else:
    st.info("👆 请先上传一张户型图")