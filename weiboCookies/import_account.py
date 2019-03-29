# -*- coding: utf-8 -*-
from db import AccountRedisClient
from error import *
import re

c = AccountRedisClient(name='weibo',db=3)
path = 'account.txt'

def set(username,password):
    try:
        c.set(username,password)
        print('账号：',username,'密码：',password)
        print('录入成功')
    except:
        print('录入失败')

def scan():
    with open(path,'r') as c:
        L = c.readlines()
    for item in L:
        username=item.split('----')[0]
        password=item.split('----')[1]
        set(username,password)
    print('='* 10+'录入%s条' % len(L) + '='* 10)

if __name__ == '__main__':
    scan()
