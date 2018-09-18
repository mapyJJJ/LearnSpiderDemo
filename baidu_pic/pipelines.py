# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
image_count=0
class BaiduPicPipeline(object):
    def process_item(self, item, spider):
        global image_count
        image_count+=1
        try:
            urllib.request.urlretrieve(item['pic_url'],"/root/桌面/{}/{}.jpg".format(item['name'],str(image_count)))
        except:
            pass
