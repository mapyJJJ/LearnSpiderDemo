# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

class YouzixyPipeline(object):
    def process_item(self, item, spider):
        return item

class PricePipeline(object):
    def process_item(self,item,spider):
        if item['price']:
            item['price']+="元"
            return item
        else:
            return DropItem('Miss Text!!!')

class SaveMongodbPipline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.clien=pymongo.MongoClient(self.mongo_url,27017)
        self.db=self.clien[self.mongo_db]
    def process_item(self,item,spider):
        self.db['sale'].insert_one(dict(item))
        return item
    def close_spider(self,spider):
        self.clien.close()
