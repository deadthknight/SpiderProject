#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup


print(qytang_soup.find_all('a', limit=2))
