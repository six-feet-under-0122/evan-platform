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