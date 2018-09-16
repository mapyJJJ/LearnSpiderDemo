# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=Field()
    name=Field()
    is_followed=Field()
    avatar_url_template=Field()
    user_type=Field()
    answer_count=Field()
    badge=Field()
    is_following=Field()
    url=Field()
    url_token=Field()
    allow_message=Field()
    articles_count=Field()
    is_blocking=Field()
    headline=Field()
    gender=Field()
    is_advertiser=Field()
    avatar_url=Field()
    is_org=Field()
    follower_count=Field()
    employments=Field()
    type=Field()
