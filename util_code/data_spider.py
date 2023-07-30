#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import copy
import csv
import json
import math
import os
import random
import sys
import traceback
from collections import OrderedDict
from datetime import date, datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import time
import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from tqdm import tqdm
import re
from bs4 import BeautifulSoup
import requests
from database_util import database_util
from config import *
from lxml import html
from html import unescape
import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains

# 数据采集
class data_spider:
    def __init__(self):
        self.database = database_util()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'Cookie':'BAIDUID=9A82F239794FF9B49742FF4563CFCB66:FG=1; BIDUPSID=0B097167FC39E838BADB2607063B55E1; PSTM=1662628771; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1688733895,1689504165,1689680917,1689731689; BDUSS=1JNRkNWQUc0SFNLUzdjU3Y5MTEycWhaWjFEZDREaX5-RWJUc2h2SWlEV2lPUmxrRVFBQUFBJCQAAAAAAAAAAAEAAAAJEw3ooPvp7gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKKs8WOirPFjR; FPTOKEN=30$DINXZ3RMH8eRD4NqT1/gP0vZHtK1m3Dkr0N2FWq+4lr9mA9LzB+oCrVySlVJvfOLiZ4ZvrMeY3r/l/6Cbyw7GnFfojxm3HU+uFzA2bN43bcK7UpU0Ey/Y5M9GswcpjgbFyS6LSTgZIpiWmd4b5cd0liBbkF/a9nu73VH6Fvc5K/sZKNLZA7fcY/k5xOHXWtUKRvAdJYzgkRWa5uxsx5aUBtRpxp2OmOiK9DWkHjYNUS4CoL0C9VlQVEA0K+KJa2dwgHXn2K0rICMmVegYEO65kzBrUuA18NGXijdLOLcag5hNpavie6JoyvtOjmswkUISdTvixDpADX6dwi7WgdMymAoKWumWc7tyPj8txzabefKluu15LWgfiKTGBv19vLh|6vNL/LFTEHgNQ5SxEFt5b5Dz0xKQMn56GT6UEg0h828=|10|cbe7d888c25559cad6c43b9185b2e036; MAWEBCUID=web_VnwwFxRLeVAgykMMRMlTWRfKqaHOAtLQrYjxGcbPcsSjvrGUBp; rpln_guide=1; STOKEN=c331c9abcf4f5851ffc2c974326e01d109ae01bb820220da5e527045c63c78a2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-%3A; BA_HECTOR=850g0gah000100al812g84831ibepsn1o; ZFY=g6Uh6bvYpw926vyUdh:BHBDpOs0nAB5xv37:AptdDPooU:C; tb_as_data=63905008c22ac161c0a38896040e80f022f37667609d5f80b7fca37ab8dcda56e37a863faccfdad8cb91b20ccc9899bc16bf23f004e8fe134d56f32dd4860025a918eddb78735a7e78ed520bc41fee43a1a41669046661e06f3f98202a326fc6; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1689741206; RT="z=1&dm=baidu.com&si=574a5744-c200-41d8-b41d-ea319fabcaeb&ss=lk98aahg&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=bi7&ul=y10"; BAIDU_WISE_UID=wapp_1689731689137_901; USER_JUMP=-1; 3893170953_FRSVideoUploadTip=1; video_bubble3893170953=1; XFI=67ac3540-25ed-11ee-8e32-856043ddd4e1; XFCS=1E20F601DB81E8BEBED59DAD13DB290038EA3DBAB57E8514C1644CD4EBA73530; ab_sr=1.0.1_NWUzMDQyOWNiNDgzMjQ3NTBmYzcwN2Q0Nzk3YWViN2FiYjk4ZWFmZjg1NTM1MGMwMzA4MWU2OTI3YWZlMjc2MmFlNmQwNDQ3NDI2ZGM4MGJhNDc5YTM1MGFkZTRjNTk3OWQ2NGNmOTZjMjVjOGQ4YTcyNTNkYWM5YmI2ZGEyNWU5NTg3ZTgxZTU5YjZiMDYwM2UzMGQ1YmNkYTQzNjIwODY0YWQyMDc1MDY3NzYxMmQzYzZlM2U5ZjEyZWY2NGUz; st_data=91eb6442119cf8e139011642a4ed937a6c4019c63350a26cbc26436ae2f21a1b3fa04986dde83487e6174ed7e4bf3fd8a06d95220cc55f4930b63c14ab2ca5f8c173ef8dcbb20a67f05b8fea446efd872f4bc3fd12e752b3d2e9f7274820e5d22913777f968b99cf2d1acbca09f244533751b189363eb7dd8702235d5c1c84c536be11b737e8052d365b1d08993d1ae0; st_key_id=17; st_sign=d8e9c01d; arialoadData=false; XFT=EKMj2fZLO73jb1Ow/LOI3dDlBeCgUTjV6MsQfu4Rr44=; top_list=8075744650-8075739015; delPer=0; PSINO=6; H_PS_PSSID=36543_38643_38831_39025_39024_38942_38882_38955_38807_38825_39089_26350_39100; wise_device=0'
        }
        self.cookie = {'Cookie': weibo_config['cookie']}  # 微博cookie，可填可不填
        self.user = {}  # 存储目标微博用户信息
        self.got_count = 0  # 存储爬取到的微博数
        self.weibo = []  # 存储爬取到的所有微博信息
        self.weibo_id_list = []  # 存储爬取到的所有微博id
        self.comments = [] # 存储爬取到的所有评论
        self.mysql_config = weibo_config['mysql_config']
        # self.since_date = datetime.now().strftime('%Y-%m-%d')
        self.since_date = (datetime.today() - timedelta(180)).strftime('%Y-%m-%d')
        # chrome_driver = r"D:\_Application\Python\Python38\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
        # path = Service(chrome_driver)
        # self.driver = webdriver.Chrome(service=path)
        self.weibo_num = 1
        self.mysql_config = weibo_config['mysql_config']
        # self.since_date = datetime.now().strftime('%Y-%m-%d')
        self.since_date = (datetime.today() - timedelta(180)).strftime('%Y-%m-%d')
        self.con_id = '1008085cd4f88d13c3119a7fe6171be680cc74_-_sort_time'
        self.lfid_name = '100103type%3D1%26q%3D%E4%B8%9C%E5%8C%97%E5%A4%A7%E5%AD%A6'
        self.since_id = None
        self.just_comment = True
        self.proxy_list = []

        with open('../app/static/proxy.txt', 'r') as file:
            for line in file:
                self.proxy_list.append(line.strip())

    def start_spider(self):
        for item in spider_list:
            if(item == 'news'):
                self.spider_news()
            elif(item == 'tieba'):
                self.spider_tieba()
            elif(item == 'weibo'):
                self.spider_weibo()
    
    #已解决
    def spider_news(self):
        base_url = 'http://neunews.neu.edu.cn/ddyw/list{}.htm'
        host = 'http://neunews.neu.edu.cn'
        news_items_list = []  # 创建一个空列表，用于保存所有新闻的item
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Cookie": "JSESSIONID = 013D024F54EA867471B236B512543178",
            "Host": "neunews.neu.edu.cn"
        }

        for page_num in range(1, 16):
            url = base_url.format(page_num)
            response = requests.get(url, headers=header)
            print(f'正在爬取第{page_num}页！')
            sleep(0.25)
            if response.status_code == 200:
                page_content = response.content
            else:
                print(f"无法访问第{page_num}页！")
                continue

            soup = BeautifulSoup(page_content, 'html.parser')
            news_list = soup.find('ul', class_='news_list')
            news_items = news_list.find_all('li', class_='news')
            print(news_items)

            for item in news_items:
                news_title = item.find('span', class_='news_title').a.text.strip()
                news_time = item.find('span', class_='news_meta').text.strip()
                news_link = host + item.find('span', class_='news_title').a['href']

                # 访问详情页获取完整标题和新闻内容
                detail_response = requests.get(news_link, headers=header)
                # 为了防止请求过于频繁，加入适当延时
                time.sleep(0.5)
                if detail_response.status_code == 200:
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    full_news_title = detail_soup.title.text.strip()

                    # 获取新闻内容
                    news_content = detail_soup.find('div', class_='entry').text.strip()
                else:
                    print(f"无法访问新闻详情页：{news_link}")
                    full_news_title = news_title  # 若无法访问详情页，仍使用列表页的标题
                    news_content = "无法获取新闻内容"  # 若无法访问详情页，设置一个默认的提示信息

                # 构建字典来保存新闻信息
                item = dict()
                item['title'] = full_news_title
                item['creator'] = '东北大学官网'
                item['create_time'] = news_time
                item['content'] = news_content
                item['link'] = news_link
                print(item)
                news_items_list.append(item)  # 将每个新闻的item添加到news_items_list列表中

        self.database.save_news(news_items_list)


    
    # 采集百度贴吧的数据
    def spider_tieba(self):
        url = 'https://tieba.baidu.com/f?kw=%E4%B8%9C%E5%8C%97%E5%A4%A7%E5%AD%A6'
        self.spider_tieba_list(url)
    
     
    def GetMiddleStr(self,content,startStr,endStr):
        patternStr = r'%s(.+?)%s'%(startStr,endStr)
        p = re.compile(patternStr,re.IGNORECASE)
        m= re.match(p,content)
        if m:
            return m.group(1)

    # 时间转换
    def get_time_convert(self,timeStr):
        if(re.match('^\d{1,2}:\d{1,2}$',timeStr) != None):
            day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            timeStr = day+' '+timeStr+':00'
        elif(re.match('^\d{4}-\d{1,2}$',timeStr) != None):
            day = time.strftime('%d',time.localtime(time.time()))
            timeStr = timeStr+'-'+day+' 00:00:00'
        elif(re.match('^\d{1,2}-\d{1,2}$',timeStr) != None):
            day = time.strftime('%Y',time.localtime(time.time()))
            timeStr = day+'-'+timeStr+' 00:00:00'
        
        timeStr = time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
        
        return timeStr


    # 过滤表情
    def filter_emoji(self,desstr,restr=''):  
        try:  
            co = re.compile(u'[\U00010000-\U0010ffff]')  
        except re.error:  
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')  
        return co.sub(restr, desstr)

    # 采集百度贴吧列表数据
    def spider_tieba_list(self,url):
        print(url)
        proxy = random.choice(self.proxy_list)
        proxies = {
            'http': f'http://{proxy}'
        }
        response = requests.get(url,headers=self.headers,proxies=proxies)
        time.sleep(random.randint(1,2))
        try:
            response_txt = str(response.content,'utf-8')
            time.sleep(random.randint(1,2))
            print(response_txt)
        except Exception as e:
            response_txt = str(response.content,'gbk')
            time.sleep(random.randint(1, 2))
        # response_txt = str(response.content,'utf-8')
        bs64_str = re.findall('<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;">[.\n\S\s]*?</code>', response_txt)
        bs64_str = ''.join(bs64_str).replace('<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;"><!--','')
        bs64_str = bs64_str.replace('--></code>','')
        html = etree.HTML(bs64_str)
        # print(thread_list)
        # 标题列表
        title_list = html.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a[1]/@title')
        # print(title_list)
        # 链接列表
        link_list = html.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a[1]/@href')
        # 发帖人
        creator_list = html.xpath('//div[@class="threadlist_author pull_right"]/span[@class="tb_icon_author "]/@title')
        # 发帖时间
        create_time_list = html.xpath('//div[@class="threadlist_author pull_right"]/span[@class="pull-right is_show_create_time"]/text()')
        creator_list = creator_list[1:]
        create_time_list = create_time_list[1:]
        # print(create_time_list)
        # print(create_time_list[1])
        for i in range(len(title_list)):
            item = dict()
            if(i< len(create_time_list)):
                item['create_time'] = create_time_list[i]
            else:
                item['create_time'] = '广告' 
            if(item['create_time'] == '广告'):
                continue
            item['create_time'] = self.get_time_convert(item['create_time'])
            #print(item['create_time'])
            item['title'] = self.filter_emoji(title_list[i])
            item['link'] = 'https://tieba.baidu.com'+link_list[i]
            item['creator'] = self.filter_emoji(creator_list[i]).replace('主题作者: ','')
            item['content'] = self.filter_emoji(item['title'])
            print(item)
            # 保存帖子数据
            result = self.database.query_tieba(item['link'])
            if(not result):
                self.database.save_tieba(item)
            self.spider_tieba_detail(item['link'])
        # 定时采集任务则只采集最新的一页数据
        # 如果有下一页继续采集下一页
        nex_page = html.xpath('//a[@class="next pagination-item "]/@href')
        if(len(nex_page)>0):
            next_url = 'https:'+nex_page[0]
            self.spider_tieba_list(next_url)

    # 采集帖子详情页
    def spider_tieba_detail(self,link):
        proxy = random.choice(self.proxy_list)
        proxies = {
            'http': f'http://{proxy}'
        }
        response = requests.get(link,headers=self.headers,proxies=proxies)
        time.sleep(random.randint(1,2))
        html = etree.HTML(response.text)
        data_fields = html.xpath('//*[@id="j_p_postlist"]/div/@data-field')
        # html = etree.HTML(str(response.content,'utf-8'))
        author_list = html.xpath('//div[@id="j_p_postlist"]/div/div[@class="d_author"]/ul/li[@class="d_name"]/a/text()')
        content_list = html.xpath('//cc/div[@class="d_post_content j_d_post_content "]')
        content_list = [''.join(i.xpath('.//text()')) for i in content_list]
        create_time = html.xpath('//div/div[@class="core_reply_tail clearfix"]')
        create_time =[i.xpath('.//span[@class="tail-info"]/text()')[-1] for i in create_time]
        for j in range(len(data_fields)):
            data_field = data_fields[j]
            data = json.loads(data_field)
            reply_item = dict()
            reply_item['content'] = self.filter_emoji(content_list[j])
            reply_item['creator'] = self.filter_emoji(author_list[j])
            reply_item['create_time'] = create_time[j]
            reply_item['link'] = link            
            reply_item['reply_id'] = data['content']['post_id']
            reply_result = self.database.query_tieba_reply(reply_item['reply_id'])
            if(not reply_result):
                self.database.save_tieba_reply(reply_item)
        nex_page = html.xpath('//ul[@class="l_posts_num"]/li[@class="l_pager pager_theme_5 pb_list_pager"]/a/@href')
        nex_page_text = html.xpath('//ul[@class="l_posts_num"]/li[@class="l_pager pager_theme_5 pb_list_pager"]/a/text()')
        if(len(nex_page)>0):
            for t in range(len(nex_page_text)):
                if(nex_page_text[t]=='下一页'):
                    next_url = 'https://tieba.baidu.com'+nex_page[t]
                    self.spider_tieba_detail(next_url)

        
    def spider_weibo(self):
        self.get_pages()
        self.get_comments()

    def get_pages(self):
        """获取全部微博"""
        self.get_user_info()
        page_count = self.get_page_count()
        wrote_count = 0
        page1 = 0
        random_pages = random.randint(1, 5)
        self.start_date = datetime.now().strftime('%Y-%m-%d')
        for page in tqdm(range(1, page_count + 1), desc='Progress'):
            is_end = self.get_one_page(page)
            if is_end:
                break
            if page % 10 == 0:  # 每爬20页写入一次文件
                self.weibo_to_mysql(wrote_count)
                wrote_count = self.got_count
                print(self.since_id)
                with open('since_id.txt', mode='a') as f:
                    f.write(str(self.since_id) + '\n')
                    f.flush()

            # 通过加入随机等待避免被限制。爬虫速度过快容易被系统限制(一段时间后限
            # 制会自动解除)，加入随机等待模拟人的操作，可降低被系统限制的风险。默
            # 认是每爬取1到5页随机等待6到10秒，如果仍然被限，可适当增加sleep时间
            if (page - page1) % random_pages == 0 and page < page_count:
                sleep(random.randint(6, 10))
                page1 = page
                random_pages = random.randint(1, 5)

        self.weibo_to_mysql(wrote_count)  # 将剩余不足20页的微博写入文件
        print(u'微博爬取完成，共爬取%d条微博' % self.got_count)

    def get_user_info(self):
        """获取用户信息"""
        # params = {'containerid': '100505' + str(weibo_config['user_id'])}
        params = {'containerid': self.con_id,
                  'luicode': '10000011',
                  'lfid': self.lfid_name,
                  'since_id': self.since_id
                  }
        js = self.get_json(params)

        if js['ok']:
            # print(js['data'])
            info = js['data']['pageInfo']
            user_info = {}
            user_info['id'] = info.get('page_title', '')
            user_info['screen_name'] = info.get('screen_name', '')
            user_info['gender'] = info.get('gender', '')
            user_info['statuses_count'] = info.get('total', 0)
            user_info['followers_count'] = info.get('followers_count', 0)
            user_info['follow_count'] = info.get('follow_count', 0)
            user_info['description'] = info.get('description', '')
            user_info['profile_url'] = info.get('profile_url', '')
            user_info['profile_image_url'] = info.get('profile_image_url', '')
            user_info['avatar_hd'] = info.get('avatar_hd', '')
            user_info['urank'] = info.get('urank', 0)
            user_info['mbrank'] = info.get('mbrank', 0)
            user_info['verified'] = info.get('verified', False)
            user_info['verified_type'] = info.get('verified_type', 0)
            user_info['verified_reason'] = info.get('verified_reason', '')
            user = self.standardize_info(user_info)
            self.user = user

    def standardize_info(self, weibo):
        """标准化信息，去除乱码"""
        for k, v in weibo.items():
            if 'bool' not in str(type(v)) and 'int' not in str(
                    type(v)) and 'list' not in str(
                type(v)) and 'long' not in str(type(v)):
                weibo[k] = v.replace(u"\u200b", "").encode(
                    sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
        return weibo

    def get_page_count(self):
        """获取微博页数"""
        try:
            weibo_count = self.user['statuses_count']
            page_count = int(math.ceil(weibo_count / 10.0))
            return 250
        except KeyError:
            sys.exit(u'程序出错')

    def get_one_page(self, page):
        """获取一页的全部微博"""
        try:
            js = self.get_weibo_json(page)
            print()
            if js['ok']:
                # print(js['data']['cards'][0])
                weibos = js['data']['cards']
                # weibos = js['data']['cards'][0]['card_group']#超话用

                # print(weibos)

                for w in weibos:
                    if int(w['card_type']) == 9:
                        wb = self.get_one_weibo(w)
                        try:
                            print(self.weibo_num, wb['text'])
                            self.weibo_num += 1
                        except:
                            pass
                        if wb:
                            # print(wb['id'])
                            # print(self.weibo_id_list)
                            if wb['id'] in self.weibo_id_list:
                                continue
                            wb['created_at'] = self.getTimeConvert(wb['created_at'])
                            since_date = datetime.strptime(
                                self.since_date, '%Y-%m-%d')
                            if wb['created_at'] < since_date:
                                if self.is_pinned_weibo(w):
                                    continue
                                else:
                                    print(u'{}已获取{}({})的第{}页微博{}'.format(
                                        '-' * 30, self.user['screen_name'],
                                        self.user['id'], page, '-' * 30))
                                    return True
                            if ('retweet' not in wb.keys()):
                                self.weibo.append(wb)
                                self.weibo_id_list.append(wb['id'])
                                self.got_count += 1
            print(u'{}已获取{}({})的第{}页微博{}'.format('-' * 30,
                                                 self.user['screen_name'],
                                                 self.user['id'], page,
                                                 '-' * 30))
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def is_pinned_weibo(self, info):
        """判断微博是否为置顶微博"""
        weibo_info = info['mblog']
        title = weibo_info.get('title')
        if title and title.get('text') == u'置顶':
            return True
        else:
            return False

    def get_weibo_json(self, page):
        """获取网页中微博json数据"""
        # params = {
        #     'containerid': '107603' + str(weibo_config['user_id']),
        #     'page': page
        # }
        params = {'containerid': self.con_id,
                  'luicode': '10000011',
                  'lfid': self.lfid_name,
                  'since_id': self.since_id
                  }
        js = self.get_json(params)
        try:
            self.since_id = js['data']['pageInfo']['since_id']
            # print(self.since_id)

        except:
            time.sleep(2)
        return js

    def get_json(self, params):
        """获取网页中json数据"""
        url = 'https://m.weibo.cn/api/container/getIndex?'
        r = requests.get(url, params=params, cookies=self.cookie)
        # print(r.url)
        return r.json()

    def get_one_weibo(self, info):
        """获取一条微博的全部信息"""
        try:
            weibo_info = info['mblog']
            weibo_id = weibo_info['id']
            retweeted_status = weibo_info.get('retweeted_status')
            is_long = weibo_info.get('isLongText')
            if retweeted_status:  # 转发
                retweet_id = retweeted_status.get('id')
                is_long_retweet = retweeted_status.get('isLongText')
                if is_long:
                    weibo = self.get_long_weibo(weibo_id)
                    if not weibo:
                        weibo = self.parse_weibo(weibo_info)
                else:
                    weibo = self.parse_weibo(weibo_info)
                if is_long_retweet:
                    retweet = self.get_long_weibo(retweet_id)
                    if not retweet:
                        retweet = self.parse_weibo(retweeted_status)
                else:
                    retweet = self.parse_weibo(retweeted_status)
                retweet['created_at'] = self.standardize_date(
                    retweeted_status['created_at'])
                weibo['retweet'] = retweet
            else:  # 原创
                if is_long:
                    weibo = self.get_long_weibo(weibo_id)
                    if not weibo:
                        weibo = self.parse_weibo(weibo_info)
                else:
                    weibo = self.parse_weibo(weibo_info)
            weibo['created_at'] = self.standardize_date(
                weibo_info['created_at'])
            return weibo
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_long_weibo(self, id):
        """获取长微博"""
        for i in range(3):
            url = 'https://m.weibo.cn/status/%s' % id
            html = requests.get(url).text
            html = html[html.find('"status":'):]
            html = html[:html.rfind('"hotScheme"')]
            html = html[:html.rfind(',')]
            html = '{' + html + '}'
            html = re.findall("""(.*?)]\[0] || \{};.*}""", html, re.S)[0]  # 修改re代码
            try:
                js = json.loads(html, strict=False)
                weibo_info = js.get('status')
                if weibo_info:
                    weibo = self.parse_weibo(weibo_info)
                    return weibo
            except:
                pass
            sleep(random.randint(3, 5))

    def parse_weibo(self, weibo_info):
        weibo = OrderedDict()
        if weibo_info['user']:
            weibo['user_id'] = weibo_info['user']['id']
            weibo['screen_name'] = weibo_info['user']['screen_name']
        else:
            weibo['user_id'] = ''
            weibo['screen_name'] = ''
        weibo['id'] = int(weibo_info['id'])
        weibo['bid'] = weibo_info['bid']
        text_body = weibo_info['text']
        selector = etree.HTML(text_body)
        weibo['text'] = etree.HTML(text_body).xpath('string(.)')
        weibo['text'] = self.clear_character_chinese(weibo['text'])
        weibo['pics'] = self.get_pics(weibo_info)
        weibo['video_url'] = self.get_video_url(weibo_info)
        weibo['location'] = self.get_location(selector)
        weibo['created_at'] = weibo_info['created_at']
        weibo['source'] = weibo_info['source']
        weibo['attitudes_count'] = self.string_to_int(
            weibo_info.get('attitudes_count', 0))
        weibo['comments_count'] = self.string_to_int(
            weibo_info.get('comments_count', 0))
        weibo['reposts_count'] = self.string_to_int(
            weibo_info.get('reposts_count', 0))
        weibo['topics'] = self.get_topics(selector, weibo['text'])
        weibo['at_users'] = self.get_at_users(selector)
        return self.standardize_info(weibo)

    # 去除字母数字表情和其它字符
    def clear_character_chinese(self, sentence):
        pattern1 = '[a-zA-Z0-9]'
        pattern2 = '\[.*?\]'
        pattern3 = re.compile(u'[^\s1234567890:：' + '\u4e00-\u9fa5]+')
        pattern4 = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
        line2 = re.sub(pattern2, '', sentence)  # 去除表情
        new_sentence = ''.join(line2.split())  # 去除空白
        return new_sentence

    def get_pics(self, weibo_info):
        """获取微博原始图片url"""
        if weibo_info.get('pics'):
            pic_info = weibo_info['pics']
            pic_list = [pic['large']['url'] for pic in pic_info]
            pics = ','.join(pic_list)
        else:
            pics = ''
        return pics

    def get_live_photo(self, weibo_info):
        """获取live photo中的视频url"""
        live_photo_list = []
        live_photo = weibo_info.get('pic_video')
        if live_photo:
            prefix = 'https://video.weibo.com/media/play?livephoto=//us.sinaimg.cn/'
            for i in live_photo.split(','):
                if len(i.split(':')) == 2:
                    url = prefix + i.split(':')[1] + '.mov'
                    live_photo_list.append(url)
            return live_photo_list

    def get_video_url(self, weibo_info):
        """获取微博视频url"""
        video_url = ''
        video_url_list = []
        if weibo_info.get('page_info'):
            if weibo_info['page_info'].get('media_info') and weibo_info[
                'page_info'].get('type') == 'video':
                media_info = weibo_info['page_info']['media_info']
                video_url = media_info.get('mp4_720p_mp4')
                if not video_url:
                    video_url = media_info.get('mp4_hd_url')
                    if not video_url:
                        video_url = media_info.get('mp4_sd_url')
                        if not video_url:
                            video_url = media_info.get('stream_url_hd')
                            if not video_url:
                                video_url = media_info.get('stream_url')
        if video_url:
            video_url_list.append(video_url)
        live_photo_list = self.get_live_photo(weibo_info)
        if live_photo_list:
            video_url_list += live_photo_list
        return ';'.join(video_url_list)

    def get_location(self, selector):
        """获取微博发布位置"""
        location_icon = 'timeline_card_small_location_default.png'
        span_list = selector.xpath('//span')
        location = ''
        for i, span in enumerate(span_list):
            if span.xpath('img/@src'):
                if location_icon in span.xpath('img/@src')[0]:
                    location = span_list[i + 1].xpath('string(.)')
                    break
        return location

    def get_topics(self, selector, context):
        """获取参与的微博话题"""
        span_list = selector.xpath("//span[@class='surl-text']")
        topics = ''
        topic_list = []
        for span in span_list:
            text = span.xpath('string(.)')
            if len(text) > 2 and text[0] == '#' and text[-1] == '#':
                topic_list.append(text[1:-1])
        if topic_list:
            topics = ';'.join(topic_list)
        if topics == '':
            context_list = re.findall('#(.*?)#', context, re.S)
            if context_list:
                topics = ';'.join(context_list)
        return topics

    def get_at_users(self, selector):
        """获取@用户"""
        a_list = selector.xpath('//a')
        at_users = ''
        at_list = []
        for a in a_list:
            if '@' + a.xpath('@href')[0][3:] == a.xpath('string(.)'):
                at_list.append(a.xpath('string(.)')[1:])
        if at_list:
            at_users = ','.join(at_list)
        return at_users

    def string_to_int(self, string):
        """字符串转换为整数"""
        if isinstance(string, int):
            return string
        elif string.endswith(u'万+'):
            string = int(string[:-2] + '0000')
        elif string.endswith(u'万'):
            string = int(string[:-1] + '0000')
        return int(string)

    def standardize_date(self, created_at):
        """标准化微博发布时间"""
        if u"刚刚" in created_at:
            created_at = datetime.now().strftime("%Y-%m-%d")
        elif u"分钟" in created_at:
            minute = created_at[:created_at.find(u"分钟")]
            minute = timedelta(minutes=int(minute))
            created_at = (datetime.now() - minute).strftime("%Y-%m-%d")
        elif u"小时" in created_at:
            hour = created_at[:created_at.find(u"小时")]
            hour = timedelta(hours=int(hour))
            created_at = (datetime.now() - hour).strftime("%Y-%m-%d")
        elif u"昨天" in created_at:
            day = timedelta(days=1)
            created_at = (datetime.now() - day).strftime("%Y-%m-%d")
        elif created_at.count('-') == 1:
            year = datetime.now().strftime("%Y")
            created_at = year + "-" + created_at
        return created_at

    def getTimeConvert(self,data):
        time_format=datetime.strptime(data,'%a %b %d %H:%M:%S %z %Y')
        time_format=str(time_format)
        times=time_format[0:10]
        return datetime.strptime(times, "%Y-%m-%d")

    # 获取全部微博的评论
    def get_comments(self):
        write_count = 0
        for mid in self.weibo_id_list:
            try:
                m_id = 0
                id_type = 0
                jsondata = self.get_comments_page(m_id, id_type,mid=mid)
                results = self.parse_comments_page(jsondata)
                if results['max']:
                    maxpage = results['max']
                    print('页数',maxpage)
                    for page in range(maxpage):
                        print('采集第{}页的微博'.format(page))
                        jsondata = self.get_comments_page(m_id, id_type,mid)
                        # print(jsondata)
                        datas = jsondata.get('data').get('data')
                        self.add_comments_json(datas)
                        if(len(self.comments)%100 == 0):
                            self.comments_to_mysql(write_count)
                            write_count = write_count+100
                        results = self.parse_comments_page(jsondata)
                        sleep(random.randint(2,4))
                        if page%30==0:
                            sleep(6)
                        m_id = results['max_id']
                        id_type = results['max_id_type']    
            except Exception as e:
                print(e)
                pass           
        self.comments_to_mysql(write_count)
    def add_comments_json(self,jsondata):
        for data in jsondata:
            item = dict()
            item['id'] = data.get('id')
            item['mid'] = data.get('mid')
            item['like_count'] = data.get("like_count")
            item['source'] = data.get("source")
            item['floor_number'] = data.get("floor_number")
            item['screen_name'] = data.get("user").get("screen_name")
            # 性别
            item['gender'] = data.get("user").get("gender")
            if(item['gender'] == 'm'):
                item['gender'] = '男'
            elif(item['gender'] == 'f'):
                item['gender'] = '女'
            item['rootid'] = data.get("rootid")
            item['create_time'] = data.get("created_at")
            import time
            item['create_time'] = time.strptime(item['create_time'], '%a %b %d %H:%M:%S %z %Y')
            item['create_time'] = time.strftime('%Y-%m-%d',item['create_time'])
            item['comment'] = data.get("text")
            item['comment'] = BeautifulSoup(item['comment'], 'html.parser').get_text()
            item['comment'] = self.clear_character_chinese(item['comment'])
            print('当前楼层{},评论{}'.format(item['floor_number'],item['comment']))
            # 评论这条评论的信息
            comments = data.get("comments")
            if(comments):
                self.add_comments_json(comments)
            # print jsondata.dumps(comment, encoding="UTF-8", ensure_ascii=False)
            self.comments.append(item)
            
    def get_comments_page(self,max_id, id_type,mid):
        from get_weibo_cookie import get_cookie
        params = {
            'max_id': max_id,
            'max_id_type': id_type
            }
        try:
            url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={mid}'
        #     headers = {
        #     'Cookie': 'T_WM=96849642965; __guid=52195957.2500582256236055600.1583058027995.9556; WEIBOCN_FROM=1110006030; SCF=Aimq85D9meHNU4Ip0PFUjYBTDjXFB0VtQr3EKoS8DHQDobRNUO3lDIufAcUg69h4J7BQWqryxQpuU3ReIHHxvQ4.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5H0p180lDMiCjNvXD_-uOh5JpX5KzhUgL.FoM0S0n0eo-0Sh.2dJLoI0qLxKqL1KMLBK-LxK-LBonLBonLxKMLB.-L12-LxK-LBK-LBoeLxK-L1hnL1hqLxKBLB.2LB-zt; XSRF-TOKEN=ca0a29; SUB=_2A25zWlwFDeRhGeFN7FoS8ivPzzWIHXVQpWRNrDV6PUJbkdANLW_9kW1NQ8CH90H5f8j5r1NA4GNPvu6__ERL-Jat; SUHB=0vJIkXXtLIIaZO; SSOLoginState=1583230037; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4474164293517551%26luicode%3D20000174%26lfid%3D102803%26uicode%3D20000174; monitor_count=45',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        #     'X-Requested-With': 'XMLHttpRequest'
        # }
            r = requests.get(url.format(id=mid,mid=mid), params=params)
            time.sleep(random.randint(1,2))
            print(r.url)
            if r.status_code == 200:
                return r.json()
        except requests.ConnectionError as e:
            print('error', e.args)    
    
    def add_comments(self,jsondata):
        datas = jsondata.get('data').get('data')
        for data in datas:
            item = dict()
            item['id'] = data.get('id')
            item['mid'] = data.get('mid')
            item['like_count'] = data.get("like_count")
            item['source'] = data.get("source")
            item['floor_number'] = data.get("floor_number")
            item['screen_name'] = data.get("user").get("screen_name")
            # 性别
            item['gender'] = data.get("user").get("gender")
            if(item['gender'] == 'm'):
                item['gender'] = '男'
            elif(item['gender'] == 'f'):
                item['gender'] = '女'
            item['created_at'] = self.standardize_date(
                data.get(['created_at']))
            import time
            item['create_time'] = time.strptime(item['create_time'], '%a %b %d %H:%M:%S %z %Y')
            item['create_time'] = time.strftime('%Y-%m-%d',item['create_time'])
            item['rootid'] = data.get("rootid")
            
            item['comment'] = data.get("text")
            item['comment'] = BeautifulSoup(item['comment'], 'html.parser').get_text()
            item['comment'] = self.clear_character_chinese(item['comment'])
            print('当前楼层{},评论{}'.format(item['floor_number'],item['comment']))
            # 评论这条评论的信息
            comments = data.get("comments")

            # print jsondata.dumps(comment, encoding="UTF-8", ensure_ascii=False)
            self.comments.append(item)

    def parse_comments_page(self,jsondata):
        if jsondata:
            items = jsondata.get('data')
            item_max_id = {}
            item_max_id['max_id'] = items['max_id']
            item_max_id['max_id_type'] = items['max_id_type']
            item_max_id['max'] = items['max']
            return item_max_id    

    def weibo_to_mysql(self, wrote_count):
        """将爬取的微博信息写入MySQL数据库"""
        mysql_config = {
        }
        weibo_list = []
        retweet_list = []
        info_list = self.weibo[wrote_count:]
        for w in info_list:
            w['text'] = self.filter_emoji(w['text'], restr='')  ###删除特殊符号
            if 'retweet' in w:
                w['retweet']['retweet_id'] = ''
                retweet_list.append(w['retweet'])
                w['retweet_id'] = w['retweet']['id']
                del w['retweet']
            else:
                w['retweet_id'] = ''
            weibo_list.append(w)
        # 在'weibo'表中插入或更新微博数据
        self.mysql_insert(mysql_config, 'weibo', retweet_list)
        self.mysql_insert(mysql_config, 'weibo', weibo_list)
        print(u'%d条微博写入MySQL数据库完毕' % self.got_count)

    def comments_to_mysql(self,write_count):
        """将爬取的用户信息写入MySQL数据库"""
        mysql_config = {
        }
        self.mysql_insert(mysql_config, 'comments', self.comments[write_count:])

    def mysql_insert(self, mysql_config, table, data_list):
        """向MySQL表插入或更新数据"""
        import pymysql

        if len(data_list) > 0:
            keys = ', '.join(data_list[0].keys())
            values = ', '.join(['%s'] * len(data_list[0]))
            if self.mysql_config:
                mysql_config = self.mysql_config
            connection = pymysql.connect(**mysql_config)
            cursor = connection.cursor()
            sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                     DUPLICATE KEY UPDATE""".format(table=table,
                                                    keys=keys,
                                                    values=values)
            update = ','.join([
                " {key} = values({key})".format(key=key)
                for key in data_list[0]
            ])
            sql += update
            try:
                cursor.executemany(
                    sql, [tuple(data.values()) for data in data_list])
                connection.commit()
            except Exception as e:
                connection.rollback()
                print('Error: ', e)
                traceback.print_exc()
            finally:
                connection.close()

    

    
if __name__ == "__main__":
    data_spider = data_spider()
    data_spider.start_spider()
    # aa = data_spider.getTimeConvert('Fri Jan 01 09:18:07 +0800 2021')
    # print(datetime.strftime(aa, "%Y-%m-%d"))
    # test()




    
