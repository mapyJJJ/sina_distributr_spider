# Sina分布式爬虫

![](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558430618&di=312727c7a58d5fb6beff4025cdcc4d62&imgtype=jpg&er=1&src=http%3A%2F%2Fwww.xz7.com%2Fup%2F2017-8%2F20178417457.jpg)

#### 框架说明：

1，**master-spider** -----主机-调度器 （ 负责链接的获取，存入redis数据库 ）

​      该爬虫主要获取 某一用户 所发微博下的 所有 评论者 的 基本资料

​      直接运行Master_spider.py 即可启动主机程序

​     `python Master_spider.py`

​      **注意：**

​		（1）你必须设置好redis服务器（一般开在本地服务，若要远程连接redis，请设置密码）

​                        默认的 **db.py** 没有设置密码参数，如果需要密码连接，请在 redis.Redis() 中设置密码参数

```python
class RedisClient(object):
    def __init__(self,REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_DB,REDIS_DOMAIN,REDIS_NAME):
        self._db=redis.Redis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD,db=REDIS_DB)
        self.domain=REDIS_DOMAIN
        self.name=REDIS_NAME
```

​                         并且在 config.py 中设置密码字段

​                         `REDIS_PASSWORD = 'xxx'`

​		（2）请求登陆必须要使用Cookie，否则无法获取内容

​			这里的 get_cookies.py 是从cookies池接口获取cookie

​                        关于登陆拿cookie在下面介绍

​		（3）关于守护进程

 		        服务器性能不高的情况下，持续的爬虫动作会占用较多内存，linux下会将其自动kill

​                        为了防止进程中断，可以自行编写 shell 守护脚本  daemon.sh

2，**ycysl**  -----从机--负责下载内容

​		爬虫从机的主要工作 是从 redis 链接库中获取链接，进行下载请求操作

​                主机爬虫也就是通过redis实现间接控制从机爬虫，当redis里面的队列链接为空时，从机爬虫处于等待状态，

​		一般所得到的数据类型都是以非关系型的键值对储存，一般使用MongoDB更加高效稳定

​                这里的从机爬虫使用scrapy框架，可以一次获取多个链接，进行高速爬取

​                **pipelines** 中自定义了两个中间件 **PymongoSavePipeline** **DuplicatesPipeline**

​                一个用于处理MongoDB的数据存储：

```python
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
```

​		另一个用于去重操作：（根据item的name字段 排除以经爬取过的用户）

```python
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
```

​		**Middlewares** 中定义了一个用于添加cookie的中间件，为所有的请求添加随机cookie

```python
class CookiesMiddleware(object):
    '''cookies'''
    def process_request(self,request,spider):
        cookie=Cookies_Pool().parse_cookies()
        request.cookies=cookie
```

​		同时你还需安装MongoDB数据库



3，**weiboCookies**  --sina 自动化模拟登陆获取cookie

​		使用及说明可参考 [Sina 模拟登陆框架项目](<https://github.com/mapyJJJ/SinaVlogin>)

​                这是一个基于selenium+Flask+redis的项目 可以在Windows和Linux平台运行，以api接口的方式提供cookie串
