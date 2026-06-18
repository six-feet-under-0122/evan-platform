"""
Service 层：业务逻辑
1. API 层只做参数校验，业务逻辑下沉到 service
2. 可测试：service 不依赖 Flask request，纯函数式
3. 可复用：CLI、定时任务、其他 service 都可以调用
4. 可编排：未来 ChatService 会编排 memory/rule/tool 多个 service
"""

from app.services.auth_service import AuthService

__all__ = ['AuthService']