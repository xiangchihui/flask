from apps.log import views

def initRoute(api):
    api.add_resource(views.UserLogContraller, '/api/logs',endpoint='/api/logs')
    api.add_resource(views.UserLogContraller, '/api/logs/user',endpoint='/api/logs/user')