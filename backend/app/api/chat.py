import json
from flask import Blueprint, request, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.resp import ok
from app.common.errors import AppError, ErrorCode
from app.services.chat_service import ChatService
from app.utils.decorators import require_json_fields

bp = Blueprint('chat', __name__)

DEFAULT_MODEL = 'gpt-4o-mini'

@bp.post('/')
@jwt_required()
@require_json_fields('session_id', 'message')
def chat():
    user_id = get_jwt_identity()
    body = request.get_json()

    session_id = body['session_id']#直接取，不用 .get()
    #- .get('key') → 不存在时返回 None，不报错
    #- ['key'] → 不存在时直接抛 KeyError
    message = body['message'].strip()
    model = body.get('model', DEFAULT_MODEL)
    file_id = body.get('file_id')

    if not message:#因为装饰器只检查字段存在不存在，不检查空字符串
        raise AppError(ErrorCode.INVALID_REQUEST, 'message 不能为空')

    user_msg, assistant_msg = ChatService.run_turn(
        session_id=session_id,
        user_id=user_id,
        user_text=message,
        model=model,
        file_id=file_id,
    )

    return ok({
        'reply': assistant_msg.content_text,
        'user_message': user_msg.to_dict(),      # ← 新增：返回用户消息
        'assistant_message': assistant_msg.to_dict(),
    })


@bp.post('/stream')
@jwt_required()
@require_json_fields('session_id', 'message')
def chat_stream():
    user_id = get_jwt_identity()
    body = request.get_json()

    session_id = body['session_id']
    message = body['message'].strip()
    model = body.get('model', DEFAULT_MODEL)
    file_id = body.get('file_id')

    if not message:
        raise AppError(ErrorCode.INVALID_REQUEST, 'message 不能为空')

    def generate():
        try:
            for chunk in ChatService.run_turn_stream(
                session_id=session_id,
                user_id=user_id,
                user_text=message,
                model=model,
                file_id=file_id,
            ):
                yield f"data: {chunk}\n\n"
            # ⭐ 改：循环结束后再发送 [DONE]
            yield "data: [DONE]\n\n"
        except AppError as e:
            yield f"event: error\ndata: {json.dumps({'code': e.code, 'message': e.message})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
    )