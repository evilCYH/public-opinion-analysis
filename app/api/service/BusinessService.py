"""
业务功能服务类
"""
import json

from app.api.model.Models import Weibo,Comments,User
from app import db
from app.api.model.errors import ResponseCode,ResponseResult
from sqlalchemy import func
import time
import datetime
from app.api.utils.time_util import get_last_week

class BusinessService:
    
    # 获取微博信息的统计数
    def getCount(self):
        sql = 'SELECT count(w.id) as weibo_number,sum(w.attitudes_count) as attitudes_count,\
        sum(w.comments_count) as comments_count,sum(w.reposts_count) as reposts_count\
        from weibo w'
        ret = db.session.execute(sql).fetchone()
        ret = ResponseResult.success(data=dict(ret))
        for i,j in ret['data'].items():
            ret['data'][i] = int(j)
        return ret

    # 按时间统计微博信息变化
    def getWeiboStaticByTime(self):
        sql = "select DATE_FORMAT(w.created_at,'%Y-%m') as created_at,sum(1) as weibo_number,sum(w.attitudes_count) as attitudes_count\
        ,sum(w.comments_count) as comments_count,sum(w.reposts_count) as reposts_count from weibo w \
        GROUP BY DATE_FORMAT(w.created_at,'%Y-%m') order by created_at"
        ret = db.session.execute(sql).fetchall()
        data = list(ret)
        xAxis = []
        weibo_number_list = []
        attitudes_count_list = []
        comments_count_list = []
        reposts_count_list = []
        for i in range(len(data)):
            item = data[i]
            xAxis.append(item.created_at)
            weibo_number_list.append(int(item.weibo_number))
            attitudes_count_list.append(int(item.attitudes_count))
            comments_count_list.append(int(item.comments_count))
            reposts_count_list.append(int(item.reposts_count))
        result = {'xAxis':xAxis,'weibo_number_list':weibo_number_list,'attitudes_count_list':attitudes_count_list
        ,'comments_count_list':comments_count_list,'reposts_count_list':reposts_count_list}
        return ResponseResult.success(data=result)

    # 获取微博话题排行榜TOP10
    def getTop10Topic(self):
        sql = "SELECT t.topics,count(1) AS count FROM(SELECT a.id,substring_index(substring_index(a.topics,\
		'；',b.help_topic_id + 1),'；',- 1) topics FROM weibo a JOIN mysql.help_topic b ON ( b.help_topic_id <(\
	    length(a.topics) - length(REPLACE (a.topics, '；', '')) + 1) AND a.topics IS NOT NULL AND a.topics != '')\
        WHERE a.topics IS NOT NULL ORDER BY a.id) t GROUP BY t.topics ORDER BY count desc limit 10"
        ret = db.session.execute(sql).fetchall()
        data = list(ret)
        yAxis = []
        series = []
        for i in range(len(data)):
            item = data[i]
            yAxis.append(item.topics)
            series.append(item.count)
        
        result = {'yAxis':list(reversed(yAxis)),'series':list(reversed(series))}
        return ResponseResult.success(data=result)

    # 获取微博话题活跃度排行榜TOP10
    def getTop10HotTopic(self):
        sql = "SELECT t.topics,sum(t.attitudes_count) as attitudes_count,sum(t.comments_count) as comments_count,sum(t.reposts_count) as reposts_count  FROM(SELECT a.attitudes_count,a.comments_count,a.reposts_count,substring_index(substring_index(a.topics,'；',b.help_topic_id + 1),'；',- 1) topics FROM weibo a JOIN mysql.help_topic b ON ( b.help_topic_id <(length(a.topics) - length(REPLACE (a.topics, '；', '')) + 1) AND a.topics IS NOT NULL AND a.topics != '')WHERE a.topics IS NOT NULL ORDER BY a.id) t GROUP BY t.topics ORDER BY attitudes_count desc,comments_count desc,reposts_count desc limit 10"
        ret = db.session.execute(sql).fetchall()
        data = list(ret)
        yAxis = []
        attitudes_count_list = []
        comments_count_list = []
        reposts_count_list = []
        for i in range(len(data)):
            item = data[i]
            yAxis.append(item.topics)
            attitudes_count_list.append(int(item.attitudes_count))
            comments_count_list.append(int(item.comments_count))
            reposts_count_list.append(int(item.reposts_count))

        result = {'yAxis':list(reversed(yAxis)),'attitudes_count_list':list(reversed(attitudes_count_list))
        ,'comments_count_list':list(reversed(comments_count_list)),'reposts_count_list':list(reversed(reposts_count_list))}

        return ResponseResult.success(data=result)

    # 查询热门微博列表
    def getHotWeiboList(self,orderBy,weibo_keywords,topic_keywords,limit,page):
        print(orderBy)
        if(orderBy == 1):
            orderBy = Weibo.comments_count.desc()
        elif(orderBy == 2):
            orderBy = Weibo.attitudes_count.desc()
        elif(orderBy == 3):
            orderBy = Weibo.reposts_count.desc()
        else:
            return ResponseResult.error()
        if(weibo_keywords != None and weibo_keywords != ''):
            if(topic_keywords != None and topic_keywords != ''):
                data = Weibo.query.filter(Weibo.text.contains(weibo_keywords),Weibo.topics.contains(topic_keywords)).order_by(orderBy).all()
            else:
                data = Weibo.query.filter(Weibo.text.contains(weibo_keywords)).order_by(orderBy).all()
        else:
            if(topic_keywords != None and topic_keywords != ''):
                data = Weibo.query.filter(Weibo.topics.contains(topic_keywords)).order_by(orderBy).all()
            else:
                data = Weibo.query.order_by(orderBy).all()
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
           result.append(data[i].to_json()) 
        return ResponseResult.lay_success(data=result,count=len(data))

    # 查询微博评论列表
    def getCommentList(self,keywords,limit,page):
        if(keywords != None and keywords != ''):
            data = Comments.query.filter(Comments.comment.contains(keywords)).all()
        else:
            data = Comments.query.all()
        print(data)
        print(limit)
        print(page)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
           result.append(data[i].to_json()) 
        return ResponseResult.lay_success(data=result,count=len(data))

    # 话题趋势分析
    def getTopicStaticByTime(self,keywords):
        # 按照;拆分
        keywords_list = keywords.split(';')
        sql = "select DATE_FORMAT(w.created_at,'%Y-%m') as created_at,sum(1) as weibo_number\
          from weibo w where w.topics like '%{}%' group by DATE_FORMAT(w.created_at,'%Y-%m') order by created_at"
        for keyword in keywords_list:
            k_sql = sql.format(keyword)
            ret = db.session.execute(sql).fetchall()
            data = list(ret)
            xAxis = []
            weibo_number_list = []
            attitudes_count_list = []
            comments_count_list = []
            reposts_count_list = []
            for i in range(len(data)):
                item = data[i]
                xAxis.append(item.created_at)
                weibo_number_list.append(item.weibo_number)
                attitudes_count_list.append(item.attitudes_count)
                comments_count_list.append(item.comments_count)
                reposts_count_list.append(item.reposts_count)

    # 查询性别分布
    def getWeiboGender(self):
        sql = "select c.gender,count(id) as count from comments c GROUP BY c.gender"
        ret = db.session.execute(sql).fetchall()
        data = list(ret)
        result = []
        for item in data:
            result.append({'name':item.gender,'value':item.count})

        return ResponseResult.success(data=result)

    # 查询所有微博
    def get_all_webbo_text(self):
        ret = Weibo.query.all()
        data = list(ret)
        result = []
        for item in data:
            result.append(item.text)
        return result
    # 查询所有微博
    def get_all_comment(self):
        ret = Comments.query.all()
        data = list(ret)
        result = []
        for item in data:
            result.append(item.comment)
        return result

    def getLastNews(self):
        query_sql = 'select title,link  from school_news order by create_time desc limit 10'
        ret = db.session.execute(query_sql).fetchall()
        data = list(ret)
        result = []
        for item in data:
            result.append({'title':item.title,'link':item.link})
        return ResponseResult.success(data=result)

    # 查询新闻动态
    def getHotNews(self,keywords,limit,page):
        sql = "select title,link,creator,create_time  from school_news  order by title desc"
        if(keywords != None and keywords != ''):
            sql = "select title,link,creator,create_time  from school_news where title like concat('%',:keywords,'%') order by title desc"
            params = {'keywords':keywords}
            ret = db.session.execute(sql,params).fetchall()
        else:
            ret = db.session.execute(sql).fetchall()
        data = list(ret)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
            item = dict(data[i])
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            result.append(item)
        return ResponseResult.lay_success(data=result,count=len(data))


        # 获取微博信息的统计数
    def getAllCount(self,start_time,end_time):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        print(params)
        sql = 'SELECT count(*) as count from weibo where created_at>=:start_time and created_at<=:end_time'
        ret = db.session.execute(sql,params).fetchone()
        weibo_count = dict(ret)['count']
        sql = 'SELECT count(*) as count from school_news where create_time>=:start_time and create_time<=:end_time'
        ret = db.session.execute(sql,params).fetchone()
        news_count = dict(ret)['count']
        sql = 'SELECT count(*) as count from tieba where create_time>=:start_time and create_time<=:end_time'
        ret = db.session.execute(sql,params).fetchone()
        tieba_count = dict(ret)['count']
        all_count = weibo_count+news_count+tieba_count
        return ResponseResult.success({'all_count':all_count,'weibo_count':weibo_count,'news_count':news_count,'tieba_count':tieba_count})
        

    def getLastYuqing(self,start_time,end_time,limit,page):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        sql = "SELECT t.* FROM (SELECT text as title,screen_name as creator,created_at as create_time,'微博' as type from weibo where created_at>=:start_time and created_at<=:end_time \
            UNION SELECT title,creator,create_time,'新闻' as type from school_news where create_time>=:start_time and create_time<=:end_time \
            UNION SELECT title,creator,create_time,'贴吧' as type from tieba where create_time>=:start_time and create_time<=:end_time) t order by t.create_time desc"
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
            item = dict(data[i])
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            result.append(item)
        return ResponseResult.lay_success(data=result,count=len(data))

    def getYuqingMap(self,start_time,end_time):
        result = self.getAllCount(start_time,end_time)
        weibo_count = result['data']['weibo_count']
        news_count = result['data']['news_count']
        tieba_count = result['data']['tieba_count']
        series = [{'name':'微博','value':weibo_count},
        {'name':'新闻','value':news_count},{'name':'贴吧','value':tieba_count}]
        return ResponseResult.success({'series':series})

    def getYuqingByTime(self,start_time,end_time):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        sql = "SELECT t.create_time,t.type,count(t.title) as count FROM (SELECT text as title,screen_name as creator,created_at as create_time,'微博' as type from weibo where created_at>=:start_time and created_at<=:end_time \
            UNION SELECT title,creator,create_time,'新闻' as type from school_news where create_time>=:start_time and create_time<=:end_time \
            UNION SELECT title,creator,create_time,'贴吧' as type from tieba where create_time>=:start_time and create_time<=:end_time) t \
            group by t.create_time,t.type order by t.create_time"
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        xAxis = []
        weibo_list = []
        news_list = []
        tieba_list = []
        type_dict = dict()
        for i in range(len(data)):
            item = dict(data[i])
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d')
            if(item['create_time'] not in xAxis):
                xAxis.append(item['create_time'])
            if(item['type'] == '微博'):
                weibo_list.append(item['count'])
                type_dict[item['create_time']+'微博'] = 1
            else:
                if(item['create_time']+'微博' not in type_dict):
                    weibo_list.append(0)
                    type_dict[item['create_time']+'微博'] = 1
            if(item['type'] == '新闻'):
                news_list.append(item['count'])
                type_dict[item['create_time']+'新闻'] = 1
            else:
                if(item['create_time']+'新闻' not in type_dict):
                    news_list.append(0)
                    type_dict[item['create_time']+'新闻'] = 1
            if(item['type'] == '贴吧'):
                tieba_list.append(item['count'])
                type_dict[item['create_time']+'贴吧'] = 1
            else:
                if(item['create_time']+'贴吧' not in type_dict):
                    tieba_list.append(0)
                    type_dict[item['create_time']+'贴吧'] = 1
        result = {'xAxis':xAxis,'weibo_list':weibo_list,'news_list':news_list
        ,'tieba_list':tieba_list}
        return ResponseResult.success(data=result)


    def getSensitiveWord(self,userId,limit,page,start_time,end_time):
        sql = 'select * from sensitive_word where creator=:creator'
        params = {'creator':userId,'start_time':start_time,'end_time':end_time}
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        user_sql = 'select * from user where id = :id'
        for i in range(start,end):
            item = dict(data[i])
            params = {'id':item['creator']}
            ret = db.session.execute(user_sql,params).fetchone()
            user = dict(ret)
            item['creator'] = user['user_name']
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            result.append(item)
        return ResponseResult.lay_success(data=result,count=len(data))

    def addSensitiveWord(self,userId,word):
        sql = 'insert sensitive_word (word,creator,create_time) values(:word,:creator,:create_time)'
        params = {'word':word,'creator':userId,'create_time':datetime.datetime.now()}
        db.session.execute(sql,params)
        return ResponseResult.success()

    def deleteSensitiveWord(self,id):
        sql = 'delete from sensitive_word where id = :id'
        params = {'id':id}
        db.session.execute(sql,params)
        return ResponseResult.success()


    def getSensitiveWordList(self,userId,start_time,end_time):
        sql = 'select * from sensitive_word where creator=:creator'
        params = {'creator':userId}
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        word_list = []
        result = dict()
        query_sql = "SELECT t.* FROM \
        (SELECT text as title,created_at as create_time,'微博' as type from weibo where text like concat('%',:word,'%') \
            UNION SELECT title,create_time,'新闻' as type from school_news where title like concat('%',:word,'%')  \
            UNION SELECT title,create_time,'贴吧' as type from tieba where title like concat('%',:word,'%')) t where \
             t.create_time>=:start_time and t.create_time <= :end_time order by t.create_time desc limit 10 "
        for i in range(len(data)):
            item = dict(data[i])
            word = item['word']
            word_list.append(word)
            params = {'word':word,'start_time':start_time,'end_time':end_time}
            info = db.session.execute(query_sql,params).fetchall()
            temp = list(info)
            dict_list = []
            for s_temp in temp:
                s_temp = dict(s_temp)
                dict_list.append(s_temp['title'])
            result[word] = dict_list
        return ResponseResult.success({'word_list':word_list,'result':result})

    def getSensitiveWordByTime(self,userId,start_time,end_time):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        
        word_sql = 'select * from sensitive_word where creator=:creator'
        word_params = {'creator':userId}
        ret = db.session.execute(word_sql,word_params).fetchall()
        word_data = list(ret)
        xAxis = []
        series = []
        legend = []
        data_dict = dict()
        if(len(word_data)==0):
            return ResponseResult.success()
        all_sql = 'SELECT ss.* from ('
        for t in range(len(word_data)):
            item = dict(word_data[t])
            word = item['word']
            params['word'] = word
            legend.append(word)
            data_dict[word] = []
            sql = "SELECT t.create_time,count(t.title) as count,'{}' as word FROM (SELECT text as title,screen_name as creator,created_at as create_time,'微博' as type from weibo  \
            UNION SELECT title,creator,create_time,'新闻' as type from school_news \
            UNION SELECT title,creator,create_time,'贴吧' as type from tieba ) t \
            where t.create_time>=:start_time and t.create_time<=:end_time and t.title like concat('%','{}','%') group by t.create_time "
            all_sql = all_sql+sql.format(word,word)
            if(t == len(word_data)-1):
               all_sql = all_sql+') ss order by ss.create_time'
            else:
                all_sql = all_sql+' UNION ' 
        print(all_sql)
        ret = db.session.execute(all_sql,params).fetchall()
        data = list(ret)
        
        for i in range(len(data)):
            item = dict(data[i])
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d')
            if(item['create_time'] not in xAxis):
                xAxis.append(item['create_time'])
            for t in range(len(legend)):   
                if(legend[t] == item['word']):
                    data_dict[legend[t]].append(item['count'])
                else:
                    data_dict[legend[t]].append(0)
        for g in range(len(legend)):      
            series.append({'name':legend[g],'type':'line','data':data_dict[legend[g]]})
        result = {'xAxis':xAxis,'series':series,'legend':legend}
        return ResponseResult.success(data=result)

    def getHotTopic(self,keywords,limit,page):
        sql = "SELECT t.topics,sum(t.attitudes_count) as attitudes_count,sum(t.comments_count) as comments_count,\
	    sum(t.reposts_count) as reposts_count  FROM(SELECT a.attitudes_count,a.comments_count,\
	    a.reposts_count,substring_index(substring_index(a.topics,\
		'；',b.help_topic_id + 1),'；',- 1) topics FROM weibo a JOIN mysql.help_topic b ON ( b.help_topic_id <(\
	    length(a.topics) - length(REPLACE (a.topics, '；', '')) + 1) AND a.topics IS NOT NULL AND a.topics != '')\
        WHERE a.topics IS NOT NULL and a.created_at >=:start_time and a.created_at <=:end_time ORDER BY a.id) t \
         GROUP BY t.topics ORDER BY attitudes_count desc,comments_count desc,reposts_count desc"
        start_time,end_time = get_last_week()
        params = {'start_time':start_time,'end_time':end_time}
        if(keywords):
            sql = "SELECT t.topics,sum(t.attitudes_count) as attitudes_count,sum(t.comments_count) as comments_count,\
            sum(t.reposts_count) as reposts_count  FROM(SELECT a.attitudes_count,a.comments_count,\
            a.reposts_count,substring_index(substring_index(a.topics,\
            '；',b.help_topic_id + 1),'；',- 1) topics FROM weibo a JOIN mysql.help_topic b ON ( b.help_topic_id <(\
            length(a.topics) - length(REPLACE (a.topics, '；', '')) + 1) AND a.topics IS NOT NULL AND a.topics != '')\
            WHERE a.topics IS NOT NULL and a.topics like concat('%',:keywords,'%') and a.created_at >=:start_time and a.created_at <=:end_time ORDER BY a.id) t \
            GROUP BY t.topics ORDER BY attitudes_count desc,comments_count desc,reposts_count desc"
            params['keywords'] = keywords
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
            item = dict(data[i])
            result.append(item)
        result_ = ResponseResult.lay_success(data=result, count=len(data))
        for i in result_['data']:
            i['attitudes_count'] = int(i['attitudes_count'])
            i['comments_count'] = int(i['comments_count'])
            i['reposts_count'] = int(i['reposts_count'])
        return result_

    def getLastTopic(self):
        sql = "select text as title from weibo order by created_at desc limit 10"
        ret = db.session.execute(sql).fetchall()
        data = list(ret)
        result = []
        for i in range(len(data)):
            item = dict(data[i])
            result.append(item)
        return ResponseResult.success(result)

    def getTopicCountByTime(self,topics,start_time,end_time):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        
        topic_list = topics.split(';')
        xAxis = []
        series = []
        legend = []
        data_dict = dict()
        all_sql = 'SELECT ss.* from ('
        for t in range(len(topic_list)):
            word = topic_list[t]
            params['word'] = word
            legend.append(word)
            data_dict[word] = []
            sql = "SELECT t.create_time,count(t.title) as count,'{}' as word FROM (SELECT text as title,screen_name as creator,created_at as create_time,'微博' as type from weibo  \
            UNION SELECT title,creator,create_time,'新闻' as type from school_news \
            UNION SELECT title,creator,create_time,'贴吧' as type from tieba ) t \
            where t.create_time>=:start_time and t.create_time<=:end_time and t.title like concat('%','{}','%') group by t.create_time "
            all_sql = all_sql+sql.format(word,word)
            if(t == len(topic_list)-1):
               all_sql = all_sql+') ss order by ss.create_time'
            else:
                all_sql = all_sql+' UNION ' 
        print(all_sql)
        ret = db.session.execute(all_sql,params).fetchall()
        data = list(ret)
        
        for i in range(len(data)):
            item = dict(data[i])
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d')
            if(item['create_time'] not in xAxis):
                xAxis.append(item['create_time'])
            for t in range(len(legend)):   
                if(legend[t] == item['word']):
                    data_dict[legend[t]].append(item['count'])
                else:
                    data_dict[legend[t]].append(0)
        for g in range(len(legend)):      
            series.append({'name':legend[g],'type':'line','data':data_dict[legend[g]]})
        result = {'xAxis':xAxis,'series':series,'legend':legend}
        return ResponseResult.success(data=result)

    
    def getNlpByTime(self,start_time,end_time):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        sql = "select DATE_FORMAT(create_time,'%Y-%m-%d') as create_time,nlp,count(id) \
         as count from nlp_result where create_time is not null and create_time>=:start_time and create_time<=:end_time \
          group by DATE_FORMAT(create_time,'%Y-%m-%d'),nlp order by DATE_FORMAT(create_time,'%Y-%m-%d')"
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        xAxis = []
        positive_list = []
        neutral_list = []
        negative_list = []
        positive_time = []
        neutral_time = []
        negative_time = []
        create_time = ''
        for i in range(len(data)):
            item = dict(data[i])
            if (item['create_time'] not in xAxis):
                xAxis.append(item['create_time'])
        for j in range(len(xAxis)):
            time_item = xAxis[j]
            positive_flag = False
            neutral_flag = False
            negative_flag = False
            for i in range(len(data)):
                item = dict(data[i])
                if(time_item == item['create_time'] ):
                    if(item['nlp'] == '积极'):
                        positive_list.append(item['count'])
                        positive_flag = True
                    if(item['nlp'] == '中立'):
                        neutral_list.append(item['count'])
                        neutral_flag = True
                    if(item['nlp'] == '消极'):
                        negative_list.append(item['count'])
                        negative_flag = True
            if(positive_flag == False):
                positive_list.append(0)
            if (neutral_flag == False):
                neutral_list.append(0)
            if (negative_flag == False):
                negative_list.append(0)

        return ResponseResult.success({'xAxis':xAxis,'positive_list':positive_list
        ,'negative_list':negative_list,'neutral_list':neutral_list})

    def getNlpMap(self,start_time,end_time):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        sql = "select nlp,count(id) as count from nlp_result where create_time is not null \
        and create_time>=:start_time and create_time<=:end_time \
          group by nlp "
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        series = []
        legend = []
        for i in range(len(data)):
            item = dict(data[i])
            series.append({'name':item['nlp'],'value':item['count']})
            legend.append(item['nlp'])
        return ResponseResult.success({'legend':legend,'series':series})

    def getNlpData(self,start_time,end_time,limit,page):
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d')
        date_from = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
        date_to = datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)
        params = {'start_time':str(date_from),'end_time':str(date_to)}
        sql = "select * from nlp_result where create_time is not null \
        and create_time>=:start_time and create_time<=:end_time  "
        ret = db.session.execute(sql,params).fetchall()
        data = list(ret)
        start = (page - 1) * limit
        end = page * limit if len(data) > page * limit else len(data)
        result = []
        for i in range(start,end):
            item = dict(data[i])
            item['create_time'] = item['create_time'].strftime('%Y-%m-%d %H:%M')
            result.append(item)
        return ResponseResult.lay_success(data=result,count=len(data))

    





