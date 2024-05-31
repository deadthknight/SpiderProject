#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import re
import requests
from readheader import readheaders
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/chart'

headers = readheaders('./header.txt')

# print(headers)

response =requests.get(url, headers=headers)

main_page = BeautifulSoup(response.text,'lxml')

# print(main_page)

if __name__ == "__main__":
    pass
