from flask import Blueprint
from flask_restful import Api

# 每新增一个模块需要在__init__.py文件中创建蓝图，并且指定路由
elevator = Blueprint('elevator', __name__, url_prefix='/dp/elevator')
elevator_api = Api(elevator)

from data_api.elevator.view import view
