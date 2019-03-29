# -*- coding: utf-8 -*-
import scrapy
from ycysl.items import YcyslItem
from scrapy_redis.spiders import RedisSpider

class WeiboPassageSpider(RedisSpider):
    name = 'weibo_passage'
    allowed_domains = ['weibo.cn']
    redis_key='weibo:HomeUrl'

    def parse(self, response):
        current_url=response.url
        conn = ";".join(response.xpath('//div[@class="c"]/div/span[@class="ctt"]/text()').extract())
        name=response.xpath('//div[@class="ut"]/span[@class="ctt"]/text()').extract_first()
        item=YcyslItem()
        item['weibo_content']=conn
        item['name']=name.split("\xa0")[0]
        item['Uid']=str(current_url).split('/u/')[1].split('?')[0]
        yield item
