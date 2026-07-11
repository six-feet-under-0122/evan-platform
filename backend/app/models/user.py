
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    """用户表"""

    __tablename__ = 'users'

    # 主键：UUID（字符串形式存储，SQLite/Postgres 都兼容）
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # 用户名（登录用，唯一）
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    # 显示名称（昵称）
    display_name = db.Column(db.String(64), nullable=True)
    # 角色：admin / user（未来权限控制用）
    role = db.Column(db.String(20), nullable=False, default='user')
    # 是否激活
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)#只要这个用户的任何其他数据被修改了，这里就必须自动把这个属性的值刷新成当前时间。
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # ============ 密码相关方法 ============

    def set_password(self, password: str):
        """设置密码（自动哈希）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    # ============ 序列化 ============

    def to_dict(self, include_sensitive=False) -> dict:
        """
        转成字典（用于 API 返回）
        Args:
            include_sensitive: 是否包含敏感字段（一般不返回给前端）
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'display_name': self.display_name or self.username,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
        }

        if include_sensitive:
            data['password_hash'] = self.password_hash

        return data

    # ============ 类方法（查询快捷方式） ============

    @classmethod
    def find_by_username(cls, username: str) -> 'User':
        """根据用户名查找"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id: str) -> 'User':
        """根据 ID 查找"""
        return cls.query.get(user_id)

    @classmethod
    def find_by_email(cls, email: str) -> 'User':
        """根据邮箱查找"""
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f'<User {self.username}>'
    '''
    把看不懂的对象（因为现在被包装成对象了）“内存地址”翻译成“人话”，让你在 print 调试或看报错时，一眼就能认出这个对象是谁。
    '''

    """
    只查找 id 和 username，不拿密码等其他字段
    return cls.query.with_entities(cls.id, cls.username).filter_by(username=username).first()
    """