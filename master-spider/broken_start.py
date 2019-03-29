from Master_spider import MasterSpider
from config import *
'''
当脚本被意外kill后，守护进程优先启动该脚本，在断点文章处重新唤起程序
读取current_url.txt(第一行：当前的微博主页面链接，第二行:当前的微博文章评论号)
'''
if __name__ == '__main__':
    with open('current_url.txt','r') as f:
        save_urls=f.readlines()
    app=MasterSpider(start_url=START_URL)
    app.broken_start(start_url=save_urls[0],passage_url=save_urls[1])



