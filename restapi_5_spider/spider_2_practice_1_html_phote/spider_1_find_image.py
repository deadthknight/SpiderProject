#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

import requests
from bs4 import BeautifulSoup
# url parse的参考文章
# https://docs.python.org/3/library/urllib.parse.html
from urllib.parse import urlparse


def find_images(url):
    page = requests.get(url)
    urlparse_result = urlparse(url)

    # 找到协议https
    # url_scheme: https
    url_scheme = urlparse_result.scheme

    # 找到host
    # url_netlocation: flask.netdevops.com
    url_netlocation = urlparse_result.netloc

    # 把页面内容转换到bs
    page_soup = BeautifulSoup(page.text, 'lxml')

    img_url_list = []

    # 搜索在<div class="container">内的图片
    for img in page_soup.find('div', class_='container').contents:
        if img.name == 'img':
            # 拼接完整路径
            img_url_list.append(f"{url_scheme}://{url_netlocation}{img.get('src')}")

    return img_url_list


if __name__ == "__main__":
    from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.core_info import web_page
    print(find_images(web_page))
