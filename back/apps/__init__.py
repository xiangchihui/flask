from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from  flask_bcrypt import Bcrypt
import os,logging
from logging.handlers import RotatingFileHandler
from flask_restplus import Api
from flask_sockets import Sockets
from django.conf import settings
settings.configure()



#实例化第三方库
bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()
api = Api()
sockets = Sockets()



def setup_log(config_name):
    """
    :param config_name: 传入日志等级
    :return
    """
    # 设置日志的的登记
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    # 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100,backupCount=100)
    # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
    # 为日志记录器设置记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaks app使用的）加载日志记录器
    logging.getLogger().addHandler(file_log_handler)    

def create_app(config_name):
    app = Flask(
        __name__,
        static_folder='../static'
    )
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    setup_log(config_name)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    sockets.init_app(app)
    app.config.from_object(config[config_name])   # 这里直接拿到的是类的名字，也就是引用
    
    return app

'''
生成环境-produce
开发环境-development
测试环境-test
以上三个值通过config配置
'''
app = create_app('development')

#注册蓝图路由
import apps.system.router as sys_router 
import apps.log.router as logs_router
sys_router.initRoute(api)
logs_router.initRoute(api)

