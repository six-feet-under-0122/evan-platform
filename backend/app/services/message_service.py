from app.extensions import db
from app.models.message import Message


class MessageService:

    @staticmethod
    def create(session_id: str, user_id: str, role: str,
               content_json: dict, content_text: str = None,
               model: str = None) -> Message:
        msg = Message(
            session_id=session_id,
            user_id=user_id,
            role=role,
            content_json=content_json,
            content_text=content_text,
            model=model,
        )
        db.session.add(msg)
        db.session.commit()
        return msg

    @staticmethod
    def list_by_session(session_id: str, limit: int = 50,
                        before_id: str = None) -> list:
        return Message.find_by_session(
            session_id, limit=limit, before_id=before_id
        ).all()

    @staticmethod
    def search_in_session(session_id: int, query: str, limit: int = 20):
        """在指定会话中搜索消息"""
        from app.models.message import Message
        from app import db

        # 使用 LIKE 进行模糊搜索
        messages = db.session.query(Message).filter(
            Message.session_id == session_id,
            db.or_(
                Message.content_text.like(f'%{query}%'),
                # 如果想搜索 JSON blocks 里的内容，可以用 JSON 函数
                # 但 SQLite 的 JSON 支持有限，先简单搜索 content_text
            )
        ).order_by(Message.created_at.desc()).limit(limit).all()

        return messages

    @staticmethod
    def search_by_user(user_id: int, query: str, limit: int = 50):
        """搜索用户所有会话的消息"""
        from app.models.message import Message
        from app.models.session import Session
        from app import db

        messages = db.session.query(Message).join(Session).filter(
            Session.user_id == user_id,
            db.or_(
                Message.content_text.like(f'%{query}%'),
            )
        ).order_by(Message.created_at.desc()).limit(limit).all()

        return messages