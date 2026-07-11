from flask import current_app
from app.models.message import Message
from app.models.file import File
from app.services.message_service import MessageService
from app.services.session_service import SessionService
from app.providers.llm.chatanywhere import ChatAnywhereProvider, blocks_to_openai_content
from app.common.errors import AppError, ErrorCode

_provider = ChatAnywhereProvider()


class ChatService:

    @staticmethod
    def run_turn(session_id: str, user_id: str,
                 user_text: str, model: str,
                 file_id: str = None) -> Message:  # ← 新增 file_id 参数

        # 1. 验证 session 归属
        session = SessionService.get_or_404(session_id, user_id)

        # 2. 组装用户消息的 blocks
        blocks = [{'type': 'text', 'text': user_text}]

        if file_id:
            # 找到文件记录，把图片信息加进 blocks
            file = File.find_by_id(file_id)
            if not file or file.user_id != user_id:
                raise AppError(ErrorCode.NOT_FOUND, '文件不存在或无权访问', 404)

            blocks.append({
                'type': 'image',
                'file_id': file.id,
                'storage_path': file.storage_path,  # 磁盘路径（给 provider 读文件用）
                'content_type': file.content_type,  # 'image/png'（给 base64 前缀用）
                #provider之后会从block里面拿地址id什么的再转换成base64(暂时)
                'filename': file.filename,
            })

        # 3. 保存用户消息
        user_msg = MessageService.create(
            session_id=session_id,
            user_id=user_id,
            role='user',
            content_json={'blocks': blocks},
            content_text=user_text,  # 纯文本冗余（图片不计入纯文本）
        )

        # 4. 拉取最近 20 条历史，组装成 LLM 格式
        history = MessageService.list_by_session(session_id, limit=20)
        messages = _build_messages(session, history, current_app.config['UPLOAD_FOLDER'])

        # 5. 调用 LLM
        reply_text = _provider.chat(messages, model)

        # 6. 保存 assistant 回复
        assistant_msg = MessageService.create(
            session_id=session_id,
            user_id=user_id,
            role='assistant',
            content_json={'blocks': [{'type': 'text', 'text': reply_text}]},
            content_text=reply_text,
            model=model,
        )

        return assistant_msg


def _build_messages(session, history: list, upload_folder: str) -> list:
    """把数据库里的消息组装成 LLM API 需要的格式"""
    messages = []

    # system prompt
    system_prompt = session.system_prompt or '你是 Evan，一个智能助理。'
    messages.append({'role': 'system', 'content': system_prompt})

    for msg in history:
        if msg.role not in ('user', 'assistant'):
            continue

        blocks = msg.content_json.get('blocks', [])

        # 判断这条消息有没有图片
        has_image = any(b['type'] == 'image' for b in blocks)

        if has_image:
            # 有图片：用 blocks 转换成 OpenAI 视觉格式（content 是列表）
            content = blocks_to_openai_content(blocks, upload_folder)
        else:
            # 纯文本：content 直接是字符串（省 token）
            content = msg.content_text or ''

        messages.append({'role': msg.role, 'content': content})

    return messages
