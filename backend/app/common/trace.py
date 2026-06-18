"""
请求追踪（trace_id）
1. 每个请求有唯一 ID，方便排查问题
2. 日志、响应、异常都带上 trace_id，形成调用链
3. 未来接入分布式追踪（如 OpenTelemetry）也是基于这个
"""

import uuid
from flask import g, request


def generate_trace_id() -> str:
    """生成唯一的 trace_id"""
    return str(uuid.uuid4())


def init_trace(app):
    """
    初始化追踪系统

    在每个请求开始时生成 trace_id，存到 g（Flask 的请求上下文）
    """

    @app.before_request
    def before_request():
        # 优先使用客户端传来的 trace_id（如果有）
        trace_id = request.headers.get('X-Trace-ID')

        # 如果没有就生成新的
        if not trace_id:
            trace_id = generate_trace_id()

        g.trace_id = trace_id

    @app.after_request
    def after_request(response):
        # 把 trace_id 加到响应头（方便客户端追踪）
        response.headers['X-Trace-ID'] = g.get('trace_id', '')
        return response