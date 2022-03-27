from apps import db
from datetime import datetime
import time
class BaseModel(db.Model):
   __abstract__ = True


   __table_arhs__ = {
       'mysql_engine': 'InnoDb',                   # 设置表引擎
       'mysql_charset': 'utf8'                     # 设置表字符集 
   }

   def save(self):
       try:
            db.session.add(self)
            db.session.commit()
       except Exception as e:
            db.session.rollback()
            print(e)
   def delete(self):
       try:
            db.session.delete(self)
            db.session.commit()
       except Exception as e:
            db.session.rollback()
            print(e)
    
   #把model字段转化字典类型
   def  model_to_dict(self):
      json_dict = {}
      for column in self.__table__.columns:
          attribute = getattr(self,column.name)
          if isinstance(attribute,datetime):
             attribute=datetime.strftime(attribute, '%Y-%m-%d %H:%M:%S') #正常时间格式
             #attribute=datetime.timestamp(attribute)       
          json_dict[column.name]=attribute
      return json_dict
       


        


