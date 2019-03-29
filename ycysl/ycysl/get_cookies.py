import requests
class Cookies_Pool(object):
    def __init__(self):
        self.api='http://47.94.86.107:5000/weibo/random'
    def get_cookies(self):
        req=requests.get(self.api).text
        return req
    def parse_cookies(self):
        cook={}
        req=self.get_cookies()
        for i in str(req).split('; '):
            j = i.split('=')
            cook[j[0]] = j[1]
        return cook
