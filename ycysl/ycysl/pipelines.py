# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class PymongoSavePipeline(object):
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
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]
    def process_item(self,item,spider):
        if spider.name=='weibo':
            self.db['user_list'].insert(dict(item))
            return item
        elif spider.name=='weibo_passage':
            self.db['user_conn'].insert(dict(item))
            return item
        elif spider.name=='weibo_m':
            self.db['user_mobile'].insert(dict(item))
            return item
    def close_spider(self,spider):
        self.client.close()

class YcyslPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    """
    去重
    """
    def __init__(self):
        self.weibo_set = set()
        self.weibo_passage_set = set()
        self.weibo_m = set()

    def process_item(self, item, spider):
        name = item['name']
        if spider.name=='weibo':
            if name in self.weibo_set:
                raise DropItem("error::%s已经存在" % name)
            else:
                self.weibo_set.add(name)
                return item
        elif spider.name=='weibo_passage':
            if name in self.weibo_passage_set:
                raise DropItem("error::%s已经存在" % name)
            else:
                self.weibo_passage_set.add(name)
                return item
        elif spider.name=='weibo_m':
            if name in self.weibo_m:
                raise DropItem("error::%s已经存在" % name)
            else:
                self.weibo_m.add(name)
                return item
