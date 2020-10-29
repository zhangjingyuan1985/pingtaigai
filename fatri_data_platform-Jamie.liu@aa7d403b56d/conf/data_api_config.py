class Config:
    # 配置MySQL参数
    MYSQL_DIALECT = 'mysql'
    MYSQL_DIRVER = 'pymysql'
    MYSQL_NAME = 'root'
    MYSQL_PWD = 'root'
    MYSQL_HOST = 'hadoop-master'
    MYSQL_PORT = 3306
    MYSQL_DB = 'data_platform'
    MYSQL_CHARSET = 'utf8mb4'

    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DIRVER}://{MYSQL_NAME}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/' \
                              f'{MYSQL_DB}?charset={MYSQL_CHARSET}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    HBASE_HOST = "hadoop-master"
    HBASE_PORT = None
    HBASE_POOL_SIZE = 3
    DEBUG = True


class ProductionConfig(Config):
    HBASE_HOST = "sz-pro-hadoop-srv01"
    HBASE_PORT = None
    HBASE_POOL_SIZE = 5


config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}
