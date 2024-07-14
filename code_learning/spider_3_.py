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

sem = asyncio.Semaphore(5)  # 设置并发数量限制为5


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


async def download_one(url, i, retries=3):
    async with sem:  # 在这里使用信号量限制并发数量
        filename = url.split('/')[-1]
        if not os.path.exists(f'./codes'):
            os.makedirs(f'./codes')
        filepath = f'./codes/{str(i) + "_" + filename}'

        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.get(url=url, headers=readheaders('../http_header.txt')) as response:
                        if filename.endswith('.py'):
                            mode = 'w'
                            text = await response.text()
                            tree = etree.HTML(text)
                            download_file = tree.xpath('//code[@class="python"]//text()')[0]
                            content = download_file
                        elif filename.endswith('.rar') or filename.endswith('.apk'):
                            mode = 'wb'
                            content = await response.read()
                        elif filename.endswith('.js'):
                            mode = 'w'
                            content = await response.text()
                        async with aiofiles.open(filepath, mode=mode) as f:
                            await f.write(content)
                break  # 成功后退出重试循环
            except aiohttp.ClientError as e:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt + 1 == retries:
                    print(f"Failed to download {url} after {retries} attempts")


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
    print('本次操作所用时间：', s2 - s1)
