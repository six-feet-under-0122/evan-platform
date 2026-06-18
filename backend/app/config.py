
"""
应用配置模块

为什么需要这个：
1. 配置分环境：dev 用 SQLite，prod 用 PostgreSQL
2. 从环境变量读取：换环境不动代码
3. 类型安全：配置集中管理，避免魔法字符串

对应旧 Evan 的问题：
- 旧：API key 硬编码在代码里
- 新：全部从环境变量读取，更安全
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载 .env 文件
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """基础配置（所有环境共享）"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-please-change-in-production')
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "dev.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 生产环境设为 False，开发可设 True 看 SQL
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-please-change')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')  # json or text
    
    # Upload
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # LLM Providers（先占位，后面会用）
    CHATANYWHERE_API_KEY = os.getenv('CHATANYWHERE_API_KEY', '')
    CHATANYWHERE_BASE_URL = os.getenv('CHATANYWHERE_BASE_URL', 'https://api.chatanywhere.tech/v1')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 开发环境打印 SQL


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 生产环境强制检查敏感配置
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # 确保生产环境设置了安全的 secret
        assert os.getenv('SECRET_KEY') != 'dev-secret-please-change-in-production', \
            'Must set SECRET_KEY in production'
        assert os.getenv('JWT_SECRET_KEY') != 'dev-jwt-secret-please-change', \
            'Must set JWT_SECRET_KEY in production'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 内存数据库


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
'''
在app.py中写下env = os.getenv('FLASK_ENV', 'default'）
app.config.from_object(config[env])
然后通过字典配置找到DevelopmentConfig
然后app.config.from_object事实上传进去DevelopmentConfig这个类。
然后flask就根据这个类执行类似
for key in dir(obj):
  if key.isupper():
    app.config[key] = getattr(obj, key)
    实现配置
额，productionconfig的话还会config[env].init_app(app)
然后检查配置
'''