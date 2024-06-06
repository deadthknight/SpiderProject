#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup
import re

# find_all(name, attrs, recursive, text, **kwargs)
# find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
# name参数可以查找所有名字为name的tag

# 一号方案,传字符串
# 找到所有tag名字为'a'的标签内容
# print(qytang_soup.find_all('a'))
# 找到所有tag名字为'img'的标签内容
# print(qytang_soup.find_all('img'))
# print(len(qytang_soup.find_all('img')))

# for a in qytang_soup.find_all('a'):
#     # 找到所有tag名字为'a'的标签,并且打印'a'标签内的链接'href'内容
#     print(a.get('href'))


# 二号方案,传正则表达式
# 找到所有匹配正则表达式'^a'的标签,找到a标签
# print(qytang_soup.find_all(re.compile("^a")))
# 找到所有匹配正则表达式'a|p|div'的标签,找到a,p,div标签
# print(qytang_soup.find_all(re.compile("a|p|div")))

# for a in qytang_soup.find_all(re.compile("^a")):
#     print(a.get('href'))


# # 三号方案,传列表
# print(qytang_soup.find_all(['a', 'p']))
#
# for ap in qytang_soup.find_all(['a', 'p']):
#     print(ap.attrs)



