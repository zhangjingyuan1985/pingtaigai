from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from conf.data_api_config import config_map

db = SQLAlchemy()


# 新增文件需要在app里注册蓝图
def create_app(config_name):
    app = Flask(__name__)
    obj = config_map.get(config_name)
    app.config.from_object(obj)
    db.init_app(app)

    from data_api.ai.view import ai
    app.register_blueprint(ai)

    return app
