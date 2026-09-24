from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.common.resp import ok
from app.services.model_service import ModelService


bp = Blueprint('models', __name__)


@bp.get('/')
@jwt_required()
def list_models():
    """获取可用的模型列表"""
    models = ModelService.list_available()
    return ok(models)


@bp.get('/default')
@jwt_required()
def get_default_model():
    """获取默认模型"""
    default = ModelService.get_default()
    return ok({'model': default})