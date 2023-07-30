from snownlp import SnowNLP


def get_nlp_result(text):
    sq = SnowNLP(text)
    score = sq.sentiments
    print(score)
    if(score<=0.3):
        return '消极'
    elif(score>='0.7'):
        return '积极'
    else:
        return '中立'