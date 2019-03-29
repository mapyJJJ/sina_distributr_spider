import redis
from config import *

class RedisClient(object):
    def __init__(self,REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_DOMAIN,REDIS_NAME):
        self._db=redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB)
        self.domain=REDIS_DOMAIN
        self.name=REDIS_NAME

    def _key(self):
        '''
        构造key
        :return:
        '''
        return "{domain}:{name}".format(domain=self.domain, name=self.name)

    def get(self):
        '''
        提供访问功能
        :param key:
        :return:
        '''
        try:
            self._db.get(self._key()).decode('utf-8')
        except:
            print('访问失败！')

    def lpush(self,value):
        '''
        :param key:  用户昵称（新浪微博用户昵称不能相同）
        :param value:  用户主页链接
        :return:
        '''
        try:
            self._db.lpush(self._key(),value)
        except:
            print('数据保存错误！')