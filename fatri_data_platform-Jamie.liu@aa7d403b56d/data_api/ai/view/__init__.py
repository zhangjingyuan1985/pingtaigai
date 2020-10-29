from flask import Blueprint
from flask_restful import Api

# 每新增一个模块需要在__init__.py文件中创建蓝图，并且指定路由
ai = Blueprint('ai',__name__,url_prefix='/dp/ai')
ai_api = Api(ai)

from data_api.ai.view import view