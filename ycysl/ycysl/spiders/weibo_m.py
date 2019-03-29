# -*- coding: utf-8 -*-
import scrapy
from ycysl.items import YcyslItem
from scrapy_redis.spiders import RedisSpider
import json

class WeiboMSpider(RedisSpider):
    name = 'weibo_m'
    allowed_domains = ['weibo.cn']
    redis_key = 'weibo:lfid'

    def parse(self, response):
        content=json.loads(response.text)
        item = YcyslItem()
        blank_node = []
        field={
            '昵称':'name','认证':'m_auth','简介':'introduction','等级':'Member_Level','注册时间':'m_time','阳光信用':'m_credit','性别':'sex','生日':'birthday','情感状况':'affective','所在地':'m_location','家乡':'m_hometown','大学':'m_school','公司':'m_company'
        }
        for num in range(0,2):
            for i in content['data']['cards'][int(num)]['card_group']:
                if 'item_name' in i.keys():
                    if i['item_name'] in field.keys():
                        blank_node.append(i['item_name'])
                        item[field[i['item_name']]]=i['item_content']
        blanks=[x for x in field.keys() if x not in blank_node]
        item['Uid']=content['data']['cardlistInfo']['containerid'].replace("_-_INFO","").replace("230283","")
        #排除其它自定义字段的影响
        try:
            for blank in blanks:
                item[field[blank]]=''
        except:
            pass
        yield item
