# -*- coding: utf-8 -*-
import json

import scrapy

from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user='excited-vczh'

#用户详情
    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
#关注列表
    follow_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follow_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
#粉丝列表
    followers_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield scrapy.Request(url=self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield scrapy.Request(url=self.follow_url.format(user=self.start_user,include=self.follow_query,offset=0,limit=20),callback=self.parse_follows)
        yield scrapy.Request(url=self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)

    def parse_user(self, response):   #解析用户信息
        result=json.loads(response.text)
        item=UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item

        yield scrapy.Request(url=self.follow_url.format(user=self.start_user,include=self.follow_query,offset=0,limit=20),callback=self.parse_follows)
        yield scrapy.Request(url=self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)


    def parse_followers(self,response): #获取用户链接名 判断页面结尾
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)
            if 'paging' in results.keys() and results.get('paging').get('is_end') == False:  #当判断不是最后一页时
                next_page=results.get('paging').get('next')
                yield scrapy.Request(url=next_page,callback=self.parse_followers)

    def parse_follows(self,response): #获取用户链接名 判断页面结尾
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)
            if 'paging' in results.keys() and results.get('paging').get('is_end') == False:  #当判断不是最后一页时
                next_page=results.get('paging').get('next')
                yield scrapy.Request(url=next_page,callback=self.parse_follows)
