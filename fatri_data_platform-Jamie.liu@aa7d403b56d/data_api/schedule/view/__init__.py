from flask import Blueprint
from flask_restful import Api

# 每新增一个模块需要在__init__.py文件中创建蓝图，并且指定路由
schedule = Blueprint('schedule',__name__,url_prefix='/dp/schedule')
schedule_api = Api(schedule)

from data_api.schedule import view
