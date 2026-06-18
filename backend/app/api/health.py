"""
健康检查接口

1.部署后验证 Caddy → Gunicorn → Flask 链路是否通
2.监控系统（如 UptimeRobot）定时探活
3.容器化部署时 Kubernetes/Docker 的 healthcheck

不需要鉴权
"""

from flask import Blueprint, current_app
from app.common.resp import ok
from app.extensions import db

bp = Blueprint('health', __name__, url_prefix='/api')


@bp.route('/health', methods=['GET'])
def health():
    """基础健康检查"""
    return ok({
        'status': 'healthy',
        'service': 'evan-platform'
    })


@bp.route('/health/db', methods=['GET'])
def health_db():
    """数据库健康检查"""
    try:
        # 执行简单查询验证数据库连接
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        current_app.logger.error(f'Database health check failed: {e}')
        db_status = 'unhealthy'

    return ok({
        'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
        'database': db_status
    })