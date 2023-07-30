"""
用户服务类
"""
import datetime
from app.api.model.errors import ResponseCode,ResponseResult
from app import db
from app.api.model.Models import User

class UserService:
    # 分页查询所有用户
    def get_users(self,limit,page):
        data = User.query.all()
        print(limit)
        print(page)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
           result.append(data[i].to_json()) 
        return ResponseResult.lay_success(data=result,count=len(data))

    # 根据ID查询单个用户
    def get_user(self,id):
        try:
            print(id)
            user = User.query.filter_by(id=id).first()
            print(user.user_name)
            return ResponseResult.success(data=user.to_json())
        except:
            return ResponseResult.error()

    def get_user_by_phone(self,phone):
        user = User.query.filter_by(phone=phone).first()
        return user

    # 创建用户
    def add_user(self,user_name, phone, password, email):
        if(self.check_add_param(user_name,phone,email,password)):
            return ResponseResult.error(ResponseCode.PARAM_IS_NULL)
        # 创建时间
        created_time = datetime.datetime.now()
        user = User(user_name, phone, password, email,created_time)
        try:
            db.session.add(user)
            db.session.commit()
            return ResponseResult.success()
        except:
            return ResponseResult.error()

    def check_add_param(self,user_name,phone,email,password):
        if(user_name is None):
            return True
        elif(phone is None):
            return True
        elif(email is None):
            return True
        elif(password is None):
            return True
        else:
            return False
        
    # 修改用户基本信息
    def update_user(self,id,user_name,phone,email):
        try:
            User.query.filter_by(id=id).update({"user_name":user_name,"phone":phone,"email":email})
            db.session.commit()
            user = User.query.filter_by(id=id).first()
            return ResponseResult.success(data=user.to_json())
        except:
            return ResponseResult.error()

    # 修改密码
    def update_password(self,id,old_password,new_password):
        try:
            user = User.query.filter_by(id=id).first()
            if(user.password != old_password):
                return ResponseResult.error(ResponseCode.PASSWORD_ERROR)
            user.password = new_password
            db.session.commit()
            return ResponseResult.success()
        except:
            return ResponseResult.error()


            

    # 删除用户
    def delete_user(self,id):
        try:
            User.query.filter_by(id=id).delete()
            db.session.commit()
            return ResponseResult.success()
        except:
            return ResponseResult.error()

    


