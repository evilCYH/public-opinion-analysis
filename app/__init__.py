from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # 实例化

def create_app():
    app = Flask(__name__,static_folder='static')
    app.config.from_object('app.secure')
    register_blueprint(app)   # 完成蓝图注册
    init_db(app)
    return app

def register_blueprint(app):  # 注册蓝图
    from app.api.controller.UserController import user
    from app.api.controller.LoginController import login
    from app.api.controller.BusinessController import business

    app.register_blueprint(user, url_prefix='/api/user')  
    app.register_blueprint(login, url_prefix='/api/login')
    app.register_blueprint(business, url_prefix='/api/business')


def init_db(app):
    # 注册db
    db.init_app(app)
    # 将代码映射到数据库中
    with app.app_context():
        from app.api.model.Models import User,Weibo,Comments
        db.create_all(app=app)

