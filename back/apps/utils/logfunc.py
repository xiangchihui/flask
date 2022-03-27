from flask_jwt_extended import get_jwt_identity
from apps.system.models import SystemLog,db
from apps.utils.common import getIpInfo
import json,re,time

##记录用户操作行为
def UserRecord(request_header,msg):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            #记录用户操作行为，入库
            try:
                username = get_jwt_identity()
                browser = request_header.user_agent.browser+'/'+request_header.user_agent.version #获取浏览器类型和版本
                description = msg
                log_type='info'
                method = request_header.method #获取请求的方法
                request_ip = request_header.remote_addr
                if 'multipart/form-data' == request_header.headers.getlist('Content-Type')[0].split(';')[0]:
                    params = None
                else:
                    params = request_header.args if method == 'GET' else request_header.get_data().decode('utf-8')
                address = getIpInfo(request_ip)
                p1 = re.compile(r'[(](.*?)[)]', re.S)
                system = re.findall(re.compile(r'[(](.*?)[)]', re.S),request_header.user_agent.string)[0].split(';')[0]
                start = time.time()
                t= func(*args, **kwargs)
                request_time = time.time()-start
                systemlogobj=SystemLog(
                    description=description,
                    log_type=log_type,
                    method=method,
                    params=params,
                    request_ip=request_ip,
                    time=round(request_time*1000,3),
                    username=username,
                    address=address,
                    browser=browser,
                    system=system,
                    exception_detail='-'
                ).save()
                return t
            except Exception as e:
                print(e)
   
        return inner_wrapper
    return wrapper