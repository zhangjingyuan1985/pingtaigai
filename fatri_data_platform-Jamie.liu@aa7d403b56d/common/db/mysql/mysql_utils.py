from conf.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.model.kafka_model import Base


class Mysql(object):
    def __init__(self, host=Config().get_conf("Mysql-sqlalchemy", "mysql.host"),
                 port=int(Config().get_conf("Mysql-sqlalchemy", "mysql.port")),
                 user=Config().get_conf("Mysql-sqlalchemy", "mysql.user"),
                 passwd=Config().get_conf("Mysql-sqlalchemy", "mysql.passwd"),
                 db=Config().get_conf("Mysql-sqlalchemy", "mysql.dbname"),
                 charset=Config().get_conf("Mysql-sqlalchemy", "mysql.charset")
                 ):
        self.sqlalchemy_database_uri = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/' \
                                       f'{db}?charset={charset}'

        engine = create_engine(self.sqlalchemy_database_uri)
        Base.metadata.create_all(engine)
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def close(self):
        self.session.close()

    def rollback(self):
        self.session.rollback()


# if __name__ == '__main__':
#     user = 'root'
#     passwd = 'root'
#     host = 'hadoop-master'
#     port = 3306
#     dbname = 'data_platform'
#     charset = 'utf8mb4'
#     mysql = Mysql(host, port, user, passwd, dbname, charset)
    # mysql.session.query(KafkaLog).filter(KafkaLog.topic == "wc", KafkaLog.partition == 0).update()
