class ErrorCode:
    """错误码常量"""

    # 通用错误 (1xxx)
    INVALID_REQUEST = 'INVALID_REQUEST'  # 请求参数错误
    UNAUTHORIZED = 'UNAUTHORIZED'  # 未登录
    FORBIDDEN = 'FORBIDDEN'  # 无权限
    NOT_FOUND = 'NOT_FOUND'  # 资源不存在
    CONFLICT = 'CONFLICT'  # 资源冲突
    INTERNAL_ERROR = 'INTERNAL_ERROR'  # 服务器内部错误

    # 认证相关 (2xxx)
    INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'  # 用户名或密码错误
    TOKEN_EXPIRED = 'TOKEN_EXPIRED'  # Token 过期
    TOKEN_INVALID = 'TOKEN_INVALID'  # Token 无效
    USER_NOT_FOUND = 'USER_NOT_FOUND'  # 用户不存在
    USER_ALREADY_EXISTS = 'USER_ALREADY_EXISTS'  # 用户已存在

    # 会话相关 (3xxx)
    SESSION_NOT_FOUND = 'SESSION_NOT_FOUND'  # 会话不存在
    SESSION_ACCESS_DENIED = 'SESSION_ACCESS_D'

    # 消息相关 (4xxx)
    MESSAGE_NOT_FOUND = 'MESSAGE_NOT_FOUND'  # 消息不存在

    # 文件相关 (5xxx)
    FILE_TOO_LARGE = 'FILE_TOO_LARGE'  # 文件过大
    FILE_TYPE_NOT_ALLOWED = 'FILE_TYPE_NOT_ALLOWED'  # 文件类型不支持
    FILE_NOT_FOUND = 'FILE_NOT_FOUND'  # 文件不存在
    FILE_UPLOAD_FAILED = 'FILE_UPLOAD_FAILED'  # 文件上传失败

    # LLM 相关 (6xxx)
    LLM_REQUEST_FAILED = 'LLM_REQUEST_FAILED'  # LLM 调用失败
    LLM_TIMEOUT = 'LLM_TIMEOUT'  # LLM 超时
    MODEL_NOT_AVAILABLE = 'MODEL_NOT_AVAILABLE'  # 模型不可用


class AppError(Exception):

    def __init__(self, code: str, message: str, status: int = 400, extra: dict = None):
        self.code = code
        self.message = message
        self.status = status
        self.extra = extra or {}
        super().__init__(self.message)

    def to_dict(self):
        """转成字典（用于日志）"""
        return {
            'code': self.code,
            'message': self.message,
            'status': self.status,
            'extra': self.extra
        }


# 常用异常快捷方式（减少重复代码）

class BadRequestError(AppError):
    """400 错误"""

    def __init__(self, message='Invalid request', code=ErrorCode.INVALID_REQUEST):
        super().__init__(code, message, 400)


class UnauthorizedError(AppError):
    """401 错误"""

    def __init__(self, message='Unauthorized', code=ErrorCode.UNAUTHORIZED):
        super().__init__(code, message, 401)


class ForbiddenError(AppError):
    """403 错误"""

    def __init__(self, message='Forbidden', code=ErrorCode.FORBIDDEN):
        super().__init__(code, message, 403)


class NotFoundError(AppError):
    """404 错误"""

    def __init__(self, message='Resource not found', code=ErrorCode.NOT_FOUND):
        super().__init__(code, message, 404)


class ConflictError(AppError):
    """409 错误"""

    def __init__(self, message='Resource conflict', code=ErrorCode.CONFLICT):
        super().__init__(code, message, 409)


class InternalError(AppError):
    """500 错误"""

    def __init__(self, message='Internal server error', code=ErrorCode.INTERNAL_ERROR):
        super().__init__(code, message, 500)