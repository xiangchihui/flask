import os, logging
from datetime import timedelta

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'n@!t!m(okei_f(!sexwhk@co0ilc=@a1l!z!7rvq408rnw*&k4'
    DEBUG=True
    JWT_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_ACCESS_TOKEN_EXPIRES=30000 #token过去时间
    #设置日志等级
    LOG_LEVEL = logging.DEBUG
    # PERMANENT_SESSION_LIFETIME = timedelta(seconds=1*60)

    
    @staticmethod
    def init_app(app):
        pass
    


#开发环境配置文件
class DevelopemntConfig(BaseConfig):

    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'eladmin'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=UTF8MB4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)



#生成环境配置文件
class  ProduceConfig(BaseConfig):
    DEBUG=False
    LOG_LEVEL = logging.WARNING

#测试环境配置文件
class TestConfig(BaseConfig):
    pass


config = {
    'development': DevelopemntConfig,
    'produce': ProduceConfig,
    'test': TestConfig,
}

