import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from app.extensions import db
from app.models.file import File
from app.common.errors import AppError, ErrorCode, NotFoundError


class FileService:

    @staticmethod
    def upload(user_id: str, file, purpose: str = 'attachment') -> File:
        """
        上传文件
        Args:
            user_id: 上传者 ID
            file: werkzeug.datastructures.FileStorage 对象（Flask 自动解析的）
            purpose: 用途标记（'attachment' / 'avatar' / 'tool_output'）

        Returns:
            File 对象
        """
        # 校验文件
        if not file or file.filename == '':
            raise AppError(ErrorCode.INVALID_REQUEST, '没有选择文件')

        # 校验文件类型（只允许图片）
        allowed_types = {'image/png', 'image/jpeg', 'image/gif', 'image/webp'}
        if file.content_type not in allowed_types:
            raise AppError(
                ErrorCode.INVALID_REQUEST,
                f'不支持的文件类型: {file.content_type}'
            )

        # 校验文件大小（最大 10MB）
        file.seek(0, os.SEEK_END)  # 移动到文件末尾
        size_bytes = file.tell()  # 获取当前位置（文件大小）
        file.seek(0)  # 移回开头，准备读取

        max_size = 10 * 1024 * 1024  # 10MB
        if size_bytes > max_size:
            raise AppError(ErrorCode.INVALID_REQUEST, '文件大小超过 10MB')

        # 生成安全的文件名（防止路径注入）
        original_filename = secure_filename(file.filename)
        ext = os.path.splitext(original_filename)[1]  # 提取扩展名 '.png'
        unique_filename = f"{uuid.uuid4()}{ext}"  # 'abc123.png'

        # 构造存储路径（相对路径）
        # 按日期分目录：uploads/2026/07/10/abc123.png
        from datetime import datetime
        date_path = datetime.utcnow().strftime('%Y/%m/%d')
        storage_path = os.path.join(date_path, unique_filename)

        # 保存文件到磁盘
        upload_dir = current_app.config['UPLOAD_FOLDER']  # 'uploads/'
        full_dir = os.path.join(upload_dir, date_path)
        os.makedirs(full_dir, exist_ok=True)  # 确保目录存在

        full_path = os.path.join(upload_dir, storage_path)
        file.save(full_path)

        # 保存记录到数据库
        file_record = File(
            user_id=user_id,
            filename=original_filename,
            content_type=file.content_type,
            size_bytes=size_bytes,
            storage_path=storage_path,
            purpose=purpose,
        )
        db.session.add(file_record)
        db.session.commit()

        return file_record

    @staticmethod
    def get_or_404(file_id: str, user_id: str = None) -> File:
        """
        获取文件，校验归属（可选）=>可以先不登录
        Args:
            file_id: 文件 ID
            user_id: 如果提供，校验文件是否属于该用户
        """
        file = File.find_by_id(file_id)
        if not file:
            raise NotFoundError('文件不存在')

        # 归属校验（可选）
        if user_id and file.user_id != user_id:
            raise AppError(ErrorCode.FORBIDDEN, '无权访问该文件', 403)

        return file

    @staticmethod
    def get_full_path(file: File) -> str:
        """获取文件的完整磁盘路径"""
        from flask import current_app
        return os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            file.storage_path
        )
