from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db import CookiesRedisClient,AccountRedisClient
from config import *

class CookiesGenerator(object):
    def __init__(self,name='weibo',db=REDIS_DB):
        '''
        :param name:
        :param db:
        '''
        self.name=name
        self.db=db
        print(self.name,self.db)
        self.account_db=AccountRedisClient(name=self.name,db=self.db)
        self.cookies_db=CookiesRedisClient(name=self.name,db=db)

    def get_cookies(self,username,password):
        self.email=username
        self.passwd=password.replace("b'","").replace(r"\n'","")
        print(self.passwd)
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.email)
        password.send_keys(self.passwd)
        submit.click()
        WebDriverWait(self.browser, 30).until(
            EC.title_is('我的首页')
        )
        cookies = self.browser.get_cookies()
        print(cookies)
        cookie = [item["name"] + "=" + item["value"] for item in cookies]
        cookie_str = '; '.join('%s' % item for item in cookie)
        self.browser.quit()
        return self.email,cookie_str

    def run(self):
        '''
        运行所有账号
        :return:
        '''
        accounts=self.account_db.all()
        accounts_list=list(accounts)
        cookies=self.cookies_db.all()
        valid_users = [cookie['username'] for cookie in cookies]
        if len(accounts_list):
            availble_account = []
            for account in accounts_list:
                if not account['username'] in valid_users:
                    availble_account.append(account)
        print('Getting', len(availble_account), ' accounts from Redis')
        for account in availble_account:
            print('Getting Cookies of', self.name, account['username'], account['password'])
            username,cookie_str=self.get_cookies(str(account['username']),str(account['password']))
            if cookie_str:
                self.cookies_db.set(username,cookie_str)



if __name__ == '__main__':
    app=CookiesGenerator(name='weibo',db=3)
    app.run()
