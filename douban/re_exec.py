# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import re
import requests
from readheader import readheaders
import chardet
from lxml import etree

def get_source_page(url):
    params = {"type": "3",
              "interval_id": "100:90",
              "action":'',
              "start": "0",
              "limit":" 20"}
    response = requests.get(url, headers=readheaders('./header.txt'), params=params, verify=False)
    # response.encoding = chardet.detect(response.content)['encoding'] #解决乱码 方案一
    # response.encoding = "UTF-8"  #方案二
    return response.text

def parse_data(source_page):
    obj = re.compile()
    return page_source




def main():
    url = 'https://movie.douban.com/top250'
    source_page = get_source_page(url)
    # page_source = parse_data(source_page)
    print(source_page)

if __name__ == '__main__':
    main()