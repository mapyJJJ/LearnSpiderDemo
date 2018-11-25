import pymongo
'''
    读取文章
'''
client=pymongo.MongoClient('localhost',27017)
db=client['wenxue']

account=db.get_collection("article")

for i in (account.find())[:2]:
    print('                   《'+i['title']+'》                          ')
    print(i['article'])
    print("==========================================================")

