from database_util import database_util
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import PIL .Image as image
import numpy as np
import jieba
# 生成词云
class GenerWord:
    def __init__(self):
        self.database = database_util()
        self.stopwords = set()
        with open("../app/static/stopwords.txt", "r", encoding="utf-8") as file:
            for line in file:
                self.stopwords.add(line.strip())
    
    def generNewsWord(self):
        # 查询数据
        content = self.database.query_last_week_news()
        processed_content = self.removeUnuseWord(content)
        self.get_image(processed_content,"../app/static/images/school_news.png")

    def removeUnuseWord(self,content):
        # 去除无意义词汇
        words = jieba.cut(content)
        processed_words = [word for word in words if word not in self.stopwords and not word.encode('utf-8').isalpha()]
        processed_content = " ".join(processed_words)
        # processed_content = content.strip().replace('学校', '').replace('工作', '')
        return processed_content
        # return content.replace('学校','').replace('工作','')

    def generWeiboWord(self):
        content = self.database.query_last_week_weibo()
        print(content)
        self.get_image(self.removeUnuseWord(content),"../app/static/images/week.png")

    def generWeiboTopicWord(self):
        content = self.database.query_last_week_weibo_topic()
        self.get_image(self.removeUnuseWord(content),"../app/static/images/weibo_topic.png")

    def trans_CN(self,text):
        word_list = jieba.cut(text)
        # 分词后在单独个体之间加上空格
        result = " ".join(word for word in word_list if word.strip() not in ['', ' ', '\n'] and not word.encode('utf-8').isalpha())
        return result

    def get_image(self,data,savePath):
        text = self.trans_CN(data)
        words = text.split()  # 分词后得到单词列表
        word_freq = Counter(words)  # 计算每个单词的频率
        wordcloud = WordCloud(
            background_color="white",
            font_path = "C:\\Windows\\Fonts\\msyh.ttc",
            width=800,
            height=400
        ).generate_from_frequencies(word_freq)
        # image_produce = wordcloud.to_image()
        # image_produce.show()
        print(savePath)
        plt.figure(figsize=(8, 4),dpi=330)  # 设置画布大小
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")  # 不显示坐标轴
        plt.tight_layout(pad=0)  # 调整布局，防止词云被裁剪

        # 可选：添加自定义样式等
        # plt.title("My Custom Word Cloud")
        # plt.colorbar()

        plt.savefig(savePath)  # 保存图像
        # plt.show()  # 显示图像（如果需要的话）
        # wordcloud.to_file(savePath)

    def build_word(self):
        self.generNewsWord()
        self.generWeiboWord()
        self.generWeiboTopicWord()

if __name__ == "__main__":
    gener = GenerWord()
    gener.build_word()

