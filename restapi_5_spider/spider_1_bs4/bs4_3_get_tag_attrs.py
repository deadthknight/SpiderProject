#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup


# 只找到的第一个a标签,的全部内容
print(qytang_soup.a)
print("-"*100)

# a 标签的标签名字, 当然也为a了
print(qytang_soup.a.name)
print("-"*100)

# 提取a标签的全部属性值,产生为字典
# {'href': '//login.taobao.com/member/login.jhtml?f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F', 'target': '_top'}
print(qytang_soup.a.attrs)
print("-"*100)

# 提取attrs href
print(qytang_soup.a['href'])
print("-"*100)

# 提取attrs target
print(qytang_soup.a['target'])
print("-"*100)

# 提取标签a内的文本
print(qytang_soup.a.text)
