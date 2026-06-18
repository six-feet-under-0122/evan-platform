"""
WSGI 入口
1. 生产环境用 Gunicorn 启动：gunicorn wsgi:app
2. 开发环境也可以用：python wsgi.py
3. 跟代码分离，方便部署

"Gunicorn 是生产级 WSGI server，稳定并发比 Flask 自带 server 强"
"""

import os
from app import create_app

# 创建 app 实例（Gunicorn 会找这个变量）
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # 仅开发环境使用：python wsgi.py
    # 生产环境用：gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )