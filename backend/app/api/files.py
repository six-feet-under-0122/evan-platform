from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.resp import ok
from app.services.file_service import FileService

bp = Blueprint('files', __name__)


@bp.post('/')
@jwt_required()
def upload_file():
    """
    上传文件

    请求格式：multipart/form-data
    - file: 文件字段
    - purpose: 用途（可选，默认 'attachment'）
    """
    user_id = get_jwt_identity()

    # 从 request.files 取文件（不是 request.get_json()）
    if 'file' not in request.files:
        return ok(None, '没有上传文件', 400)

    file = request.files['file']
    purpose = request.form.get('purpose', 'attachment')  # form 里的其他字段

    file_record = FileService.upload(user_id, file, purpose)

    return ok(file_record.to_dict(), '上传成功', 201)


@bp.get('/<file_id>')
def download_file(file_id):
    """
    下载文件（无需登录，只要有 file_id 就能访问）

    如果要限制只有上传者能下载，加上：
    @jwt_required()
    file = FileService.get_or_404(file_id, get_jwt_identity())
    """
    file = FileService.get_or_404(file_id)
    full_path = FileService.get_full_path(file)

    # send_file 自动处理文件流、Content-Type、缓存头
    return send_file(
        full_path,
        mimetype=file.content_type,
        as_attachment=False,  # False = 浏览器直接显示；True = 强制下载
        download_name=file.filename,
    )
