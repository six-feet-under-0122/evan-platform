import uuid
from datetime import datetime
from app.extensions import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)

    # 文件信息
    filename = db.Column(db.String(255), nullable=False)  # 原始文件名
    content_type = db.Column(db.String(100), nullable=False)  # image/png, application/pdf
    size_bytes = db.Column(db.Integer, nullable=False)

    # 存储路径（相对路径，实际存在 uploads/ 下）
    storage_path = db.Column(db.String(500), nullable=False, unique=True)

    # 用途标记（可选，以后可以用来区分头像 / 消息附件 / 工具输出）
    purpose = db.Column(db.String(50), default='attachment')  # 'attachment' / 'avatar' / 'tool_output'
    # Python 端的默认值 vs 数据库端的默认值：
    # 在 SQLAlchemy 模型里写的 default=... 是由 Python 应用程序在向数据库插入数据时动态计算并传过去的。
    # Alembic 默认不会把它们生成为数据库层面的 DEFAULT 约束。
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'content_type': self.content_type,
            'size_bytes': self.size_bytes,
            'purpose': self.purpose,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'url': f'/api/files/{self.id}',  # 下载地址
        }

    @classmethod
    def find_by_id(cls, file_id: str):
        return cls.query.filter_by(id=file_id).first()