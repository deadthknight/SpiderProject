# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import asyncio
import requests
import time
import aiohttp
import aiofiles
import os
from lxml import etree
from readheader import readheaders


def get_source_page(source_url):
    response = requests.get(url=source_url, headers=readheaders('../http_header.txt'))
    # print(response.json())
    return response.json()


def parse_source_page(source_page):
    data_url_list = []
    data_list = source_page["data"]
    for data in data_list:
        name = data['name']
        data_url = "https://chowluking.com/code/" + name
        data_url_list.append(data_url)
    return data_url_list


async def download_one(url,i):
    # https: // chowluking.com / code / 马蜂窝景点爬取.py
    filename = url.split('/')[-1]
    if not os.path.exists(f'./codes'):
        os.makedirs(f'./codes')
    filepath = f'./codes/{str(i) + "_" + filename} '
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  # ssl 报错
        async with session.get(url=url, headers=readheaders('../http_header.txt')) as response:
            if filename.endswith('.py'):
                mode = 'w'  # 文本模式
                text = await response.text()
                tree = etree.HTML(text)
                download_file = tree.xpath('//code[@class="python"]//text()')[0]
                content = download_file
            elif filename.endswith('.rar') or filename.endswith('.apk'):
                mode = 'wb'  # 二进制模式
                content = await response.read()
            elif filename.endswith('.js'):
                mode = 'w'  # 文本模式
                content = await response.text()
            async with aiofiles.open(filepath, mode=mode) as f:
                await f.write(content)
    # filepath = f'./codes/{str(i) + "_" + filename}.txt'  # 下载的txt按顺序排列 i
    # # print('下载该文章')


async def download_all(url_list):
    await asyncio.gather(*(download_one(url, i) for i, url in enumerate(url_list, 1)))


def main():
    url = 'https://chowluking.com/codes'
    source_page = get_source_page(url)
    url_list = parse_source_page(source_page)
    asyncio.run(download_all(url_list))
    print('所有代码已下载完毕')


if __name__ == '__main__':
    s1 = time.time()
    main()
    s2 = time.time()
    print('本次操作所用时间：', s2 - s1)  # 计算并打印操作所用时间
