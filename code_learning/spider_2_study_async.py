#!/usr/bin/env python3.11
# -*- coding:utf-8 -*-
import asyncio
import requests
import time
import aiohttp
import aiofiles
import os
from lxml import etree
from readheader import readheaders

error = 0
failed_urls = []


def get_source_page(source_url):
    response = requests.get(url=source_url, headers=readheaders('../http_header.txt'))
    return response.json()


def parse_source_page(source_page):
    data_url_list = []
    data_list = source_page["data"]
    for data in data_list:
        name = data['name']
        data_url = "https://chowluking.com/code/" + name
        data_url_list.append(data_url)
    return data_url_list


async def download_one(url, i, sem):
    filename = url.split('/')[-1]
    if not os.path.exists(f'./codes'):
        os.makedirs(f'./codes')
    filepath = f'./codes/{str(i) + "_" + filename}'
    print('开始下载', filename)
    async with sem:
        for attempt in range(5):
            try:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.get(url=url, headers=readheaders('../http_header.txt')) as response:
                        if filename.endswith('.py'):
                            mode = 'w'
                            text = await response.text()
                            tree = etree.HTML(text)
                            download_file = tree.xpath('//code[@class="python"]//text()')[0]
                            content = download_file
                            async with aiofiles.open(filepath, mode=mode, encoding='utf-8') as f:
                                await f.write(content)
                        elif filename.endswith('.rar') or filename.endswith('.apk'):
                            mode = 'wb'
                            content = await response.read()
                            async with aiofiles.open(filepath, mode=mode) as f:
                                await f.write(content)
                        elif filename.endswith('.js'):
                            mode = 'w'
                            content = await response.text()
                            async with aiofiles.open(filepath, mode=mode, encoding='utf-8') as f:
                                await f.write(content)
                print(filename, '下载完成')
                break
            except Exception as e:
                print(f"下载第{i}个文件， {filename} 出错: {e}, 重新下载（尝试次数: {attempt + 1}）")
                if attempt == 4:  # 如果已经尝试了5次
                    failed_urls.append(url)


async def download_all(url_list,concurrency_limit):
    sem = asyncio.Semaphore(concurrency_limit)  # 设置并发限制
    await asyncio.gather(*(download_one(url, i,sem) for i, url in enumerate(url_list, 1)))


def main():
    url = 'https://chowluking.com/codes'
    source_page = get_source_page(url)
    url_list = parse_source_page(source_page)
    concurrency_limit = 50
    asyncio.run(download_all(url_list,concurrency_limit))
    print('所有代码已下载完毕')
    if failed_urls:
        print('以下文件下载失败:', failed_urls)


if __name__ == '__main__':
    s1 = time.time()
    main()
    s2 = time.time()
    print('本次操作所用时间：', s2 - s1)
