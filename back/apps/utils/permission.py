from flask_jwt_extended import get_jwt_identity
from apps.system.models import *
from flask import jsonify,Response
import json


def PreAuthorize(permission):
    def wrapper(func):
        def inner_wrapper(*args,**kwargs):
            username = get_jwt_identity()
            userobj=User.query.filter_by(username=username).first()
            if userobj.is_admin is  None:
                sql='select permission from sys_menu where id in (select distinct menu_id from sys_role_menus where role_id in (select role_id from sys_users_roles where user_id=(select id from sys_user where username="{}")));'.format(username)
                data=db.session.execute(sql)
                permissions=[ item[0]  for item in data if item[0] != '' ]
                if permission in permissions:
                    return func(*args,**kwargs)
                message = json.dumps({'errors': '没有权限访问，请联系管理员！'})
                return Response(message,status=403,mimetype='application/json')
            else:#如果是超级管理员，跳过权限控制
                return func(*args,**kwargs)
        return inner_wrapper
    
    return wrapper