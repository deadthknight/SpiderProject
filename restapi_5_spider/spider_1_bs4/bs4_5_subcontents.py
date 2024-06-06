#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup
import bs4
import re

# 访问直接子节点
# 找到页面里边的产品清单
# print(qytang_soup.find('ul', class_="gl-warp clearfix"))

# 你会发现'\n'(换行)会出现在直接子节点里边
# print(qytang_soup.find('ul', class_="gl-warp clearfix").contents)

# 由于'\n'(换行)会出现在直接子节点里边!所以要排除错误可能
for item_card in qytang_soup.find('ul', class_="gl-warp clearfix").contents:
    if item_card.name == 'li':
        # 找到产品的文本介绍
        print(item_card.find('div', class_="p-name p-name-type-2").find('em').text)
        # # 找到产品的价格
        print(item_card.find('div', class_="p-price").find('i').text)
        # # 找大图
        print(item_card.find('div', class_="p-img").find('a').find('img').get('data-lazy-img'))
