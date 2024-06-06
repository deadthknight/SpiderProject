#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from bs4 import BeautifulSoup
import requests
from part1_restapi.restapi_5_spider.spider_1_bs4.readheader import readheaders


client = requests.session()
# 获取京东搜索iwatch8页面
url = 'https://search.jd.com/Search?keyword=watch9'

# 使用自定义头部信息,通过认证!然后获取天猫搜索iwatch4页面
taobao_home = client.get(url, headers=readheaders('http_header.txt'))

# lxml HTML 解析器
qytang_soup = BeautifulSoup(taobao_home.text, 'lxml')

# 格式化打印BeautifulSoup对象
# print(qytang_soup.prettify())



