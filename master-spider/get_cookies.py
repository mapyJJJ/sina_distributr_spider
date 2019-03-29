import requests
from config import *

class Cookies_Pool(object):
    def __init__(self):
        self.api=COOKIES_URL
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
