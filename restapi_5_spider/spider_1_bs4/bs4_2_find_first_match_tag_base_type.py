#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup
import bs4
print(qytang_soup.title)
print("-"*100)
print(qytang_soup.head)
print("-"*100)
# 这种方式,只找到第一个符合要求的标签a
print(qytang_soup.a)
print("-"*100)
# 这种方式,只找到第一个符合要求的标签p
print(qytang_soup.p)
print("-"*100)
# 类型为<class 'bs4.element.Tag'>
print(type(qytang_soup.p))
if type(qytang_soup.p) is bs4.element.Tag:
    print('match!')
