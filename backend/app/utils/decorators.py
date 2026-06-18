"""
通用装饰器

为什么需要这个：
1. 参数校验逻辑可复用
2. 路由代码更简洁
"""

from functools import wraps
from flask import request
from app.common.errors import BadRequestError


def require_json_fields(*required_fields):
    """
    校验 JSON 请求体必须包含指定字段

    用法：
        @require_json_fields('username', 'password')
        def login():
            data = request.get_json()
            ...
    """

    def decorator(f):
        @wraps(f)# 1.让接下来的wrapper继承原函数f的名字和文档
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)

            if not data:
                raise BadRequestError('Request body must be JSON')

            missing = [field for field in required_fields if field not in data]

            if missing:
                raise BadRequestError(
                    f'Missing required fields: {", ".join(missing)}'
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator