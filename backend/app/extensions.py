"""
扩展初始化模块
为什么需要这个：
1. 避免循环导入：在这里创建全局扩展对象，但不立即绑定 app
2. 集中管理：所有第三方库的初始化都在这里
3. 支持应用工厂模式：create_app 时再绑定

"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 创建扩展实例（不绑定 app）
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def init_extensions(app):
    """初始化所有扩展（在 create_app 中调用）"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        origins=app.config['CORS_ORIGINS'],
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
    )