# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
import chardet
from readheader import readheaders
from loguru import logger


movie_name = input('输入关键字：')
headers = readheaders('./header_code.txt')
url = 'https://dygod.org/index.htm'
# url = 'https://dytt.dytt8.net/index.htm'

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
    # print(tree)
    # title = tree.xpath('//title/text()')
    # print(title)
    download_url = tree.xpath('//*[@id="Zoom"]//a/@href')[0]
    # download_url = tree.xpath('//*[@id="Zoom"]/span/a/@href')[0] 网页可以找到 代码运行找不到

    dic = {'电影名称':name,
           '链接地址':movie_url,
           '下载链接':download_url}
    movies.append(dic)
# pprint(movies)
# 构建字典并添加到列表中

# 搜索和打印
if movie_name:
    matched_movies = [x for x in movies if movie_name in x['电影名称']]  # 找到匹配的电影
    if matched_movies:  # 如果找到了匹配的电影
        for movie in matched_movies:
            logger.info(f"电影名称: {movie['电影名称']}\n下载链接: {movie['下载链接']}")
    else:  # 如果没有找到匹配的电影
        print("未找到匹配的电影")
        for movie in movies:
            logger.info(movie['电影名称'])
else:
    # 没有输入名字时，打印所有电影名称
    for movie in movies:
        logger.info(movie['电影名称'])

    # 调用selenium 点击下载链接
    # wd = webdriver.Chrome()
    # wd.get(url)
    # element = wd.find_element(By.CSS_SELECTOR,'#Zoom > span > a > strong > font > font')
    # element.click()
    # time.sleep(3)
    # break
# print(name_list)
