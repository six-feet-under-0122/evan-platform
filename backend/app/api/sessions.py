from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.resp import ok
from app.services.session_service import SessionService
from app.services.message_service import MessageService


bp = Blueprint('sessions', __name__)


@bp.post('/')
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    body = request.get_json(silent=True) or {}
    session = SessionService.create(
        user_id=user_id,
        title=body.get('title', '新对话'),
        persona=body.get('persona', 'evan'),
        system_prompt=body.get('system_prompt'),
    )
    return ok(session.to_dict(), '会话创建成功',201)


@bp.get('/')
@jwt_required()
def list_sessions():
    user_id = get_jwt_identity()
    limit = min(int(request.args.get('limit', 20)), 100)
    offset = int(request.args.get('offset', 0))
    sessions = SessionService.list_by_user(user_id, limit=limit, offset=offset)
    return ok([s.to_dict() for s in sessions])


@bp.get('/<session_id>')
@jwt_required()
def get_session(session_id):
    user_id = get_jwt_identity()
    session = SessionService.get_or_404(session_id, user_id)
    return ok(session.to_dict())


@bp.patch('/<session_id>')
@jwt_required()
def update_session(session_id):
    user_id = get_jwt_identity()
    body = request.get_json(silent=True) or {}
    session = SessionService.get_or_404(session_id, user_id)
    session = SessionService.update(session, **body)
    return ok(session.to_dict())


@bp.delete('/<session_id>')
@jwt_required()
def delete_session(session_id):
    user_id = get_jwt_identity()
    session = SessionService.get_or_404(session_id, user_id)
    SessionService.delete(session)
    return ok(None, '会话已删除')


@bp.get('/<session_id>/messages')
@jwt_required()
def list_messages(session_id):
    user_id = get_jwt_identity()
    # 先验证这个 session 是不是你的
    SessionService.get_or_404(session_id, user_id)

    limit = min(int(request.args.get('limit', 50)), 100)
    before_id = request.args.get('before_id')

    messages = MessageService.list_by_session(session_id, limit=limit, before_id=before_id)
    return ok([m.to_dict() for m in messages])
