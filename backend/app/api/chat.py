from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.resp import ok
from app.common.errors import AppError, ErrorCode
from app.services.chat_service import ChatService

bp = Blueprint('chat', __name__)

DEFAULT_MODEL = 'gpt-4o-mini'


@bp.post('/')
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    body = request.get_json(silent=True) or {}

    session_id = body.get('session_id')
    message = body.get('message', '').strip()
    model = body.get('model', DEFAULT_MODEL)
    file_id = body.get('file_id')  # ← 新增，可选

    if not session_id:
        raise AppError(ErrorCode.INVALID_REQUEST, 'session_id 必填')
    if not message:
        raise AppError(ErrorCode.INVALID_REQUEST, 'message 不能为空')

    assistant_msg = ChatService.run_turn(
        session_id=session_id,
        user_id=user_id,
        user_text=message,
        model=model,
        file_id=file_id,  # ← 传进去，没有图片时是 None
    )

    return ok({
        'reply': assistant_msg.content_text,
        'message': assistant_msg.to_dict(),
    })
