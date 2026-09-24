import uuid
from datetime import datetime
from app.extensions import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    session_id = db.Column(
        db.String(36),
        db.ForeignKey('sessions.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )

    role = db.Column(db.String(20), nullable=False)  # user / assistant / system / tool
    content_json = db.Column(db.JSON, nullable=False)  # blocks 结构
    content_text = db.Column(db.Text, nullable=True)  # 纯文本冗余，方便搜索

    model = db.Column(db.String(100), nullable=True)  # 生成时用的模型，user 消息为 None

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 额，外键连接+relationship连接+backref双向+messages.session.name链式调用对面表的数据；
    # session = db.relationship('Session', backref='messages')
    # 这句话的意思就是在Massage里塞了session,在Session里塞了messages 然后非必要不连接省内存

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'role': self.role,
            'content_json': self.content_json,
            'content_text': self.content_text,
            'model': self.model,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def find_by_session(cls, session_id: str, limit: int = 50, before_id: str = None):
        q = cls.query.filter_by(session_id=session_id)
        if before_id:
            # 无限滚动：拿比 before_id 更早的消息
            anchor = cls.query.get(before_id)
            if anchor:
                q = q.filter(cls.created_at < anchor.created_at)
        return q.order_by(cls.created_at.asc()).limit(limit)