"""
会话（Session）模型
"""

import uuid
from datetime import datetime
from app.extensions import db


class Session(db.Model):
    """对话会话表"""

    __tablename__ = 'sessions'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(200), nullable=False, default='新对话')
    persona = db.Column(db.String(50), nullable=False, default='evan')
    system_prompt = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='sessions')

    def to_dict(self) -> dict:
        """转成字典（用于 API 返回）"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'persona': self.persona,
            'system_prompt': self.system_prompt,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def find_by_id(cls, session_id: str) -> 'Session':
        """根据 ID 查找"""
        return cls.query.get(session_id)#有个什么一级缓存，搜索过的可以直接从内存里拿数据，应该是这个意思

    @classmethod
    def find_by_user(cls, user_id: str):
        """
        查某个用户的所有会话（按更新时间倒序）
        返回的是query而不是.all()方便上层继续接 .limit()/.offset()分页等功能。
        """
        return cls.query.filter_by(user_id=user_id).order_by(cls.updated_at.desc())

    def __repr__(self):
        return f'<Session {self.id} title={self.title!r}>'
