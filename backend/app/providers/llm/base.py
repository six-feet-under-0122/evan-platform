from abc import ABC, abstractmethod
from typing import Generator
# Abstract Base Classes
# cpp中的纯虚函数+抽象类

class BaseLLMProvider(ABC):

    @abstractmethod
    def chat(self, messages: list, model: str, **kwargs) -> str:
        """
        发送消息，返回回复文本

        Args:
            messages: 消息列表，格式：
                [{"role": "user", "content": "..."}, ...]
            model: 模型名称
            **kwargs: 额外参数（比如 temperature、max_tokens 等）
        """

        pass

    @abstractmethod
    def stream(self, messages: list, model: str, **kwargs) -> Generator[str, None, None]:
        """发送消息，以生成器方式逐块 yield 文本片段"""
        pass

    '''
    在 Python 中，kwargs 代表 Keyword Arguments（关键字参数）。
    它是一个语法糖，允许向函数传递任意数量的、带有名字的参数。
    当在函数定义中使用 kwargs 时，Python 会把所有未被显式定义的关键字参数，打包成一个字典（Dictionary）传进函数内部。
    '''