import requests
from lxml import etree
from selenium import webdriver
import time

cookies = {'_T_WM': '8add6a408e32362ac458ff67beee2481', 'SCF': 'AgaPJhytVyEKPK7uxhCn0jtyOLHR1F3hGJblXo3CGcSPyfxTqObdxbWHrnnDP-PL1lSCkZSuHjkCOALRBKpaxx4.', 'SUB': '_2A25xh-aiDeRhGeBJ7FEZ-CnPyjSIHXVSi4rqrDV6PUJbktAKLULMkW1NRix7k5c0aeABlaDXfR3Qlr1mI1MBwCxm', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWTcgIib-ASqbcyWePui-Zd5JpX5KzhUgL.FoqNS0eR1hM0eKn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcS0M01hnNe02R', 'SUHB': '0rrrFW-ZUD09f5'}
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

req=requests.get('https://weibo.cn/u/5296658630',cookies=cookies,headers=headers)
html=etree.HTML(req.content)
text=html.xpath('//div[@class="ut"]/span/a[contains(text(), "加关注")]/@href')

driver=webdriver.Chrome()
driver.add_cookie(cookie_dict=cookies)
driver.get('https://weibo.cn/u/5296658630/')
time.sleep(5)
driver.find_element_by_xpath('//div[@class="ut"]/span/a[contains(text(), "加关注")]').click()
driver.close()
