from flask import Blueprint,jsonify,request,session
import json,logging,time,random,base64
from uuid import uuid4
from io import BytesIO
from apps.system.models import *
from apps import jwt,bcrypt,app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,jwt_optional,get_jwt_claims
)
from apps.utils.logfunc import UserRecord
from apps.utils.permission import PreAuthorize
from apps.utils.common import ArithmeticCaptchaAbstract,random_color,dept_tree,generate_name
from apps.utils.rsaEncrypt import decrypt_func
import os
from datetime import datetime
from flask_restplus import Resource,marshal,fields
from sqlalchemy import or_,and_

systembp=Blueprint('system',__name__)

BASE_DIR=os.path.dirname(os.path.abspath(__name__))
UPLOAD_DIR=os.path.join(BASE_DIR,'static/avatar')


@systembp.route('/auth/login',methods=['post'])
def login():
    try:
        if not request.is_json:
            return jsonify({'status':400,'message':'Missing JSON in request'})
        print(request.form)
        data= json.loads(request.get_data()) #获取前端提交过来的json数据
        print(data)
        username = data.get('username',None)
        password = data.get('password',None)      
        # code = data.get('code',None)
        # _uuid = data.get('uuid',None)
        # if not code:
        #    return jsonify({"status":400,"message": "请输入验证码!"}), 400
        
        # if session.get(_uuid) is None:
        #     return jsonify({"status":400,"message": "验证码不存在或已过期"}), 400
        # if session.get(_uuid) == int(code):
        password = decrypt_func(os.path.abspath(os.curdir)+'/apps/utils/clinet_private.pem',password)
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"status":400,"message": "{} 用户不存在!".format(username)}), 400
        if not bcrypt.check_password_hash(user.password,password):
            app.logger.warning("{} 用户密码不正确!".format(username))
            return jsonify({"status":400,"message": "{} 用户密码不正确!".format(username)}), 400
        if not user.enabled:
            return jsonify({"status":400,"message": "{} 用户未激活!".format(username)}), 400
        app.logger.info("{}用户登陆成功".format(username))
        access_token = create_access_token(identity=user.username)
        session[username]=user.init_permission().get('roles')
        return jsonify({'status':200,'user':user.init_permission(),'token':'Bearer '+access_token})
        # else:
        #     return jsonify({"status":400,"message": "输入的验证码有误"}), 400        
    except Exception as e:
        app.logger.error(e)


#待完善的接口
@systembp.route('/auth/info')
@jwt_required
def auth_info():
    try:
        username= get_jwt_identity() #获取登陆成功的用户名
        user = User.query.filter_by(username=username).first()
        return jsonify(user.init_permission())
    except Exception as e:
         print(e)



@systembp.route('/api/users/updatePass',methods=['post'])
@jwt_required
def updatePass():
    try:
        if not request.is_json:
            return jsonify({'status':400,'message':'Missing JSON in request'})
        if not request.get_data() :
            return jsonify({'status':400,'message':'没有获取数据'})
        
        username= get_jwt_identity() #获取登陆成功的用户名
        if username is not None:
            oldpass = decrypt_func(os.path.abspath(os.curdir)+'/apps/utils/clinet_private.pem',json.loads(request.get_data()).get('oldPass'))
            newpass = decrypt_func(os.path.abspath(os.curdir)+'/apps/utils/clinet_private.pem',json.loads(request.get_data()).get('newPass'))
            userobj=User.query.filter_by(username=username).first()
            if bcrypt.check_password_hash(userobj.password,oldpass):
                userobj.password = bcrypt.generate_password_hash(newpass),
                userobj.updatePass = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.session.commit()
                return jsonify({'status':200,'message':'密码修改成功'}),200
            else:
                return jsonify({'status':400,'message':'原始密码输入有误'}),400
        else:
            return jsonify({'status':400,'message':'未登陆'}),400
    except Exception as e:
         print(e)


#图像上传函数
@systembp.route('/api/users/updateAvatar',methods=['post'])
@jwt_required
@UserRecord(request,'上传头像') 
def updateAvatar():
    try:
        images = request.files.get('avatar')
        username= get_jwt_identity() #获取登陆成功的用户名
        avatar_name=generate_name()+'.png'
        filepath = os.path.join(UPLOAD_DIR,username) #每个用户一个文件夹保存头像图片
        if os.path.exists(filepath) is not True: #判断目录是否存在
            os.mkdir(filepath)
        
        avatar_path=os.path.join(filepath,avatar_name)
        images.save(avatar_path)

        #把图片路径信息写入对应用户记录中
        User.query.filter_by(username=username).update({
            'avatar_name':avatar_name,
            'avatar_path':'/static/avatar/{}/{}'.format(username,avatar_name)
        })
        db.session.commit()
        return jsonify({'status':200,'message':'头像上传成功'})
    except Exception as e:
         print(e)

@systembp.route('/api/menus/build',methods=['get'])
@jwt_required
def build_menu():
    try:
        user= get_jwt_identity()
        userobj=User.query.filter_by(username=user).first()
        return jsonify(userobj.init_menu())
    except Exception as e:
        app.logger.error(e)

@systembp.route('/api/menus/superior',methods=['post'])
def get_superior():
    try:
        menuobj=Menu.query.filter_by(pid=0).all()
        return jsonify([item.menut_list() for item in menuobj])
    except Exception as e:
         print(e)

@systembp.route('/api/menus/lazy')
def menus_lazy():
    try:
        menuobj=Menu.query.filter_by(pid=request.args.get('pid')).all()
        return jsonify([item.menut_list() for item in menuobj])
    except Exception as e:
         print(e)


class MenuContraller(Resource):

    @jwt_required
    @PreAuthorize("menu:list")
    def get(self):
        try:
            if request.args.get('pid') is None:
               menuobj=Menu.query.filter_by(pid=0).order_by(Menu.menu_sort.asc()).all()
            else:
               menuobj=Menu.query.filter_by(pid=request.args.get('pid')).order_by(Menu.menu_sort.asc()).all()
            return {'status':200,'content':[item.menut_list() for item in menuobj]},200
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("menu:add")    
    def post(self):
        try:
            postdata=json.loads(request.get_data())
            postobj=Menu(
                pid=postdata.get('pid'),
                type=postdata.get('type'),
                title=postdata.get('title'),
                name = postdata.get('componentName'),
                component = postdata.get('component'),
                menu_sort= postdata.get('menuSort'),
                icon = postdata.get('icon'),
                cache=postdata.get('cache'),
                i_frame=postdata.get('iframe'),
                hidden=postdata.get('hidden'),
                path=postdata.get('path'),
                permission=postdata.get('permission'),
            ).save()
            if int(postdata.get('type')) !=0:
                menuobj=Menu.query.get(postdata.get('pid'))
                menuobj.sub_count+=1
                db.session.commit()
            return {'status':200,'message':'数据添加成功'}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("menu:edit")  
    def put(self):
        try:
            postdata=json.loads(request.get_data())
            Menu.query.filter_by(id=postdata.get('id')).update({
                'pid':postdata.get('pid'),
                'type':postdata.get('type'),
                'title':postdata.get('title'),
                'name' : postdata.get('componentName'),
                'component': postdata.get('component'),
                'menu_sort':postdata.get('menuSort'),
                'icon' : postdata.get('icon'),
                'cache':postdata.get('cache'),
                'i_frame':postdata.get('iframe'),
                'hidden':postdata.get('hidden'),
                'path':postdata.get('path'),
                'permission':postdata.get('permission')                
            })
            db.session.commit()
            return {'status':200,'message':'数据修改成功'}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("menu:del")  
    def delete(self):
        try:
             pass
        except Exception as e:
             print(e)









#岗位管理视图函数
class JobContraller(Resource):
    @jwt_required
    @PreAuthorize("job:list")
    def get(self):
        try:
            if not request.args.get('name') and not  request.args.get('enabled'):
                jobobj=Job.query.order_by(Job.job_sort).offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()
            elif request.args.get('enabled') and request.args.get('name'):
                jobobj=Job.query.filter(
                    or_(
                       Job.name.like('%{}%'.format(request.args.get('name'))),
                       Job.enabled==int(request.args.get('enabled'))
                    )
                ).order_by(Job.job_sort).offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()

            elif request.args.get('enabled'):
                jobobj=Job.query.filter_by(enabled=bool(int(request.args.get('enabled')))).order_by(Job.job_sort).offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()           
            else:
                jobobj=Job.query.filter(
                    or_(
                       Job.name.like('%{}%'.format(request.args.get('name'))),
                    )
                ).order_by(Job.job_sort).offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()

            return {'status':200,'content':[item.model_to_dict() for item in jobobj ],'totalElements':len(jobobj)},200
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("job:add")
    @UserRecord(request,'添加岗位')  
    def post(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            Job(
                name=json.loads(request.get_data()).get('name'),
                enabled=json.loads(request.get_data()).get('enabled'),
                job_sort=json.loads(request.get_data()).get('job_sort')
            ).save()
            return {'status':200,'message':'{}岗位新增成功!'.format(json.loads(request.get_data()).get('name'))}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("job:edit")
    @UserRecord(request,'修改岗位')
    def put(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400
            Job.query.filter(Job.id==int(json.loads(request.get_data()).get('id'))).update({
                'name':json.loads(request.get_data()).get('name'),
                'enabled':json.loads(request.get_data()).get('enabled'),
                'job_sort':json.loads(request.get_data()).get('job_sort')
            })
            db.session.commit()
            return {'status':200,'message':'数据修改成功'},200
        except Exception as e:
             print(e)
    
    
    @jwt_required
    @PreAuthorize("job:del")
    @UserRecord(request,'删除岗位')  
    def delete(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400
            for id in json.loads(request.get_data()):
               Job.query.get(int(id)).delete()
            return {'status':200,'message':'数据删除成功'},200
        except Exception as e:
             print(e)

#字典管理视图函数
class DictContraller(Resource):

    @jwt_required
    @PreAuthorize("dict:list")
    def get(self):
        try:
            if not request.args.get('blurry'):
                dictobj=Dict.query.offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()
            else:
                dictobj = Dict.query.filter(
                    or_(
                        Dict.name.like('%{}%'.format(request.args.get('blurry'))),
                        Dict.description.like('%{}%'.format(request.args.get('blurry')))
                    )
                ).offset(
                    int(request.args.get('page'))*int(request.args.get('size'))
                ).limit(int(request.args.get('size'))).all()
            return {'status':200,'content':[ item.model_to_dict() for item in dictobj],'totalElements':len(dictobj)}
        except Exception as e:
             print(e)


    @jwt_required
    @PreAuthorize("dict:edit") 
    @UserRecord(request,'修改字典')    
    def put(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400

            Dict.query.filter_by(id=json.loads(request.get_data()).get('id')).update({
                'name':json.loads(request.get_data()).get('name'),
                'description':json.loads(request.get_data()).get('description'),
            })
            db.session.commit()
            return {'status':200,'message':'{}修改成功!'.json.loads(request.get_data()).get('name')},200      
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("dict:add") 
    @UserRecord(request,'添加字典')     
    def post(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}

            Dict(
                name=json.loads(request.get_data()).get('name'),
                description=json.loads(request.get_data()).get('description')
            ).save()
            return {'status':200,'message':'{}新增成功!'.format(json.loads(request.get_data()).get('name'))}          
        except Exception as e:
             print(e)


    @jwt_required
    @PreAuthorize("dict:del")
    @UserRecord(request,'删除字典')   
    def delete(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'}),400
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400
            for id in json.loads(request.get_data()):
                #先删除DictDetail关联的数据
                DictDetail.query.filter(DictDetail.dict_id==int(id)).delete()
                Dict.query.get(int(id)).delete()
            return {'status':200,'message':'数据删除成功'},200       
        except Exception as e:
             print(e)

#字典详情视图函数
class DictDetailContraller(Resource):

    @jwt_required
    @PreAuthorize("dict:add") 
    @UserRecord(request,'添加字典值')        
    def post(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            DictDetail(
                dict_id=json.loads(request.get_data()).get('dict').get('id'),
                label=json.loads(request.get_data()).get('label'),
                value=json.loads(request.get_data()).get('value'),
                dict_sort=json.loads(request.get_data()).get('dict_sort')
            ).save()
            return {'status':200,'message':'{}新增成功!'.format(json.loads(request.get_data()).get('label'))}
        except Exception as e:
             print(e)
    
    @jwt_required
    @PreAuthorize("dict:list")    
    def get(self):
        try:
            if not request.args.get('dictName'):
                return jsonify({'status':400,'message':'Missing dictName in request'})
            dictobj=Dict.query.filter_by(name=request.args.get('dictName')).first()
            page=int(request.args.get('page'))
            size=int(request.args.get('size'))
            content=DictDetail.query.filter_by(dict_id=dictobj.id).order_by(DictDetail.dict_sort).offset(page*size).limit(size).all()
            return {'status':200,'content':[item.model_to_dict() for item in content],'totalElements':len(dictobj.details)}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("dict:edit")
    @UserRecord(request,'修改字典值')     
    def put(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'提交的不是json数据,请重新提交数据!'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            DictDetail.query.filter_by(id=json.loads(request.get_data()).get('id')).update({
                'label':json.loads(request.get_data()).get('label'),
                'value':json.loads(request.get_data()).get('value'),
                'dict_sort':json.loads(request.get_data()).get('dict_sort')
            })
            db.session.commit()
            return {'status':200,'message':'{}修改成功!'.format(json.loads(request.get_data()).get('label'))}
        except Exception as e:
             print(e)
    

    @jwt_required
    @PreAuthorize("dict:del")
    @UserRecord(request,'删除字典值')     
    def delete(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'提交的不是json数据,请重新提交数据!'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            DictDetail.query.get(int(json.loads(request.get_data())[0])).delete()
            return {'status':200,'message':'数据删除成功'}         
        except Exception as e:
             print(e)


#角色管理视图函数
class RoleContraller(Resource):

    @jwt_required
    @PreAuthorize("role:list")
    def get(self):
        try:
            if not request.args.get('blurry') :
                rolesobj=Role.query.order_by(Role.id).offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()
            else:
                rolesobj=Role.query.filter(
                    or_(
                       Role.name.like('%{}%'.format(request.args.get('blurry'))),
                    )
                ).order_by(Role.id).offset(
                    int(request.args.get('page',0))*int(request.args.get('size',10))
                ).limit(int(request.args.get('size',10))).all()
            return {'status':200,'content':[item.model_to_dict() for item in rolesobj ],'totalElements':len(rolesobj)},200            
        except Exception as e:
             print(e)
    
    @jwt_required
    @PreAuthorize("role:add")
    @UserRecord(request,'添加角色')   
    def post(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            Role(
                name=json.loads(request.get_data()).get('name'),
                level=json.loads(request.get_data()).get('level'),
                description=json.loads(request.get_data()).get('description'),
                data_scope=json.loads(request.get_data()).get('data_scope'),
            ).save()
            return {'status':200,'message':'数据新增成功'}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("role:edit")
    @UserRecord(request,'修改角色')     
    def put(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            Role.query.filter(Role.id==int(json.loads(request.get_data()).get('id'))).update({
                'name':json.loads(request.get_data()).get('name'),
                "level":json.loads(request.get_data()).get('level'),
                "description":json.loads(request.get_data()).get('description'),
                "data_scope":json.loads(request.get_data()).get('data_scope'),                
            })
            db.session.commit()
            return {'status':200,'message':'数据修改成功'},200
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("role:del")
    @UserRecord(request,'删除角色')    
    def delete(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            
            for id in json.loads(request.get_data()):
                Role.query.get(int(id)).delete()
            return {'status':200,'message':'数据删除成功'},200
        except Exception as e:
             print(e)

#获取单个角色的函数
@systembp.route('/api/roles/<int:id>')
def single_role(id):
    try:
        roleobj=Role.query.get(id)
        return jsonify(roleobj.model_to_dict())
    except Exception as e:
         print(e)


#部门管理视图函数
class DeptmentContraller(Resource):
    
    @jwt_required
    @PreAuthorize("dept:list")    
    def get(self):
        try:
            if request.args.get('pid'):
                deptobj=Deptment.query.filter(Deptment.pid==request.args.get('pid')).order_by(Deptment.dept_sort).all()
            elif request.args.get('enabled'):
                deptobj=Deptment.query.filter(
                    and_(
                        Deptment.enabled==bool(request.args.get('enabled')),
                        Deptment.pid == request.args.get('pid',0)
                    )        
                ).order_by(Deptment.dept_sort).all()
            elif request.args.get('name') or request.args.get('enabled'):
                deptobj=Deptment.query.filter(
                    or_(
                        Deptment.enabled==bool(request.args.get('enabled')),
                        Deptment.name.like('%{}%'.format(request.args.get('name'))),
                    )      
                ).order_by(Deptment.dept_sort).all()                
            else:
                deptobj=Deptment.query.filter(Deptment.pid==0).all()
            return {'status':200,'content':[ item.model_to_dict() for item in deptobj]}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("dept:add")
    @UserRecord(request,'添加部门')
    def post(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            data=json.loads(request.get_data())
            Deptment(
                name=data.get('name'),
                pid= 0 if data.get('pid') == None else data.get('pid'),
                dept_sort=data.get('deptSort'),
                sub_count = data.get('subCount'),
                enabled= data.get('enabled') == 'true',
            ).save()
            # db.session.add(deptobj)
            # db.session.flush()
            # dept_id=deptobj.id
            if data.get('pid') is not None:
                detpobj=Deptment.query.get(int(data.get('pid')))
                detpobj.sub_count +=1
                db.session.commit()
            return {'status':200,'message':'数据添加成功!'}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("dept:edit")
    @UserRecord(request,'修改部门')      
    def put(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            data=json.loads(request.get_data())
            
            
            # 判断该部门之前属于哪个上级部门
            deptobj=Deptment.query.get(data.get('id'))
            if deptobj.pid != 0:
                top_deptobj=Deptment.query.get(deptobj.pid)
                top_deptobj.sub_count = int(top_deptobj.sub_count)-1
                db.session.commit()


            Deptment.query.filter_by(id=int(data.get('id'))).update({
                'name': data.get('name'),
                'pid': 0 if data.get('pid') == None else data.get('pid'),
                'dept_sort':data.get('deptSort'),
                'sub_count': data.get('subCount'),
                'enabled': data.get('enabled') == 'true',               
            })
            db.session.commit()
            if data.get('pid') is not None:
                deptobj=Deptment.query.get(int(data.get('pid')))
                deptobj.sub_count +=1
                db.session.commit()

            return {'status':200,'message':'数据修改成功!'}
        except Exception as e:
            print(e)

    @jwt_required
    @PreAuthorize("dept:del")
    @UserRecord(request,'删除部门') 
    def delete(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'}
            
            del_ids = json.loads(request.get_data())
            
            for id in del_ids:
                deldata=Deptment.query.get(id)
                if deldata.pid !=0:
                   deptobj=Deptment.query.get(deldata.pid)
                   deptobj.sub_count -=1
                   db.session.commit()
                deldata.delete() #删除父级部门

                #查询是否还有下级部门，一并删除
                child_data=Deptment.query.filter_by(pid=id)
                if child_data.count() != 0:
                   for item in child_data.all():
                       Deptment.query.get(item.id).delete()
            return {'status':200,'message':'数据删除成功!'}
        except Exception as e:
             print(e)


#用户管理视图函数
class UserContraller(Resource):

    @jwt_required
    @PreAuthorize("user:list")  
    def get(self):
        try:
            dept_id=int(request.args.get('deptId',0))
            page=int(request.args.get('page',0))
            size=int(request.args.get('size',10))
            blurry=request.args.get('blurry')
            if dept_id is not None and dept_id !=0:
                #检查dept_id是不是父级id
                deptid=[]
                if Deptment.query.get(int(dept_id)).pid == 0:
                    deptobj=Deptment.query.filter_by(pid=dept_id).offset(page*size).limit(size).all()
                    for item in deptobj:
                        deptid.append(item.id)
                    userobj=User.query.filter(User.dept_id.in_(deptid)).offset(page*size).limit(size).all()
                else:
                    userobj=User.query.filter(User.dept_id==int(dept_id)).offset(page*size).limit(size).all()   
            elif blurry is not None:
                userobj = User.query.filter(
                    or_(
                        User.email == blurry,
                        User.username.like('%{}%'.format(blurry)),
                    )
                ).offset(page*size).limit(size).all()
            elif request.args.get('enabled',0):
                userobj = User.query.filter(
                    and_(
                        User.enabled == request.args.get('enabled',1),
                        # User.username.like('%{}%'.format(blurry)),
                    )
                ).offset(page*size).limit(size).all()                
            else:
                userobj = User.query.offset(page*size).limit(size).all()    
            return {'status':200,'content':[item.model_to_dict() for item in userobj]}
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("user:add")
    @UserRecord(request,'添加用户') 
    def post(self):
        try:
            if not request.is_json:
                    return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400

            userobj=User(
                username=json.loads(request.get_data()).get('username'),
                nick_name=json.loads(request.get_data()).get('nickName'),
                email=json.loads(request.get_data()).get('email'),
                enabled=bool(1) if json.loads(request.get_data()).get('enabled') == 'true' else  bool(0),
                phone=json.loads(request.get_data()).get('phone'),
                gender = bool(1) if json.loads(request.get_data()).get('gender') == '男' else  bool(0),
                avatar_name = json.loads(request.get_data()).get('avatarName'),
                avatar_path = json.loads(request.get_data()).get('avatarPath'),
                password = bcrypt.generate_password_hash('123456'),
                dept_id =  json.loads(request.get_data()).get('dept').get('id'),
            )
            db.session.add(userobj)
            db.session.flush()
            user_id=userobj.id
            db.session.commit()

            roles_list=[]
            for role_id in json.loads(request.get_data()).get('roles'):
                roles_list.append(UsersToRoles(user_id=user_id,role_id=role_id.get('id')))
            db.session.add_all(roles_list)
            db.session.commit()

            jobs_list = []
            for job_id in json.loads(request.get_data()).get('jobs'):
                jobs_list.append(UsersToJobs(user_id=user_id,job_id=job_id.get('id')))
            db.session.add_all(jobs_list)
            db.session.commit()


        except Exception as e:
             print(e)
    
    
    @jwt_required
    @PreAuthorize("user:edit")
    @UserRecord(request,'修改用户')  
    def put(self):
        try:
            if not request.is_json:
                    return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400
            
            print(json.loads(request.get_data()))
            User.query.filter_by(id=int(json.loads(request.get_data()).get('id'))).update({
                'username':json.loads(request.get_data()).get('username'),
                'nick_name':json.loads(request.get_data()).get('nickName'),
                'email':json.loads(request.get_data()).get('email'),
                'enabled':bool(1) if json.loads(request.get_data()).get('enabled') == 'true' else  bool(0),
                'phone':json.loads(request.get_data()).get('phone'),
                'gender':bool(1) if json.loads(request.get_data()).get('gender') == '男' else  bool(0),
                'avatar_name':json.loads(request.get_data()).get('avatarName'),
                'avatar_path':json.loads(request.get_data()).get('avatarPath'),
                'dept_id':json.loads(request.get_data()).get('dept').get('id'),                
            })
            db.session.commit()
            #先删除关联的role,在重新添加
            UsersToRoles.query.filter_by(user_id=int(json.loads(request.get_data()).get('id'))).delete()
            roles_list=[]
            for role_id in json.loads(request.get_data()).get('roles'):
                roles_list.append(UsersToRoles(user_id=int(json.loads(request.get_data()).get('id')),role_id=role_id.get('id')))
            db.session.add_all(roles_list)
            db.session.commit()

            UsersToJobs.query.filter_by(user_id=int(json.loads(request.get_data()).get('id'))).delete()
            jobs_list = []
            for job_id in json.loads(request.get_data()).get('jobs'):
                jobs_list.append(UsersToJobs(user_id=int(json.loads(request.get_data()).get('id')),job_id=job_id.get('id')))
            db.session.add_all(jobs_list)
            db.session.commit()
            return {'status':200,'message':'数据更新成功'},200            
        except Exception as e:
             print(e)

    @jwt_required
    @PreAuthorize("user:del")
    @UserRecord(request,'删除用户')  
    def delete(self):
        try:
            if not request.is_json:
                return jsonify({'status':400,'message':'Missing JSON in request'})
            if not request.get_data() :
                return {'status':400,'message':'没有获取数据'},400

            #删除用户相关联的信息
            print(json.loads(request.get_data()))
            for id in json.loads(request.get_data()):
                #删除用户与角色关联表的记录
                UsersToRoles.query.filter_by(user_id=id).delete()
                #删除用户与岗位关联表的记录
                UsersToJobs.query.filter_by(user_id=id).delete()
                User.query.get(int(id)).delete()
            return {'status':200,'message':'数据删除成功!'},200
                   
        except Exception as e:
             print(e)

#获取全部角色数据
@systembp.route('/api/roles/all',methods=['get'])
def RolesAll():
    try:
        return jsonify([ item.model_to_dict() for item in Role.query.all()])
    except Exception as e:
        print(e)


#获取子菜单函数
@systembp.route('/api/menus/child')
def get_menu_child():
    menu_list=[]
    try:
        menuobj=Menu.query.get(int(request.args.get('id')))
        if menuobj.sub_count !=0:
            menu_list.append(int(request.args.get('id')))
            if menuobj.pid !=0:
                menuobj=Menu.query.filter_by(pid=int(request.args.get('id'))).all()
                for item in menuobj:
                    menu_list.append(int(item.id))
            else:
                menuobj=Menu.query.filter_by(pid=int(request.args.get('id'))).all()
                for item in menuobj:
                    menu_list.append(item.id)
                    if item.sub_count !=0:
                        childmenuobj=Menu.query.filter_by(pid=int(item.id)).all()
                        for i in childmenuobj:
                            menu_list.append(i.id)
        
        else:
            menu_list.append(int(request.args.get('id')))
        

        return jsonify(list(set(menu_list)))
    except Exception as e:
         print(e)


#添加角色与菜单的关系
@systembp.route('/api/roles/menu',methods=['put'])
def roles_menu():
    try:
        data=json.loads(request.get_data())
        #先清空原有数据
        RoleToMenu.query.filter_by(role_id=int(data.get('id'))).delete()
        menu_list=[]
        for item in data.get('menus'):
            menu_id=int(item.get('id'))
            menu_list.append(RoleToMenu(menu_id=menu_id,role_id=data.get('id')))
        db.session.add_all(menu_list)
        db.session.commit()
        return jsonify({'status':200,'message':'数据修改成功'})
    except Exception as e:
        print(e)


#获取用户级别
@systembp.route('/api/roles/level',methods=['get'])
def getroleslevel():
    try:
        return jsonify({'level':3})
    except Exception as e:
         print(e)

@systembp.route('/api/dept/superior',methods=['post'])
def detpsuperior():
    try:
        deptobj=Deptment.query.all()
        data=[ item.model_to_dict() for item in Deptment.query.all()]
        return {'status':200,'content':dept_tree(data,0,'pid','id'),'totalElements':len(data)}
    except Exception as e:
         print(e)

@systembp.route('/auth/logout',methods=['delete'])
def logout():
    try:
        return {'status':200,'content':'退出成功'}
    except Exception as e:
         print(e)


#验证码生成
@systembp.route('/auth/code',methods=['get'])
def generate_captcha():
    generate_code=ArithmeticCaptchaAbstract(width=111,height=36,fonts='apps/utils/fonts/actionj.ttf',font_sizes=32)
    calc_num1=random.randint(0,9)
    calc=random.choice(['+','-','x'])
    calc_num2=random.randint(0,9)
    if calc == '+':
        result=int(calc_num1+calc_num2)
    elif calc == '-':
        result=int(calc_num1-calc_num2)
    else:
        result=int(calc_num1*calc_num2)
    char_str='{}{}{}=?'.format(calc_num1,calc,calc_num2)
    img=generate_code.create_captcha_image(char_str,random_color(),background=(255,255,255))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
    _uuid='code-key-'+uuid4().hex
    session[_uuid]=result
    img=str(img,encoding='utf-8')
    return jsonify({'uuid':_uuid,'img':img})




#该方法主要用来测试用
@systembp.route('/protected',methods=['get'])
# @jwt_required
# @UserRecord(request,'测试')
def protected():

    # session['test']='test'
    # print(session.get('test'))
    #print(session.get('didiplus'))
    base_path = os.path.dirname(os.path.abspath(__file__))
    #base_dir = dirname(dirname(abspath(__file__)))
    print(os.path.abspath(__file__))
    return jsonify({'code':200,'msg':'这是一个测试'}), 200


