from apps import db,app,api
from flask_script import Manager,Server,Shell
from  flask_migrate import MigrateCommand,Migrate
from apps.system.models import *
 



#注册蓝图
from apps.system.views import systembp
from apps.log.views import logsbp

app.register_blueprint(systembp)
app.register_blueprint(logsbp)


manager = Manager(app)
migrate  = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db)

manager.add_command('runserver',Server('0.0.0.0',port=5000))
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)


@manager.command
def rungevent():
    import werkzeug.serving
    from werkzeug.debug import DebuggedApplication
    from geventwebsocket.handler import WebSocketHandler
    from gevent import pywsgi
    

    @werkzeug.serving.run_with_reloader
    def run():
        # app.debug =True
        # dapp = DebuggedApplication(app,evalex=True)
        ws = pywsgi.WSGIServer(('0.0.0.0', 5000),application=app, handler_class=WebSocketHandler)
        ws.serve_forever()

if __name__ == "__main__":
    manager.run()