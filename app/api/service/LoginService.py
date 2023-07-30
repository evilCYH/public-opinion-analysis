"""
登录服务类
"""
import datetime
from app.api.model.errors import ResponseCode,ResponseResult
from app import db
from app.api.model.Models import User
from app.api.service.UserService import UserService
userService = UserService()

class LoginService:

    # 用户登录
    def login(self,phone,password):
        try:
            print(phone)
            print(password)
            user = User.query.filter_by(phone=phone,password=password).first()
            print(user)
            if(user):
                return ResponseResult.success(data=user.to_json())
            else:
                return ResponseResult.error(ResponseCode.LOGIN_ERROR)
        except:
            return ResponseResult.error()

    # 用户注册
    def register(self,user_name, phone, password, email):
        user = userService.get_user_by_phone(phone)
        if(user):
            return ResponseResult.error(ResponseCode.PHONE_EXIST_ERROR)
        return userService.add_user(user_name, phone, password, email)

    

    


