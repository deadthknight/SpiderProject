# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import re
import requests
from readheader import readheaders
import chardet
from lxml import etree


def get_source_page(url):
    response = requests.get(url, headers=readheaders('./header.txt'))
    # response.encoding = chardet.detect(response.content)['encoding'] #解决乱码 方案一
    # response.encoding = "UTF-8"  #方案二
    return response.text


def parse_data(source_page):
    obj = re.compile(
        r'div class="item">.*?<em class="">(?P<rate>.*?)</em>.*?<div class="hd">.*?<a href="(?P<src>.*?)" class="">.*?'
        r'<span class="title">(?P<title>.*?)</span>.*?average">(?P<score>.*?)'
        r'</span>.*?<span>(?P<num>.*?)</span>', re.S)
    res = obj.finditer(source_page)
    lst = []
    for item in res:
        dic = item.groupdict()
        lst.append(dic)
    return lst


def main():
    for i in range(10):
        url = f'https://movie.douban.com/top250?start={i * 25}&filter='
        source_page = get_source_page(url)
        lst = parse_data(source_page)
        for x in lst:
            print(x)


if __name__ == '__main__':
    main()
