#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

from part1_restapi.restapi_5_spider.spider_2_practice_2_qqketang.spider_2_qqketang_page import getpage
from part1_restapi.restapi_5_spider.spider_2_practice_2_qqketang.spider_1_qqketang_getlastpage import getlastpage


# 汇总代码, 给一个方向的名称, 就能逐页获取所有课程内容
def getall(direction):
    # 想获取这个方向的最大页码号
    max_page = getlastpage(direction)
    all_coures = []
    for page in range(max_page):
        # 爬取每一页的内容,并且扩展(extend)到列表all_coures
        all_coures.extend(getpage(direction, page+1))
    return all_coures


if __name__ == '__main__':
    print(getall("ccie"))

