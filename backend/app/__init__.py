"""工具函数模块""""""
应用工厂
1. 支持测试：每个测试可以创建独立的 app
2. 避免全局副作用：导入不会自动初始化
3. 支持多环境：dev/prod 用不同配置创建 app

启动流程：
1. 创建 Flask app
2. 加载配置
3. 初始化扩展（db/jwt/cors）
4. 初始化通用功能（trace/logging）   
5. 注册错误处理
6. 注册蓝图
"""

import os
from flask import Flask
from app.config import config
from app.extensions import init_extensions, db
from app.common.trace import init_trace
from app.common.logging import init_logging
from app.common import resp
from app.common.errors import AppError, ErrorCode
from flask_jwt_extended.exceptions import (
    NoAuthorizationError, JWTDecodeError
)
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def create_app(config_name=None):
    """
    应用工厂函数

    Args:
        config_name: 配置名称（development/production/testing）
                    如果为 None，从环境变量读取 FLASK_ENV
    """
    # 决定配置
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    init_logging(app)
    app.logger.info(f'Starting app with config: {config_name}')
    init_extensions(app)
    init_trace(app)
    register_error_handlers(app)
    from app.api import register_blueprints
    register_blueprints(app)

    # 6. 注册 CLI 命令（可选）
    register_cli_commands(app)

    # 7. 导入所有 model（确保 Flask-Migrate 能发现）
    from app import models  # noqa: F401

    app.logger.info('App initialized successfully')

    return app


def register_error_handlers(app):
    """
    注册全局错误处理

    为什么这样做（你笔记里强调的）：
    1. 业务层只需要 raise AppError，不用关心 HTTP 响应
    2. 所有错误都走统一格式
    3. 未捕获异常也有兜底处理
    """

    # 1. 自定义业务异常
    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        app.logger.warning(f'AppError: {e.code} - {e.message}')
        return resp.fail(e.code, e.message, e.status, e.extra if app.debug else None)

    # 2. JWT 相关异常
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth(e):
        return resp.fail(
            ErrorCode.UNAUTHORIZED,
            'Missing authorization header',
            401
        )

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token(e):
        return resp.fail(
            ErrorCode.TOKEN_EXPIRED,
            'Token has expired',
            401
        )

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(e):
        return resp.fail(
            ErrorCode.TOKEN_INVALID,
            'Invalid token',
            401
        )

    @app.errorhandler(JWTDecodeError)
    def handle_jwt_decode(e):
        return resp.fail(
            ErrorCode.TOKEN_INVALID,
            'Token decode failed',
            401
        )

    # 3. 404 错误
    @app.errorhandler(404)
    def handle_not_found(e):
        return resp.fail(
            ErrorCode.NOT_FOUND,
            f'Endpoint not found: {e.description}',
            404
        )

    # 4. 405 方法不允许
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return resp.fail(
            ErrorCode.INVALID_REQUEST,
            'Method not allowed',
            405
        )

    # 5. 兜底：所有未捕获的异常
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        # 这里要打 error 级别，因为是未预期的
        app.logger.exception(f'Unexpected error: {e}')

        # 生产环境不暴露具体错误信息（安全考虑）
        if app.debug:
            return resp.fail(
                ErrorCode.INTERNAL_ERROR,
                f'Internal server error: {str(e)}',
                500
            )
        else:
            return resp.fail(
                ErrorCode.INTERNAL_ERROR,
                'Internal server error',
                500
            )


def register_cli_commands(app):
    """
    注册 Flask CLI 命令

    用法：flask <command>

    为什么需要 CLI 命令：
    1. 初始化数据（创建管理员用户）
    2. 数据库维护任务
    3. 一次性脚本（数据迁移、清理等）
    """

    @app.cli.command('create-user')
    def create_user_command():
        """
        创建用户的 CLI 命令

        用法：
            flask create-user
        """
        import click
        from app.services.auth_service import AuthService
        from app.common.errors import AppError
    #输入
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        email = click.prompt('Email (optional)', default='', show_default=False)
        display_name = click.prompt('Display name (optional)', default='', show_default=False)
        role = click.prompt('Role', default='user', type=click.Choice(['user', 'admin']))

        try:
            user = AuthService.create_user(
                username=username,
                password=password,
                email=email if email else None,
                display_name=display_name if display_name else None,
                role=role
            )
            click.echo(f'✓ User created: {user.username} (id={user.id})')
        except AppError as e:
            click.echo(f'✗ Error: {e.message}', err=True)

    @app.cli.command('list-users')
    def list_users_command():
        """列出所有用户"""
        import click
        from app.models.user import User

        users = User.query.all()

        if not users:
            click.echo('No users found.')
            return

        click.echo(f'{"ID":<38} {"Username":<20} {"Role":<10} {"Active":<8}')
        click.echo('-' * 80)
        for user in users:
            click.echo(f'{user.id:<38} {user.username:<20} {user.role:<10} {str(user.is_active):<8}')