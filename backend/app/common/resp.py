from flask import jsonify, g
from typing import Any, Optional


def ok(data: Any = None, message: str = 'Success', status: int = 200) -> tuple:
    """
    成功响应

    Args:
        data: 返回的数据（可以是 dict、list、None）
        message: 成功消息（可选）

    Returns:
        (response, status_code)
    """
    response = {
        'ok': True,
        'data': data,
        'message': message,
        'trace_id': g.get('trace_id', '')
    }
    return jsonify(response), status


def fail(code: str, message: str, status: int = 400, extra: Optional[dict] = None) -> tuple:
    """
    失败响应

    Args:
        code: 错误码（来自 ErrorCode）
        message: 错误消息
        status: HTTP 状态码
        extra: 额外信息（可选，用于调试）

    Returns:
        (response, status_code)
    """
    response = {
        'ok': False,
        'error': {
            'code': code,
            'message': message
        },
        'trace_id': g.get('trace_id', '')
    }

    # 开发环境可以附加额外信息（生产环境建议去掉）
    if extra:
        response['error']['extra'] = extra

    return jsonify(response), status


def paginated(items: list, total: int, page: int, per_page: int) -> tuple:
    """
    分页响应

    Args:
        items: 当前页数据
        total: 总数
        page: 当前页码
        per_page: 每页条数

    Returns:
        (response, status_code)
    """
    response = {
        'ok': True,
        'data': {
            'items': items,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page  # 向上取整
            }
        },
        'trace_id': g.get('trace_id', '')
    }
    return jsonify(response), 200