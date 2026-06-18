"""
初始化用户脚本（用于第一次部署）
比 flask create-user 更适合自动化部署
"""

import os
import sys
import getpass

# 把 backend 目录加到 Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.auth_service import AuthService
from app.common.errors import AppError


def main():
    """主函数"""
    print('=' * 60)
    print('Evan Platform - Initial User Setup')
    print('=' * 60)

    app = create_app()

    with app.app_context():
        # 检查是否已有用户
        from app.models.user import User
        existing_count = User.query.count()

        if existing_count > 0:
            print(f'\n⚠ Warning: {existing_count} user(s) already exist.')
            confirm = input('Continue creating new user? (y/N): ')
            if confirm.lower() != 'y':
                print('Aborted.')
                return

        # 收集输入
        print('\nEnter user information:')
        username = input('Username: ').strip()
        if not username:
            print('Error: Username cannot be empty.')
            return

        password = getpass.getpass('Password: ')
        password_confirm = getpass.getpass('Confirm password: ')

        if password != password_confirm:
            print('Error: Passwords do not match.')
            return

        if len(password) < 6:
            print('Error: Password must be at least 6 characters.')
            return

        email = input('Email (optional): ').strip() or None
        display_name = input('Display name (optional): ').strip() or None
        role = input('Role [user/admin] (default: admin): ').strip() or 'admin'

        if role not in ('user', 'admin'):
            print('Error: Role must be "user" or "admin".')
            return

        # 创建用户
        try:
            user = AuthService.create_user(
                username=username,
                password=password,
                email=email,
                display_name=display_name,
                role=role
            )
            print(f'\n✓ User created successfully!')
            print(f'  ID: {user.id}')
            print(f'  Username: {user.username}')
            print(f'  Role: {user.role}')
        except AppError as e:
            print(f'\n✗ Error: {e.message}')


if __name__ == '__main__':
    main()