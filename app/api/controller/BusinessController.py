"""
业务功能模块
"""
from flask import Blueprint,request,jsonify,Response,send_file
from app.api.service.BusinessService import BusinessService
import io

# 定义一个蓝图
business = Blueprint('business', __name__)

businessService = BusinessService()

# 获取累计的微博数等信息
@business.route('/getCount/',methods=['get'])
def getCount():
    return jsonify(businessService.getCount())

# 获取微博数等信息随着时间的变化
@business.route('/getWeiboStaticByTime/',methods=['get'])
def getWeiboStaticByTime():
    return jsonify(businessService.getWeiboStaticByTime())

# 获取微博话题排行榜TOP10
@business.route('/getTop10Topic/',methods=['get'])
def getTop10Topic():
    return jsonify(businessService.getTop10Topic())

# 获取微博话题排行榜TOP10
@business.route('/getTop10HotTopic/',methods=['get'])
def getTop10HotTopic():
    return jsonify(businessService.getTop10HotTopic())

# 查询微博列表
@business.route('/getHotWeiboList/')
def getHotWeiboList():
    orderBy = request.args.get('order_by',type=int,default=1)
    weibo_keywords = request.args.get('weibo_keywords')
    topic_keywords = request.args.get('topic_keywords')
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    return jsonify(businessService.getHotWeiboList(orderBy,weibo_keywords,topic_keywords,limit,page))

# 查询微博评论列表
@business.route('/getCommentList/')
def getCommentList():
    keywords = request.args.get('keywords')
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    return jsonify(businessService.getCommentList(keywords,limit,page))


@business.route('/getTopicStaticByTime/')
def getTopicStaticByTime():
    keywords = request.args.get('keywords')
    return jsonify(businessService.getTopicStaticByTime(keywords))


@business.route('/getWeiboGender/')
def getWeiboGender():
    return jsonify(businessService.getWeiboGender())

@business.route('/getLastNews/')
def getLastNews():
    return jsonify(businessService.getLastNews())


@business.route('/getHotNews/')
def getHotNews():
    keywords = request.args.get('keywords')
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    return jsonify(businessService.getHotNews(keywords,limit,page))

@business.route('/getAllCount/')
def getAllCount():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getAllCount(start_time,end_time))

@business.route('/getLastYuqing/')
def getLastYuqing():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    return jsonify(businessService.getLastYuqing(start_time,end_time,limit,page))


@business.route('/getYuqingMap/')
def getYuqingMap():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getYuqingMap(start_time,end_time))

@business.route('/getYuqingByTime/')
def getYuqingByTime():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getYuqingByTime(start_time,end_time))


@business.route('/getSensitiveWord/')
def getSensitiveWord():
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    userId = request.args.get("userId")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getSensitiveWord(userId,limit,page,start_time,end_time))

@business.route('/addSensitiveWord/',methods=['post'])
def addSensitiveWord():
    userId = request.form.get("userId")
    word = request.form.get("word")
    return jsonify(businessService.addSensitiveWord(userId,word))

@business.route('/deleteSensitiveWord/')
def deleteSensitiveWord():
    id = request.args.get("id")
    return jsonify(businessService.deleteSensitiveWord(id))



@business.route('/getSensitiveWordList/',methods=['get'])
def getSensitiveWordList():
    userId = request.args.get("userId")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getSensitiveWordList(userId,start_time,end_time))

@business.route('/getSensitiveWordByTime/',methods=['get'])
def getSensitiveWordByTime():
    userId = request.args.get("userId")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getSensitiveWordByTime(userId,start_time,end_time))


@business.route('/getHotTopic/')
def getHotTopic():
    keywords = request.args.get("keywords")
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    return jsonify(businessService.getHotTopic(keywords,limit,page))


@business.route('/getLastTopic/')
def getLastTopic():
    return jsonify(businessService.getLastTopic())


@business.route('/getTopicCountByTime/',methods=['get'])
def getTopicCountByTime():
    topics = request.args.get("topics")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getTopicCountByTime(topics,start_time,end_time))

@business.route('/getNlpByTime/',methods=['get'])
def getNlpByTime():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getNlpByTime(start_time,end_time))

@business.route('/getNlpMap/',methods=['get'])
def getNlpMap():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(businessService.getNlpMap(start_time,end_time))

@business.route('/getNlpData/',methods=['get'])
def getNlpData():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    limit = request.args.get("limit",type=int)
    page = request.args.get("page",type=int)
    return jsonify(businessService.getNlpData(start_time,end_time,limit,page))

    
    



