# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
import chardet
from readheader import readheaders

headers = readheaders('./header_code.txt')
url = 'https://www.dytt8.com/'

response = requests.get(url=url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']
tree = etree.HTML(response.text)
tr_list = tree.xpath('(//div[@class="bd3rl"])[1]/div[2]//div[2]//tr[position()>1]')
# print(len(tr_list))
name_list = []
download_list = []
for tr in tr_list:
    name = tr.xpath('./td/a[2]/text()')[0]
    url = 'https://www.dytt8.com/'+ tr.xpath('./td/a[2]/@href')[0]

    print(name,url)
    name_list.append(name)
    break
# print(name_list)