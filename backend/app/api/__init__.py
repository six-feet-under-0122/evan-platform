"""
API 蓝图注册

为什么所有蓝图都在这里注册：
1. 集中管理路由前缀
2. 方便查看项目有哪些 API
3. create_app 调用 register_blueprints 即可
"""

from app.api.health import bp as health_bp
from app.api.auth import bp as auth_bp
from app.api.sessions import bp as sessions_bp
from app.api.chat import bp as chat_bp
from app.api.files import bp as files_bp
from app.api import models as models_bp

def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(files_bp, url_prefix='/api/files')
    app.register_blueprint(models_bp.bp, url_prefix='/api/models')
