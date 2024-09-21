# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
import chardet

url = 'https://dygod.org/index.htm'
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
response = requests.get(url=url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']
tree = etree.HTML(response.text)
tr_list = tree.xpath('(//div[@class="bd3rl"])[1]/div[2]//div[2]//tr[position()>1 and position()<=11]')
# print(len(tr_list))
name_list = []
download_list = []
movies = []
for tr in tr_list:
    name = tr.xpath('./td/a[2]/text()')[0]
    movie_url = 'https://dygod.org'+ tr.xpath('./td/a[2]/@href')[0]
    # print(name,movie_url)
    name_list.append(name)
    response = requests.get(url=movie_url, headers=headers)
    response.encoding = chardet.detect(response.content)['encoding']
    tree = etree.HTML(response.text)
    download_url = tree.xpath('//*[@id="Zoom"]//a/@href')[0]
    dic = {'电影名称':name,
           '链接地址':movie_url,
           '下载链接':download_url}
    movies.append(dic)
for movie in movies:
    print(f"{movie['电影名称']}")