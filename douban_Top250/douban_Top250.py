#!/usr/bin/python3
#
#  爬取Top250 存储到Mongodb中
#
import urllib.request
import pymongo
from lxml import etree

url='https://movie.douban.com/top250?start=0&filter='
headers={'User-Agent':'Mozilla/4.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
data={}

def save_MongoDB(data):
    top_250.insert_one(dict(data))

def get_info(html):
    page=etree.HTML(html)
    try:
        next_url = "https://movie.douban.com/top250" + \
               page.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href')[0]
        print(next_url)
    except:
        pass
    try:
        for number in range(1,26):
            data['title']=page.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(number)+']/div/div[2]/div[1]/a/span[1]/text()')[0]
            data['details']="".join(page.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(number)+']/div/div[2]/div[2]/p[1]/text()')[0].split())
            data['point']=page.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(number)+']/div/div[2]/div[2]/div/span[2]/text()')[0]
            data['comment']=page.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(number)+']/div/div[2]/div[2]/div/span[4]/text()')[0]
            data['quote']=page.xpath('//*[@id="content"]/div/div[1]/ol/li['+str(number)+']/div/div[2]/div[2]/p[2]/span/text()')[0]
            save_MongoDB(data)
        return parse(next_url)
    except Exception as msg:
        print(msg)

def parse(url):
    req=urllib.request.Request(url=url,headers=headers)
    page=urllib.request.urlopen(req)
    html=page.read().decode('utf-8')
    return get_info(html)

if __name__ == '__main__':
    client=pymongo.MongoClient('localhost',27017)
    db=client['douban']
    top_250=db['Moive_Top250']
    parse(url)
