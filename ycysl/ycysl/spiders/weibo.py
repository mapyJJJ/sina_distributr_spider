# -*- coding: utf-8 -*-
import scrapy
from ycysl.items import YcyslItem
from scrapy_redis.spiders import RedisSpider

#基本资料
class WeiboSpider(RedisSpider):
    name = 'weibo'
    allowed_domains=['weibo.cn']
    redis_key = 'weibo:MasterUrl'

    def parse(self, response):
        item=YcyslItem()
        current_url=response.url
        field={'昵称':'name','性别':'sex','地区':'area','生日':'birthday','简介':'introduction','情感状况':'affective','会员等级':'Member_Level','标签':'tags','·':'school_company'}
        post_nodes = response.xpath('//div[@class="c"]/text()').extract()
        # uid=response.xpath('//div[@class="c"]/a[contains(@href,"uid=")]/@href').extract_first().split('uid=')[1]
        uid=current_url.split('/')[3]
        blank_node=[]
        s_c=[]
        for con in post_nodes:
            for node in field.keys():
                if node in con:
                    blank_node.append(node)
                    if '·' in con:
                        s_c.append(con[1:])
                        item[field[node]]=";".join(s_c)
                    else:
                        try:
                            item[field[node]]=con.split(':')[1].replace("\xa0","")
                        except:
                            item[field[node]]=con.split('：')[1].replace("\xa0","")
        item['Uid']=str(uid)
        blanks=[x for x in field.keys() if x not in blank_node]
        for blank in blanks:
            item[field[blank]]=''
        yield item