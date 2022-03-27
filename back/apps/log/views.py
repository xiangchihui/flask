
from flask_restplus import Resource
from flask import request,Blueprint,jsonify
from apps.system.models import SystemLog,db
from flask_jwt_extended import get_jwt_identity,jwt_required

logsbp=Blueprint('logs',__name__)

class UserLogContraller(Resource):
    
    @jwt_required
    def get(self):
        try:
            username = get_jwt_identity()
            page=request.args.get('page',0)
            size=request.args.get('size',10)
            logobj=SystemLog.query.filter_by(username=username).offset(int(page)*int(size)).limit(int(size)).all()
            return {'status':200,'content':[ item.model_to_dict() for item in logobj],'totalElements':len(logobj)}
        except Exception as e:
             print(e)

@logsbp.route('/api/logs/del/info',methods=['delete'])
@jwt_required
def del_logs():
    try:
        username = get_jwt_identity()
        #清空当前用户的操作记录
        SystemLog.query.filter_by(username=username).delete()
        db.session.commit()
        return jsonify({'status':200,'message':'数据删除成功'})
    except Exception as e:
         print(e)