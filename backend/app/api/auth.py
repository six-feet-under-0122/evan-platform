"""
认证 API
接口：
- POST /api/auth/login    用户登录
- POST /api/auth/refresh  刷新 token
- GET  /api/auth/me       获取当前用户信息
- POST /api/auth/logout   登出（前端清除 token 即可，这里只是占位）
-"不开放注册" 用户创建通过 CLI 脚本（scripts/init_user.py）
"""

from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt
)
from app.services.auth_service import AuthService
from app.common.resp import ok
from app.utils.decorators import require_json_fields

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/login', methods=['POST'])
@require_json_fields('username', 'password')
def login():
    """
    用户登录

    Request:
        { "username": "...", "password": "..." }

    Response:
        {
            "ok": true,
            "data": {
                "access_token": "...",
                "refresh_token": "...",
                "user": { ... }
            }
        }
    """
    data = request.get_json()

    result = AuthService.login(
        username=data['username'],
        password=data['password']
    )

    return ok(result, message='Login successful')


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # 必须用 refresh token 调用
def refresh():
    """
    刷新 access token

    Headers:
        Authorization: Bearer <refresh_token>

    Response:
        {
            "ok": true,
            "data": { "access_token": "..." }
        }
    """
    user_id = get_jwt_identity()#配合@jwt_required()一起食用
    result = AuthService.refresh_token(user_id)

    return ok(result, message='Token refreshed')


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    获取当前用户信息

    Headers:
        Authorization: Bearer <access_token>

    Response:
        {
            "ok": true,
            "data": { user_info }
        }
    """
    user_id = get_jwt_identity()
    user = AuthService.get_current_user(user_id)

    return ok(user.to_dict())


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    登出

    注意：JWT 是无状态的，真正的登出有两种方式：
    1. 前端删除 token（最简单，推荐先用这个）
    2. 后端维护 token 黑名单（需要 Redis，未来再做）

    这里只是占位，方便前端调用
    """
    return ok(message='Logout successful')