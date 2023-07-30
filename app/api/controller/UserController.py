"""
用户管理
"""
from flask import Blueprint,request,jsonify
from app.api.service.UserService import UserService

# 定义一个蓝图
user = Blueprint('user', __name__)
# 初始化用户服务类
userService = UserService()

# 分页查询用户
@user.route('/',methods=['GET'])
def get_users():
    limit = request.args.get("pageSize",type=int)
    page = request.args.get("currentPage",type=int)
    return jsonify(userService.get_users(limit,page))

# 查询单个用户
@user.route('/<int:id>',methods=['GET'])
def get_user(id):
    return jsonify(userService.get_user(id))

# 新增用户
@user.route('/',methods=['POST'])
def add_user():
    user_name = request.form['user_name']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    result = userService.add_user(user_name, phone, password, email)
    print(result)
    return jsonify(result)

# 修改用户
@user.route('/<int:id>',methods=['PUT'])
def update_user(id):
    user_name = request.form['user_name']
    phone = request.form['phone']
    email = request.form['email']
    result = userService.update_user(id,user_name,phone,email)
    return jsonify(result)

@user.route('/password/<int:id>',methods=['PUT'])
def update_password(id):
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    result = userService.update_password(id,old_password,new_password)
    return jsonify(result)

# 删除用户
@user.route('/<int:id>',methods=['DELETE'])
def delete_user(id):
    return jsonify(userService.delete_user(id))