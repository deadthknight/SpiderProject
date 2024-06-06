#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup
import re
# 通过 text 参数可以搜搜文档中的字符串内容.与 name 参数的可选值一样, text 参数接受 字符串 , 正则表达式 , 列表, True
print(qytang_soup.find_all(text="京东"))
print(qytang_soup.find_all(text=re.compile("京东")))
print(qytang_soup.find_all('a', text=re.compile("京东")))
