from flask_script import Manager
from data_api.schedule import create_app,db

# app = create_app('develop')
app = create_app('product')

manager = Manager(app=app)


@manager.command
def hello():
    pass


if __name__ == '__main__':
    # 启动 python schedule_manage.py runserver -h 0.0.0.0 -p 1234
    manager.run()
