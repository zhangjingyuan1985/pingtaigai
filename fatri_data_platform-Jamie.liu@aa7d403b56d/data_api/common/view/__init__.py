from flask import Blueprint
from flask_restful import Api

# 每新增一个模块需要在__init__.py文件中创建蓝图，并且指定路由
common = Blueprint('common',__name__,url_prefix='/dp/common')
common_api = Api(common)

from data_api.common.view import view
