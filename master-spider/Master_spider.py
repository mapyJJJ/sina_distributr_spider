import time
import requests
from bs4 import BeautifulSoup
from config import *
from get_cookies import Cookies_Pool
from db import RedisClient
from lxml import etree
from fake_useragent import UserAgent
"""
    1，屏蔽print输出，减小内存占用
    2，使用set去重时从全局去重到单页面去重
    3，使用nohup命令实现后台运行
    4，保留系统错误日志文件，方便问题查找
    5，创建守护进程 daemon_py.sh
    6，crontab定时管理
"""

class MasterSpider:
    def __init__(self,start_url):
        self.start_url=start_url
        #数据量过大时会发生内存溢出
        #self.fi=set()
        self.headers={"User-Agent":"Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        '''
        初始化连接redis
        '''
        self.start_url=START_URL
        self.db=RedisClient(REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_DOMAIN,REDIS_NAME)
        self.db1=RedisClient(REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_DOMAIN="weibo",REDIS_NAME="HomeUrl")
        self.db2=RedisClient(REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_DOMAIN="weibo",REDIS_NAME="lfid")

    def new_cookies(self):
        cookies = Cookies_Pool().parse_cookies()
        return cookies

    def parse(self,pass_url):
        #解析当前微博下的所有评论用户
        first_req=requests.get(pass_url+str(1),cookies=self.new_cookies()).content
        if 'not exist' in str(first_req):
            return None
        html = etree.HTML(first_req)
        #获取中断的页面
        try:
            with open('page_num.txt','r') as f:
                broken_page_num=int(f.readlines()[0])+1
        except:
            broken_page_num=1
        #评论总页数
        try:
            page_num = (html.xpath('//*[@id="pagelist"]/form/div/text()')[1].split('/')[1])[:-1]
        except:
            #print('[-----]页面请求错误')
            return self.parse(pass_url=pass_url)
        for page in range(broken_page_num,int(page_num)+1):
            print(page)
            if page % 5 == 0:
                with open('page_num.txt','w') as f:
                    f.write(str(page))
            fi=set()
            #保存当前运行状态
            cookies=self.new_cookies()
            #print('[++++++++]当前cookies:',str(cookies))
            try:
                req=requests.get(pass_url+str(page),cookies=cookies,headers={"User-Agent":UserAgent().random}).content
                html=etree.HTML(req)
                fans = html.xpath('//div[@class="c"]/a[contains(@href,"/u/")]/@href')
                fans_name=html.xpath('//div[@class="c"]/a[contains(@href,"/u/")]/text()')
            except:
                while True:
                    #print('[!!!!!]出现错误，未获取到内容:')
                    time.sleep(5)
                    try:
                        req = requests.get(pass_url + str(page),headers={"User-Agent":UserAgent().random},cookies=cookies).content
                        html = etree.HTML(req)
                        fans = html.xpath('//div[@class="c"]/a[contains(@href,"/u/")]/@href')
                        fans_name = html.xpath('//div[@class="c"]/a[contains(@href,"/u/")]/text()')
                        break
                    except:
                        pass

            for i,j in enumerate(fans):
                #防止底部返回链接的干扰
                if '5644764907' in j:
                    continue
                fans_url='https://weibo.cn/'+j.split('/u/')[1]+'/info'
                fans_weibo='https://weibo.cn'+j
                m_url="https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=230283{}".format(j.split('/u/')[1],j.split('/u/')[1])
                name=fans_name[i]
                if name in fi:
                    pass
                else:
                    fi.add(name)
                    self.db.lpush(fans_url)
                    self.db1.lpush(fans_weibo)
                    self.db2.lpush(m_url)
                    print('[+++][+++][+++]',name)
                #在应对限制ip的反爬措施中，效率最高的等待时间
                time.sleep(0.35)
        #爬完该篇微博的所有评论后
        time.sleep(1)
        with open('page_num.txt','w') as f:
            f.write('0')


    def open_url(self):
        #获取微博主页页码
        req = requests.get(url=self.start_url, cookies=self.new_cookies())
        html = etree.HTML(req.content)
        page_num = (html.xpath('//*[@id="pagelist"]/form/div/text()')[1].split('/')[1])[:-1]
        #print('[+]微博主页数:',str(page_num))
        for page in range(1,int(int(page_num)/2+1)):
            page_url=self.start_url.split('=')[0]+'='+str(page)
            #print('[+][+]当前所在主页链接：',page_url
            req = requests.get(url=page_url, cookies=self.new_cookies())
            soup = BeautifulSoup(req.content, 'lxml')
            #获取到当前微博页面上的所有文章链接
            passages = soup.find_all(attrs={"class": "cc"})
            #print('[+][+][+]该页面的微博文章数：',str(len(passages)))
            #循环每一篇微博评论区地址
            for passage in passages:
                with open(r'current_url.txt', 'w') as f:
                    f.write(page_url+'\n'+passage.get('href'))
                pass_url=passage.get('href').replace('#cmtfrm', '&page=')
                #print('[+][+][+][+]当前文章的第一页评论页面模板',pass_url)
                self.parse(pass_url)
            time.sleep(120)

    def broken_start(self,start_url,passage_url):
        #print('passage_url',passage_url)
        # 获取微博主页页码
        req = requests.get(url=self.start_url, cookies=self.new_cookies())
        html = etree.HTML(req.content)
        page_num = (html.xpath('//*[@id="pagelist"]/form/div/text()')[1].split('/')[1])[:-1]
        # 从中断处开始
        for page in range(int(start_url.split('=')[1]),int(int(page_num)/2+1)):
            page_url = self.start_url.split('=')[0] + '=' + str(page)
            # print('[+][+]当前所在主页链接：',page_url)
            req = requests.get(url=page_url, cookies=self.new_cookies())
            soup = BeautifulSoup(req.content, 'lxml')
            # 获取到当前微博页面上的所有文章链接
            passages = soup.find_all(attrs={"class": "cc"})
            # print('[+][+][+]该页面的微博文章数：',str(len(passages)))
            # 循环每一篇微博评论区
            try:
                passage_list=[x.get('href') for x in passages]
                index=passage_list.index(passage_url.replace('\n',''))
                print('index',str(index))
            except Exception as msg:
                print(msg)
                index=0

            for passage in passages[index:]:
                with open(r'current_url.txt', 'w') as f:
                    f.write(page_url+"\n"+passage.get('href'))
                pass_url = passage.get('href').replace('#cmtfrm', '&page=')
                # print('[+][+][+][+]当前文章的第一页评论页面模板',pass_urli)
                self.parse(pass_url)
            time.sleep(120)


if __name__ == '__main__':
    app=MasterSpider(start_url=START_URL)
    app.open_url()
