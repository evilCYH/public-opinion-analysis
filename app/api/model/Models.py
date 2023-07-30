from sqlalchemy import Column, Integer, String,DateTime
from app import db

# 基础的实体
class BaseModel:
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


    

# 用户实体
class User(db.Model,BaseModel):

    __tablename__ = 'user'

    # 用户ID
    id = Column(Integer, primary_key=True, autoincrement=True,comment='主键')
    # 用户名
    user_name = Column(String(64), nullable=False,comment='用户名')
    # 手机号
    phone = Column(String(11), nullable=False,comment='手机号')
    # 密码
    password = Column(String(64), nullable=False,comment='密码')
    # 邮箱地址
    email = Column(String(64), nullable=False,comment='邮箱地址')
    # 创建时间
    created_time = Column(DateTime, nullable=False,comment='创建时间')

    def __init__(self, user_name, phone, password, email,created_time):
        
        self.user_name = user_name
        self.phone = phone
        self.password = password
        self.email = email
        self.created_time = created_time


# 微博实体
class Weibo(db.Model,BaseModel):

    __tablename__ = 'weibo'

    # id
    id = Column(String(64), primary_key=True,comment='主键')
    # 微博ID
    bid = Column(String(64), nullable=False,comment='微博ID')
    # 用户ID
    user_id = Column(String(11), nullable=False,comment='用户ID')
    # 用户昵称
    screen_name = Column(String(64), nullable=False,comment='用户昵称')
    # 邮箱地址
    text = Column(String(1024), nullable=False,comment='微博内容')
    # 话题
    topics = Column(String(1024), nullable=False,comment='话题')
    # @的用户
    at_users = Column(String(1024), nullable=False,comment='@的用户')
    # 图片列表
    pics = Column(String(1024), nullable=False,comment='图片列表')
     # 视频列表
    video_url = Column(String(1024), nullable=False,comment='视频列表')
     # 发布地点
    location = Column(String(128), nullable=False,comment='发布地点')
     # 发布时间
    created_at = Column(DateTime, nullable=False,comment='发布时间')
    # 微博来源
    source = Column(String(128), nullable=False,comment='微博来源')
    # 点赞数
    attitudes_count = Column(Integer, nullable=False,comment='点赞数')
    # 评论数
    comments_count = Column(Integer, nullable=False,comment='评论数')
    # 评论数
    reposts_count = Column(Integer, nullable=False,comment='转发数')
    # 转发ID
    retweet_id = Column(String(32), nullable=False,comment='转发数')

    def __init__(self, bid, user_id, screen_name, text,topics,at_users,pics
    ,video_url,location,created_at,source,attitudes_count,comments_count,reposts_count,retweet_id):
        
        self.bid = bid
        self.user_id = user_id
        self.screen_name = screen_name
        self.text = text
        self.topics = topics
        self.at_users = at_users
        self.pics = pics
        self.video_url = video_url
        self.location = location
        self.created_at = created_at
        self.source = source
        self.attitudes_count = attitudes_count
        self.comments_count = comments_count
        self.reposts_count = reposts_count
        self.retweet_id = retweet_id


# 微博评论实体
class Comments(db.Model,BaseModel):

    __tablename__ = 'comments'

    # ID
    id = Column(String(64), primary_key=True,comment='主键')
    # 评论ID
    mid = Column(String(64), nullable=False,comment='评论ID')
    # 用户昵称
    screen_name = Column(String(64),comment='用户昵称')
    # 喜欢的数量
    like_count = Column(Integer,comment='喜欢的数量')
    # 楼层数
    floor_number = Column(Integer,comment='楼层数')
    # 回复数
    follow_count = Column(Integer,comment='回复数')
    # 来源
    source = Column(String(128),comment='来源')
    # 来源
    comment = Column(String(1024),comment='评论内容')
    # 性别
    gender = Column(String(32),comment='性别')
    # 根评论ID
    rootid = Column(String(64),comment='根评论ID')


    def __init__(self, mid,screen_name,like_count, floor_number, follow_count,source,comment,gender,rootid):
        
        self.mid = mid
        self.screen_name = screen_name
        self.like_count = like_count
        self.floor_number = floor_number
        self.follow_count = follow_count
        self.source = source
        self.comment = comment
        self.gender = gender
        self.rootid = rootid



    


