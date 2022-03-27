from apps import db
from apps.utils.basemodels import BaseModel
from datetime import datetime
from apps.utils.common import menu_tree
from sqlalchemy.orm import relationship

class User(BaseModel):

    __tablename__='sys_user'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    #dept_id = db.Column(db.BigInteger)
    dept_id = db.Column(db.BigInteger,db.ForeignKey('sys_dept.id'))
    # job_id  = db.Column(db.BigInteger)
    # role_id = db.Column(db.BigInteger)
    username = db.Column(db.String(255))
    nick_name = db.Column(db.String(255))
    gender = db.Column(db.Boolean)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    avatar_name = db.Column(db.String(255))
    avatar_path = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean)
    enabled = db.Column(db.Boolean)
    pwd_reset_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    def init_permission(self):
        if self.is_admin: #如果是管理员，拥有全部的权限
            roles = ['admin']
            user_dict ={
                'avatarName':self.avatar_name,
                'avatarPath':self.avatar_path,
                'createTime':datetime.timestamp(self.create_time),
                'dept': {
                    'id':self.dept_id,
                    'name':Deptment.query.get(self.dept_id).name
                },
                'email':self.email,
                'enabled':self.enabled,
                'gender':  '男' if self.gender else '女',
                'id':self.id,
                'jobs': [ item.model_to_dict() for item in User.query.get(self.id).sys_jobs],
                'roles':[ item.model_to_dict() for item in User.query.get(self.id).sys_roles],
                'nickName':self.nick_name,
                'username':self.username,
                'phone':self.phone,
                'updateTime':datetime.timestamp(self.update_time),

            }
            return {'user':user_dict,'roles':roles}
        else: #普通用户登录权限初始化
            sql='select permission from sys_menu where id in (select distinct menu_id from sys_role_menus where role_id in (select role_id from sys_users_roles where user_id={}));'.format(self.id)
            data=db.session.execute(sql)
            permission=[ item[0]  for item in data if item[0] != '' ]
            user_dict ={
                'avatarName':self.avatar_name,
                'avatarPath':self.avatar_path,
                'createTime':datetime.timestamp(self.create_time),
                'dept': {
                    'id':self.dept_id,
                    'name':Deptment.query.get(self.dept_id).name
                },
                'email':self.email,
                'enabled':self.enabled,
                'gender':  '男' if self.gender else '女',
                'id':self.id,
                'jobs': [ item.model_to_dict() for item in User.query.get(self.id).sys_jobs],
                'nickName':self.nick_name,
                'username':self.username,
                'phone':self.phone,
                'roles':[ item.model_to_dict() for item in User.query.get(self.id).sys_roles],
                'updateTime':datetime.timestamp(self.update_time),

            }
            return {'user':user_dict,'roles':permission}
            
    def init_menu(self):
        if self.is_admin:
            menuobj=Menu.query.filter(Menu.type != 2).all()
            menu_data=[]
            for item in menuobj:
                menu_dict = {
                    'id':item.id,
                    'pid':item.pid,
                    "alwaysShow": True,
                    "component": 'Layout' if item.pid == 0 else item.component,
                    "hidden": bool(item.hidden) ,
                    "meta": {
                        "icon": item.icon,
                        "noCache": bool(item.cache),
                        "title": item.title                    
                    },                    
                    "name":item.name,
                    "path":'/'+item.path if item.pid == 0 else item.path,
                    "redirect":"noredirect",
                }                
                menu_data.append(menu_dict)
            return menu_tree(menu_data,0,'pid','id')
        else:
            sql="select * from sys_menu where id in (select distinct menu_id from sys_role_menus where role_id in (select role_id from sys_users_roles where user_id={})) and type != 2 order by menu_sort;".format(self.id)
            data = db.session.execute(sql)
            menu_data=[]
            for item in data:
                menu_dict = {
                    'id':item.id,
                    'pid':item.pid,
                    "alwaysShow": True,
                    "component": 'Layout' if item.pid == 0 else item.component,
                    "hidden": bool(item.hidden) ,
                    "meta": {
                        "icon": item.icon,
                        "noCache": bool(item.cache),
                        "title": item.title                    
                    },                    
                    "name":item.name,
                    "path": '/'+item.path if item.pid == 0 else item.path,
                    "redirect":"noredirect",
                }
                menu_data.append(menu_dict)

            return menu_tree(menu_data,0,'pid','id')
            

    def model_to_dict(self):
        
        user_dict={
            'dept':{
                'id':self.dept_id,
                'name':Deptment.query.get(self.dept_id).name,
            },
            'email':self.email,
            'enabled':self.enabled,
            'avatarPath':self.avatar_path,
            'avatarName':self.avatar_name,
            'gender':'男' if self.gender else '女',
            'id':self.id,
            'jobs': [ item.model_to_dict() for item in User.query.get(self.id).sys_jobs],
            'nickName':self.nick_name,
            'phone':self.phone,
            'roles':[ item.model_to_dict() for item in User.query.get(self.id).sys_roles],
            'username':self.username,
            'createTime':datetime.strftime(self.create_time, '%Y-%m-%d %H:%M:%S')
        }
        return user_dict

    def __repr__(self):
        return '<name %r>' % self.username
    
    
class Deptment(BaseModel):

    __tablename__ = 'sys_dept'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True,comment='ID')
    pid =  db.Column(db.BigInteger,comment='上级部门')
    sub_count = db.Column(db.Integer,comment='子部门数目')
    name =  db.Column(db.String(255),comment='名称')
    dept_sort =  db.Column(db.Integer,comment='部门排序')
    enabled = db.Column(db.Boolean,comment='状态：1启用、0禁用')
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    relate_users = db.relationship("User",backref='relate_deptement',lazy='dynamic')
   
    def model_to_dict(self):
        dept_dict={
           'createTime':datetime.strftime(self.create_time, '%Y-%m-%d %H:%M:%S'), #正常时间格式 
           'deptSort':self.dept_sort,
           'enabled':self.enabled,
           'id':self.id,
           'pid':self.pid,
           'name':self.name,
           'label':self.name,
           'hasChildren': self.sub_count > 0,
           'leaf':self.sub_count <=0,
           'subCount':self.sub_count
        }
        return dept_dict
    def to_dict(self):
        dept_tree_dict={
          'id':self.id,
          'pid':self.pid,
          'name':self.name,
          'enabled':self.enabled,
        }
        return dept_tree_dict
    def __repr__(self):
        return '<name %r>' % self.name


class Dict(BaseModel):

    __tablename__ = 'sys_dict'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 将 sys_dict_detail 与 sys_dict 创建关系 这个不是字段,只是关系,backref是反向关联的关键字
    details = relationship('DictDetail',backref='_dict')

class DictDetail(BaseModel):
    __tablename__ = 'sys_dict_detail'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    #dict_id = db.Column(db.BigInteger)
    # 关联字段,让class_id 与 class 的 id 进行关联,主外键关系(这里的ForeignKey一定要是表名.id不是对象名)
    dict_id = db.Column(db.BigInteger,db.ForeignKey('sys_dict.id'))
    label = db.Column(db.String(255))
    value = db.Column(db.String(255))
    dict_sort = db.Column(db.Integer)
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



class Job(BaseModel):

    __tablename__ = 'sys_job'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    name =  db.Column(db.String(255))
    enabled = db.Column(db.Boolean)
    job_sort = db.Column(db.Integer)
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    user=db.relationship('User',secondary='sys_users_jobs',backref=db.backref('sys_jobs',lazy=True))



class Menu(BaseModel):
    """
    导航菜单模型
    """
    __tablename__ = 'sys_menu'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True,comment='ID')
    pid = db.Column(db.BigInteger,comment='上级菜单ID')
    sub_count =  db.Column(db.Integer,default=0,comment='子菜单数目')
    type =  db.Column(db.Integer,comment='菜单类型')
    title = db.Column(db.String(255),comment='菜单标题')
    name = db.Column(db.String(255),comment='组件名称')
    component = db.Column(db.String(255),comment='组件')
    menu_sort =  db.Column(db.Integer,comment='排序')
    icon = db.Column(db.String(255),comment='图标')
    path = db.Column(db.String(255),comment='链接地址')
    i_frame = db.Column(db.Boolean,comment='是否外链')
    cache = db.Column(db.Boolean,comment='缓存')
    hidden = db.Column(db.Boolean,comment='隐藏')
    permission = db.Column(db.String(255),comment='权限')
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        
    def menut_list(self):
        menut_dict = {
            'cache':self.cache,
            'createTime':datetime.strftime(self.create_time, '%Y-%m-%d %H:%M:%S'),
            'hasChildren': self.sub_count > 0,
            'hidden':self.hidden,
            'iFrame':self.i_frame,
            'icon':self.icon,
            "id": self.id,
            'label':self.title,
            'menuSort':self.menu_sort,
            'permission':self.permission,
            'componentName':self.name,
            'component':self.component,
            'path':self.path,
            'subCount':self.sub_count,
            'title':self.title,
            'type':self.type,
            'pid':self.pid,
            'leaf':self.sub_count <=0
            
        }
        return menut_dict


class Role(BaseModel):

    __tablename__ = 'sys_role'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    level = db.Column(db.Integer)
    description = db.Column(db.String(255))
    data_scope = db.Column(db.String(255))
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),onupdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    user=db.relationship('User',secondary='sys_users_roles',backref=db.backref('sys_roles',lazy=True))
    menus=db.relationship('Menu',secondary='sys_role_menus',backref=db.backref('sys_roles',lazy=True))

    def model_to_dict(self):
        role=Role.query.get(self.id)
        menus=[ item.menut_list() for item in role.menus]

        role_dict={
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'description':self.description,
            'data_scope':self.data_scope,
            'create_time':datetime.strftime(self.create_time, '%Y-%m-%d %H:%M:%S'),
            'menus': menus
        }
        return role_dict


class RoleToMenu(db.Model):
    __tablename__ = 'sys_role_menus'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    menu_id = db.Column(db.BigInteger,db.ForeignKey('sys_menu.id'))
    role_id = db.Column(db.BigInteger,db.ForeignKey('sys_role.id'))


class UsersToRoles(db.Model):
    __tablename__ = 'sys_users_roles'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('sys_user.id'))
    role_id = db.Column(db.BigInteger,db.ForeignKey('sys_role.id'))



class UsersToJobs(db.Model):
    __tablename__ = 'sys_users_jobs'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('sys_user.id'))
    job_id = db.Column(db.BigInteger,db.ForeignKey('sys_job.id'))

class SystemLog(BaseModel):

    __tablename__ = 'sys_log'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    description = db.Column(db.String(255))
    log_type = db.Column(db.String(255))
    method = db.Column(db.String(255))
    params = db.Column(db.String(255))
    request_ip = db.Column(db.String(255))
    time = db.Column(db.String(255))
    username = db.Column(db.String(255))
    address = db.Column(db.String(255))
    browser =db.Column(db.String(255))
    system =  db.Column(db.String(255))
    exception_detail = db.Column(db.String(255))
    create_time = db.Column(db.DateTime,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))












