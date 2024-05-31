# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
import chardet
import time
from pprint import pprint
import os
import re

headers = readheaders('../http_header.txt')

url = 'https://pic.netbian.com/4kdongwu/'

response = requests.get(url=url, headers=headers)
# 中文处理乱码 方法一
# response.encoding = chardet.detect(response.content)['encoding']

tree = etree.HTML(response.text)

li_list = tree.xpath('//div[@class="slist"]//li')
# print(li_list)
if not os.path.exists('./download_pic'):
    os.mkdir('./download_pic')

# 定义非法字符过滤函数
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

for li in li_list:
    download_url = 'https://pic.netbian.com' + li.xpath('.//img/@src')[0]
    # print(download_url)
    name = li.xpath('.//img/@alt')[0] + '.jpg'
    # 处理中文乱码 方法二
    name = name.encode('iso-8859-1').decode('gbk')
    # 替换特殊字符
    name = sanitize_filename(name)
    # name1 = name.replace('*', '_')
    # print (name1)
    download_pic = requests.get(url=download_url,headers=headers).content
    pic_path = 'download_pic/' + name
    with open(pic_path,'wb') as fp:
        fp.write(download_pic)
        print ('Downloading Done')
    break

if __name__ == "__main__":
    pass