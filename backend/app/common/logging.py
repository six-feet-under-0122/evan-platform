import logging
import json
import sys
from datetime import datetime
from flask import g, request, has_request_context


class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器（JSON）"""

    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }

        # 如果在请求上下文中，加上请求信息
        if has_request_context():
            log_data.update({
                'trace_id': g.get('trace_id', ''),
                'method': request.method,
                'path': request.path,
                'ip': request.remote_addr
            })

        # 加上异常信息（如果有）
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # 加上自定义字段（通过 extra 传入）
        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        return json.dumps(log_data, ensure_ascii=False)


class TextFormatter(logging.Formatter):
    """文本日志格式化器（开发环境友好）"""

    def format(self, record):
        parts = [
            f"[{datetime.utcnow().isoformat()}]",
            f"[{record.levelname}]",
        ]

        if has_request_context():
            trace_id = g.get('trace_id', '')[:8]  # 只显示前 8 位
            parts.append(f"[{trace_id}]")
            parts.append(f"[{request.method} {request.path}]")

        parts.append(record.getMessage())

        log_line = ' '.join(parts)

        if record.exc_info:
            log_line += '\n' + self.formatException(record.exc_info)

        return log_line


def init_logging(app):
    """
    初始化日志系统

    根据配置选择格式化器（json/text）
    """

    # 清除默认 handler
    app.logger.handlers = []

    # 创建 handler
    handler = logging.StreamHandler(sys.stdout)

    # 根据配置选择格式化器
    log_format = app.config.get('LOG_FORMAT', 'json')
    if log_format == 'json':
        handler.setFormatter(StructuredFormatter())
    else:
        handler.setFormatter(TextFormatter())

    # 设置日志级别
