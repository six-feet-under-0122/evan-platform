from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models.user import User
from app.common.errors import (
    UnauthorizedError, NotFoundError, ConflictError, ErrorCode
)


class AuthService:

    @staticmethod
    def login(username: str, password: str) -> dict:
        """
        用户登录
        Args:
            username: 用户名
            password: 密码
        Returns:
            {
                'access_token': str,
                'refresh_token': str,
                'user': dict
            }
        Raises:
            UnauthorizedError: 用户名或密码错误
        """
        user = User.find_by_username(username)

        if not user:
            raise UnauthorizedError(
                message='Invalid username or password',
                code=ErrorCode.INVALID_CREDENTIALS
            )
        if not user.check_password(password):
            raise UnauthorizedError(
                message='Invalid username or password',
                code=ErrorCode.INVALID_CREDENTIALS
            )
        if not user.is_active:
            raise UnauthorizedError(
                message='Account is disabled',
                code=ErrorCode.FORBIDDEN
            )
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        # 生成 token
        # identity 是 JWT 里的 sub 字段，用 user_id
        # additional_claims 可以放额外信息（用户名、角色等）
        additional_claims = {
            'username': user.username,
            'role': user.role
        }

        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            additional_claims=additional_claims
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }

    @staticmethod
    def refresh_token(user_id: str) -> dict:
        """
        刷新 access token
        Args:
            user_id: 当前用户 ID（从 refresh token 里解出来）
        Returns:
            {'access_token': str}
        """
        user = User.find_by_id(user_id)

        if not user:
            raise NotFoundError(
                message='User not found',
                code=ErrorCode.USER_NOT_FOUND
            )

        if not user.is_active:
            raise UnauthorizedError(
                message='Account is disabled',
                code=ErrorCode.FORBIDDEN
            )

        additional_claims = {
            'username': user.username,
            'role': user.role
        }

        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )


        return {'access_token': access_token}

    @staticmethod
    def get_current_user(user_id: str) -> User:
        """
        获取当前用户（用于 /me 接口）
        Args:
            user_id: 用户 ID（从 JWT 解出来）

        Returns:
            User 对象
        """
        user = User.find_by_id(user_id)

        if not user:
            raise NotFoundError(
                message='User not found',
                code=ErrorCode.USER_NOT_FOUND
            )

        return user

    @staticmethod
    def create_user(username: str, password: str, email: str = None,
                    display_name: str = None, role: str = 'user') -> User:
        """
        创建用户（仅供管理员/CLI 使用，不对外开放）
        Args:
            username: 用户名
            password: 密码
            email: 邮箱（可选）
            display_name: 显示名称（可选）
            role: 角色（admin/user）
        Returns:
            User 对象
        """
        # 检查用户名是否已存在
        if User.find_by_username(username):
            raise ConflictError(
                message=f'Username "{username}" already exists',
                code=ErrorCode.USER_ALREADY_EXISTS
            )

        # 检查邮箱是否已存在
        if email and User.find_by_email(email):
            raise ConflictError(
                message=f'Email "{email}" already exists',
                code=ErrorCode.USER_ALREADY_EXISTS
            )

        # 创建用户
        user = User(
            username=username,
            email=email,
            display_name=display_name,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user