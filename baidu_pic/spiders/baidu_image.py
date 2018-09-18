# -*- coding: utf-8 -*-
import json
import os
from baidu_pic.items import BaiduPicItem
import scrapy

#  说明:1,scrapy会因为robot.txt 出现Forbidden,(纯属智障,默认遵守robot规则),在setting.py 找到 ROBOTTXT_OBEY改为False
#       2,回调parse函数时 加上 dont_filter=True
page = 30
class BaiduImageSpider(scrapy.Spider):
    name = 'baidu_image'
    allowed_domains = ['http://image.baidu.com']
    start_url=['http://image.baidu.com']
    keywords = input("enter keywords:")
    item = BaiduPicItem()
    try:
        os.mkdir('/root/桌面/{}/'.format(keywords))
    except:
        pass

    def start_requests(self):
        self.item['name']=self.keywords
        yield scrapy.Request(url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&pn=30&rn=30'.format(self.keywords,self.keywords),callback=self.parse)
    def parse(self, response):
        global page
        page+=30
        next_url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&pn={}&rn=30'.format(self.keywords,self.keywords,str(page))
        try:
            json_data = json.loads(response.text)
            for i in json_data['data']:
                self.item['pic_url']=i['middleURL']
                yield self.item
        except:
            pass
        yield scrapy.Request(url=next_url, callback=self.parse,dont_filter=True)