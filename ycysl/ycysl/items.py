# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YcyslItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()  #昵称
    sex=scrapy.Field()   #性别
    area=scrapy.Field()  #地区
    birthday=scrapy.Field()  #生日
    introduction=scrapy.Field()  #简介
    affective=scrapy.Field()  #情感状况
    Member_Level=scrapy.Field()  #会员等级
    tags=scrapy.Field()  #标签
    school_company=scrapy.Field()  #学习工作
    weibo_content=scrapy.Field()  #近期微博内容
    Uid=scrapy.Field()  #uid标识
    #手机版字段
    m_auth=scrapy.Field()  #认证


    m_time=scrapy.Field()  #注册时间
    m_credit=scrapy.Field() #阳光信用



    m_location=scrapy.Field()  #所在地
    m_hometown=scrapy.Field()  #家乡
    m_school=scrapy.Field()
    m_company=scrapy.Field()
    pass
