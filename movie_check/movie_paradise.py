# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
import chardet
from readheader import readheaders
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

headers = readheaders('./header_code.txt')
url = 'https://dygod.org/index.htm'
# url = 'https://dytt.dytt8.net/index.htm'

response = requests.get(url=url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']
tree = etree.HTML(response.text)
tr_list = tree.xpath('(//div[@class="bd3rl"])[1]/div[2]//div[2]//tr[position()>1 and position()<=8]')
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
    # print(tree)
    # title = tree.xpath('//title/text()')
    # print(title)
    download_url = tree.xpath('//*[@id="Zoom"]//a/@href')[0]
    # download_url = tree.xpath('//*[@id="Zoom"]/span/a/@href')[0] 网页可以找到 代码运行找不到

    dic = {'电影名称':name,
           '链接地址':movie_url,
           '下载链接':download_url}
    movies.append(dic)
pprint(movies)

    # 调用selenium 点击下载链接
    # wd = webdriver.Chrome()
    # wd.get(url)
    # element = wd.find_element(By.CSS_SELECTOR,'#Zoom > span > a > strong > font > font')
    # element.click()
    # time.sleep(3)
    # break
# print(name_list)