from app.extensions import db
from app.models.session import Session
from app.common.errors import AppError, ErrorCode


class SessionService:

    @staticmethod
    def create(user_id: str, title: str = '新对话', persona: str = 'evan',
               system_prompt: str = None) -> Session:
        session = Session(
            user_id=user_id,
            title=title.strip() if title else '新对话',
            persona=persona,
            system_prompt=system_prompt,
        )
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def list_by_user(user_id: str, limit: int = 20, offset: int = 0):
        return (
            Session.find_by_user(user_id)
            .limit(limit)
            .offset(offset)
            .all()
        )

    @staticmethod
    def get_or_404(session_id: str, user_id: str) -> Session:
        """获取会话，同时验证归属权"""
        session = Session.find_by_id(session_id)
        if not session:
            raise AppError(ErrorCode.NOT_FOUND, 'Session not found')
        if session.user_id != user_id:
            raise AppError(ErrorCode.FORBIDDEN, 'Access denied')
        return session

    @staticmethod
    def update(session: Session, **kwargs) -> Session:
        allowed = {'title', 'persona', 'system_prompt'}
        for key, value in kwargs.items():
            if key in allowed and value is not None:
                setattr(session, key, value)
        db.session.commit()
        return session

    @staticmethod
    def delete(session: Session):
        db.session.delete(session)
        db.session.commit()
