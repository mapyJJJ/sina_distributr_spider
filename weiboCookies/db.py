import redis
from config import *
from error import *
import random

#初始化连接数据库
class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,db=0):
        '''
        :param host:
        :param port:
        :param db:
        初始化redis连接
        默认不设置密码
        '''
        self._db=redis.Redis(host=host,port=port,db=db)
        self.domain=REDIS_DOMAIN
        self.name=REDIS_NAME

    def _key(self,key):
        '''
        自定义key格式
        :param key:
        :return:
        '''
        return "{domain}:{name}:{key}".format(domain=self.domain, name=self.name, key=key)

    def keys(self):
        '''
        返回所有键名称
        :return:
        '''
        return self._db.keys('{domain}:{name}:*'.format(domain=self.domain,name=self.name))

    def clear_db(self):
        '''
        清空数据库
        :return:
        '''
        self._db.flushall()

class AccountRedisClient(RedisClient):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,domain='account',name='default',db=0):
        '''
        账号管理类
        :param host:
        :param port:
        :param domain:
        :param name:
        :param db:
        '''
        super().__init__(host,port,db)
        self.domain=domain
        self.name=name
    def set(self,key,value):
        '''
        提供账号的存储
        :param key:
        :param value:
        :return:
        '''
        try:
            self._db.set(self._key(key),value)
        except:
            raise SetAccountError

    def get(self,key):
        '''
        提供访问账号功能
        :param key:
        :return:
        '''
        try:
            self._db.get(self._key(key)).decode('utf-8')
        except:
            raise GetAccountError

    def all(self):
        '''
        返回所有账号
        :return:
        '''
        print(self.domain, self.name)
        try:
            for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain,name=self.name)):
                key_name=key.decode('utf-8').split(':')
                if len(key_name) == 3:
                    username=key_name[2]
                    yield {'username':username,'password':self._db.get(key)}
        except Exception as e:
            print(e.args)
            raise GetAllAccountError

    def delete(self,key):
        '''
        提供删除账号的功能
        :param key:
        :return:
        '''
        try:
            print('删除用户',key)
            return self._db.delete(self._key(key))
        except:
            raise DeleteAccountError

class CookiesRedisClient(RedisClient):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,domain='cookies',name='default',db=0):
        super().__init__(host,port,db)
        self.domain=domain
        self.name=name

    def set(self,key,value):
        '''
        提供cookies的存储
        :param key:
        :param value:
        :return:
        '''
        try:
            self._db.set(self._key(key),value)
        except:
            raise SetCookiesError

    def get(self, key):
        try:
            return self._db.get(self._key(key)).decode('utf-8')
        except:
            raise GetCookiesError

    def get_random(self):
        '''
        随机获取一个cookie
        :return:
        '''
        try:
            keys = self.keys()
            return self._db.get(random.choice(keys))
        except:
            raise GetRandomCookieError

    def all(self):
        '''
        获取所有账户，返回字典
        :return:
        '''
        try:
            for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name)):
                group = key.decode('utf-8').split(':')
                if len(group) == 3:
                    username = group[2]
                    yield {
                        'username': username,
                        'password': self.get(username)
                    }
        except Exception as e:
            print(e.args)
            raise GetAllCookieError

    def delete(self, key):
        try:
            print('删除Cookies：', key)
            return self._db.delete(self._key(key))
        except:
            raise DeleteAccountError

    def count(self):
        """
        获取当前Cookies数目
        :return: 数目
        """
        return len(self.keys())