# -*- coding: UTF-8 -*-
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
from data_spider import data_spider
# from gener_word import GenerWord
# from nlp_util import NLPUTIL

# 错误监控
from gener_word import GenerWord
from nlp_util import NLPUTIL


def my_listener(event):
    if event.exception:
        print ('任务出错了！！！！！！')
    else:
        print ('任务照常运行...')
# 定时采集数据
def spider():
    print('采集任务开始:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    app = data_spider()
    app.start_spider()
    print('采集任务结束:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# 定时生成词云图
def build_wordcloud():
    print('生成词云图任务开始:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    app = GenerWord()
    app.build_word()
    print('生成词云图任务结束:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# 定时生成情感分析数据
def build_nlp():
    print('生成情感分析任务开始:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    app = NLPUTIL()
    app.build_nlp_result()
    print('生成情感分析任务结束:'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# 任务
def start():
    print('创建任务')
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # 添加采集定时任务
    scheduler.add_job(spider, 'interval',seconds=10)
    # 添加生成词云定时任务
    #scheduler.add_job(build_wordcloud, 'interval',seconds=20)
    # # 添加构建情感分析定时任务
    #scheduler.add_job(build_nlp, 'interval',seconds=20)
    scheduler.start()



if __name__ == "__main__":
    start()



