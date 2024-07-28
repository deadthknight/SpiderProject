#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import requests
from readheader import readheaders
from bs4 import BeautifulSoup

headers = readheaders('../douban/header.txt')

# print(headers)
url = 'https://www.biedoul.com/t/57OX55m%2B5Zu%2B54mH.html'

response = requests.get(url=url, headers=headers).text

# print(response)

pic_soup = BeautifulSoup(response,'lxml')

# print(pic_soup)
p = []
x = pic_soup.find('div',class_='nr').find_all('dl',class_='xhlist')
for i in x:
    y = i.find_all('img')
    # print(y)
    for j in y:
        p.append(j.get('src'))
    print(p)
        # print(len(p))
    break
    # print(y.get('src'))

if __name__ == "__main__":
    pass
