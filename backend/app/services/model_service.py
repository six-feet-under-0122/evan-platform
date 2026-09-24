from typing import List, Dict
from app import db
from datetime import datetime


class ModelService:
    """
    模型管理服务
    未来可以从 evan-daemon 同步模型列表
    现在先hardcode一些常用模型
    """

    # 硬编码的模型列表（后续改为从数据库读取）
    AVAILABLE_MODELS = [
        {
            'id': 'gpt-4o-mini',
            'name': 'GPT-4o Mini',
            'provider': 'openai',
            'type': 'api',
            'description': '快速、便宜的模型，适合日常对话',
            'max_tokens': 16384,
            'enabled': True,
        },
        {
            'id': 'gpt-4o',
            'name': 'GPT-4o',
            'provider': 'openai',
            'type': 'api',
            'description': '更强大的推理能力',
            'max_tokens': 128000,
            'enabled': True,
        },
        {
            'id': 'gpt-4-turbo',
            'name': 'GPT-4 Turbo',
            'provider': 'openai',
            'type': 'api',
            'description': 'GPT-4 升级版',
            'max_tokens': 128000,
            'enabled': True,
        },
        # 本地模型（需要 Ollama）
        {
            'id': 'qwen2.5:14b',
            'name': 'Qwen 2.5 14B',
            'provider': 'ollama',
            'type': 'local',
            'description': '本地运行，免费无限制',
            'max_tokens': 32768,
            'enabled': False,  # 默认关闭，需要用户安装 Ollama
        },
    ]

    @classmethod
    def list_available(cls) -> List[Dict]:
        """获取可用模型列表"""
        # TODO: 未来从数据库读取，由 evan-daemon 更新
        return [m for m in cls.AVAILABLE_MODELS if m['enabled']]

    @classmethod
    def get_default(cls) -> str:
        """获取默认模型"""
        return 'gpt-4o-mini'

    @classmethod
    def get_model_info(cls, model_id: str) -> Dict:
        """获取模型详情"""
        for model in cls.AVAILABLE_MODELS:
            if model['id'] == model_id:
                return model
        return None

    @classmethod
    def is_valid_model(cls, model_id: str) -> bool:
        """验证模型ID是否有效"""
        return cls.get_model_info(model_id) is not None

