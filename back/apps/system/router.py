from apps.system import views


def initRoute(api):
    api.add_resource(views.MenuContraller, '/api/menus',endpoint='/api/menus')
    api.add_resource(views.JobContraller, '/api/job',endpoint='/api/job')
    api.add_resource(views.DictContraller, '/api/dict',endpoint='/api/dict')
    api.add_resource(views.RoleContraller, '/api/roles',endpoint='/api/roles')
    api.add_resource(views.DeptmentContraller, '/api/dept',endpoint='/api/dept')
    api.add_resource(views.UserContraller, '/api/users',endpoint='/api/users')
    api.add_resource(views.DictDetailContraller, '/api/dictDetail',endpoint='/api/dictDetail')
