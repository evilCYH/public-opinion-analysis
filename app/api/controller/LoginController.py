"""
登录管理
"""
from flask import Blueprint,request,jsonify,render_template
from app.api.service.LoginService import LoginService

# 定义一个蓝图
login = Blueprint('login', __name__)
# 初始化用户服务类
loginService = LoginService()


# 登录
@login.route('/',methods=['POST'])
def login_in():
    phone = request.form['phone']
    password = request.form['password']
    return jsonify(loginService.login(phone,password))

# 注册
@login.route('/register/',methods=['POST'])
def register():
    user_name = request.form['user_name']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    return jsonify(loginService.register(user_name, phone, password, email))



