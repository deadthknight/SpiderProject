#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import requests
import bs4
from readheader import readheaders

if __name__ == "__main__":
    # url = "https://www.sogou.com/web?"
    # kw = input('Please enter keywords:')
    # param = {'query': kw}
    #
    # client = requests.session()
    #
    # response = client.get(url, params=param, headers=readheaders('http_header.txt'))
    #
    # filename = kw + ".html"
    # with open (filename, 'w', encoding='utf8') as f:
    #     f.write(response.text)
    a = 1
    b = 2
    if a == b:
        print("equal")
    else:
        print('not equal')

# https://www.kfc.com.cn/kfccda/storelist/index.aspx