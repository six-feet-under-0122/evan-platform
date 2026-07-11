import base64
import os
import requests
from flask import current_app
from app.providers.llm.base import BaseLLMProvider
from app.common.errors import AppError, ErrorCode


class ChatAnywhereProvider(BaseLLMProvider):

    def chat(self, messages: list, model: str, **kwargs) -> str:
        api_key = current_app.config['CHATANYWHERE_API_KEY']
        api_url = current_app.config.get(
            'CHATANYWHERE_API_URL',
            'https://api.chatanywhere.tech/v1/chat/completions'
        )

        try:
            resp = requests.post(
                api_url,
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': model,
                    'messages': messages,  # messages 已经是组装好的格式
                },
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content']

        except requests.Timeout:
            raise AppError(ErrorCode.LLM_TIMEOUT, 'LLM request timed out', 504)
        except requests.RequestException as e:
            raise AppError(ErrorCode.LLM_REQUEST_FAILED, f'LLM request failed: {e}', 502)


def blocks_to_openai_content(blocks: list, upload_folder: str) -> list:
    """
    把 message 的 blocks 结构转成 OpenAI 的 content 格式

    blocks 格式（你自己的）：
        [
            {"type": "text", "text": "帮我看看这张图"},
            {"type": "image", "file_id": "abc123", "storage_path": "2026/07/10/abc.png"}
        ]

    OpenAI 格式：
        [
            {"type": "text", "text": "帮我看看这张图"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
        ]
    """
    content = []

    for block in blocks:
        if block['type'] == 'text':
            # 文本 block 直接转
            content.append({
                'type': 'text',
                'text': block['text']
            })

        elif block['type'] == 'image':
            # 图片 block：读文件 → 转 base64
            full_path = os.path.join(upload_folder, block['storage_path'])

            with open(full_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

            # OpenAI 的 base64 图片格式
            content.append({
                'type': 'image_url',
                'image_url': {
                    'url': f"data:{block['content_type']};base64,{image_data}"
                }
            })

    return content
