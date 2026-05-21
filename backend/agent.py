"""
住宅户型分析 - AI Agent
基于 Agent 架构：感知 -> 推理 -> 决策 -> 行动
读取知识库中的风水规则，结合户型图进行智能分析
"""

import os
import json
from openai import OpenAI, APIStatusError


class FengShuiAgent:
    """户型分析 AI Agent"""

    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model_name = model_name
        self.knowledge = self._load_knowledge()

    def _load_knowledge(self) -> str:
        """加载户型分析知识库"""
        knowledge_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "knowledge",
            "feng_shui_skills.json",
        )
        with open(knowledge_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 将知识库格式化为文本
        text_parts = []
        for item in data:
            text_parts.append(f"【{item['category']}】{item['title']}")
            for rule in item["rules"]:
                text_parts.append(f"  - {rule}")
            text_parts.append("")
        return "\n".join(text_parts)

    def analyze(self, image_base64: str, mime_type: str) -> str:
        """
        AI Agent 分析户型图

        Agent 流程:
        1. 感知 - 接收并理解户型图
        2. 推理 - 结合知识库分析户型
        3. 行动 - 生成结构化的户型分析报告
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt()

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                },
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ],
                max_completion_tokens=4096,
            )

            return response.choices[0].message.content

        except APIStatusError as e:
            raise RuntimeError(
                f"模型 API 调用失败 (HTTP {e.status_code}): {e.response.text}"
            ) from e

    def _build_system_prompt(self) -> str:
        """构建系统提示词 - 读取 skills 模板并注入知识库内容"""
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "knowledge",
            "feng_shui_system_prompt.md",
        )
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.replace("{knowledge}", self.knowledge)

    def _build_user_prompt(self) -> str:
        """构建用户提示词"""
        return "请分析这张户型图，结合你的知识库给出专业的户型分析报告。"