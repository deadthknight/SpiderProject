# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
from bs4 import BeautifulSoup
from pprint import pprint
import random
import chardet
headers = readheaders('./pear_header.txt')
url = 'https://www.pearvideo.com/popular?'

# param = {'reqType': '',
#          'categoryId': '',
#          'start': 0,
#          'sort': 0,
#          }

response = requests.get(url=url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']

tree = etree.HTML(response.text)
li_list = tree.xpath('//*[@id="popularList"]/li')
print(li_list)
# print(tree)




# video_date = requests.get(url=video_url, headers=headers).content
#
# with open('./video.mp4', 'wb') as fp:
#     fp.write(video_date)


# print(tree)

if __name__ == "__main__":
    pass
