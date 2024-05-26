# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import chardet
from readheader import readheaders

headers = readheaders('../http_header.txt')
# print(headers)

url = 'https://www.shicimingju.com/book/sanguoyanyi.html'

response = requests.get(url=url, headers=headers)
# 自动检测：chardet 可以自动检测字节流的编码，确保我们能够正确解码网页内容
response.encoding = chardet.detect(response.content)['encoding']

soup = BeautifulSoup(response.text, 'lxml')

# print(soup.title)

# fp = open('./sanguo.txt', 'w', encoding='utf-8')   #创建文件
for info in soup.select('.book-mulu li >a'):
    title_chapter = info.text
    title_url = 'https://www.shicimingju.com' + info['href']
    response_content = requests.get(url=title_url, headers=headers)
    response_content.encoding = chardet.detect(response_content.content)['encoding']
    soup_content = BeautifulSoup(response_content.text, 'lxml')
    chapter = soup_content.find('div', class_='chapter_content').text

    # 将标题和内容写入文件
    # fp.write(title_chapter + ':\n' + chapter + '\n\n')

    print(title_chapter, '下载完毕！！')

# fp.close()  # 关闭文件对象

if __name__ == "__main__":
    pass
    # 方法二 select 方法返回的是一个 ResultSet 对象，一个元素列表
    # chapter = soup_content.select('.chapter_content')
    # for x in chapter:
    #
    from lxml import etree