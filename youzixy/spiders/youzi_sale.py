# -*- coding: utf-8 -*-
import re

import scrapy
from youzixy.items import YouzixyItem

class YouziSaleSpider(scrapy.Spider):
    name = 'youzi_sale'
    allowed_domains = ['http://www.youzixy.com']
    start_urls = ['http://www.youzixy.com/sale/goods/page/1']
    page_number=0
    def parse(self, response):
        global page_number
        self.page_number+=1
        item=YouzixyItem()
        title=response.css('.class-item-bg .title::text').extract()
        price=response.css('.price span::text').extract()
        school=response.css('.some .school::text').extract()
        pic_url=response.css('.class-img img::attr(src)').extract()

        next_url='http://www.youzixy.com/sale/goods/page/{}'.format(str(self.page_number))
        if len(title) == len(price) == len(school) == len(pic_url):
            for i in range(0,len(title)):
                item['title']=("".join(title[i]).split())[0]
                item['price']=price[i]
                item['school']=school[i]
                item['pic_url']=pic_url[i]
                yield item
        if "下一页" in response.text:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
        else:
            pass

