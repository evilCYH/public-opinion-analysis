from snownlp import SnowNLP
from database_util import database_util
# 情感分析
class NLPUTIL:
    def __init__(self):
        self.database = database_util()

    def get_nlp_result(self,text):
        try:
            sq = SnowNLP(text)
            score = sq.sentiments
            print(score)
            if(score<=0.3):
                return '消极'
            elif(score>=0.7):
                return '积极'
            else:
                return '中立'
        except Exception as e:
            print(e)
            return '中立'


    def build_nlp_result(self):
        data  = self.database.query_nlp_data()
        for item in data:
            flag = self.database.check_nlp_detail(item['source'],item['id'])
            if(flag):
                continue
            if(item['content'] == None or item['content'] == ''):
                continue
            item['nlp'] = self.get_nlp_result(item['content'])
            self.database.save_nlp_result(item)


if __name__ == "__main__":
    nlp = NLPUTIL()
    nlp.build_nlp_result()