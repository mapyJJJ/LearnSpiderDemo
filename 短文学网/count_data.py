import pymongo
import time

def data_sum():
    client=pymongo.MongoClient('localhost',27017)
    db=client['wenxue']
    passage=db['passage']
    article=db['article']
    while True:
        print('--------------------------------')
        print('句子采集数量'+str(passage.count()))
        print('文章采集数量'+str(article.count()))
        time.sleep(2)

if __name__ == '__main__':
    data_sum()

