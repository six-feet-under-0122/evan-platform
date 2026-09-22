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
        @require_json_fields('username', 'password') <= 对于有参数的修饰器，执行require_json_fields('username', 'password')(login)
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

        return wrapper#<=包装函数 #decorator运行到这就会把原函数运行了

    return decorator#require_json_fields运行到这里开始运行decorator
# 同理，这样的结构可以支持套超多层
"""
import functools

# 四层嵌套：为了接收两个不同阶段的参数
def log_to_file(filename):                 # 【第1层】：接收文件名
    def log_with_prefix(prefix):          # 【第2层】：接收日志前缀
        def decorator(f):                  # 【第3层】：【执行】接收原函数
            @functools.wraps(f)
            def wrapper(*args, **kwargs):  # 【第4层】：【包装】全新函数
                print(f"打开文件 {filename}，写入: {prefix} 函数执行了")
                return f(*args, **kwargs)
            return wrapper
        return decorator
    return log_with_prefix
    
    @log_to_file("app.log")("[WARNING]")  #连续写两个括号
def multiply(a, b):
    return a * b
"""