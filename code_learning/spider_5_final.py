# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
# !/usr/bin/env python3.11
# -*- coding: utf-8 -*-
import asyncio
import requests
import time
import aiohttp
import aiofiles
import os
from lxml import etree
from readheader import readheaders
import sys

# Ensure UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

error_count = 0  # 全局变量，用于统计出错的文件数量
timeout_error_count = 0  # 用于统计超时的次数
failed_downloads = []  # 用于记录未成功下载的地址和文件名


def get_source_page(source_url):
    try:
        response = requests.get(url=source_url, headers=readheaders('../http_header.txt'))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"获取源页面出错: {e}")
        return None


def parse_source_page(source_page):
    data_url_list = []
    if source_page and "data" in source_page:
        data_list = source_page["data"]
        for data in data_list:
            name = data['name']
            data_url = "https://chowluking.com/code/" + name
            data_url_list.append(data_url)
    return data_url_list


async def download_one(url, i, semaphore):
    global error_count, timeout_error_count, failed_downloads  # 引用全局变量
    filename = url.split('/')[-1]
    if not os.path.exists('./codes'):
        os.makedirs('./codes')
    filepath = f'./codes/{str(i) + "_" + filename}'

    retry_count = 3
    async with semaphore:
        for attempt in range(retry_count):
            try:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.get(url=url, headers=readheaders('../http_header.txt'),
                                           timeout=aiohttp.ClientTimeout(total=120)) as response:
                        response.raise_for_status()
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
                print(filename, '下载完成')
                return
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"下载 {url} 出错: {e}")
                if isinstance(e, asyncio.TimeoutError):
                    timeout_error_count += 1
                error_count += 1
                if attempt < retry_count - 1:
                    print(f"重试 {url} 第 {attempt + 1} 次")
                    await asyncio.sleep(5)  # 等待5秒后重试
                else:
                    failed_downloads.append((url, filename))


async def download_all(url_list):
    semaphore = asyncio.Semaphore(10)  # 限制并发数量为10
    await asyncio.gather(*(download_one(url, i, semaphore) for i, url in enumerate(url_list, 1)))


def save_failed_downloads(failed_downloads):
    with open('failed_downloads.txt', 'w', encoding='utf-8') as f:
        for url, filename in failed_downloads:
            f.write(f"{url}\t{filename}\n")
    print(f"未成功下载的地址和文件名已记录在 failed_downloads.txt 文件中")


async def retry_failed_downloads():
    global failed_downloads
    if not failed_downloads:
        return

    print("开始重新下载失败的文件...")
    retry_list = failed_downloads
    failed_downloads = []  # 清空之前的失败记录
    semaphore = asyncio.Semaphore(10)  # 限制并发数量为10
    await asyncio.gather(*(download_one(url, i, semaphore) for i, (url, _) in enumerate(retry_list, 1)))

    # 如果还有失败的，记录到文件
    if failed_downloads:
        save_failed_downloads(failed_downloads)


def main():
    url = 'https://chowluking.com/codes'
    source_page = get_source_page(url)
    if source_page is None:
        print("未能获取源页面数据，程序终止")
        return
    url_list = parse_source_page(source_page)
    asyncio.run(download_all(url_list))

    # 尝试重新下载失败的文件
    asyncio.run(retry_failed_downloads())

    if failed_downloads:
        save_failed_downloads(failed_downloads)
    print(f'所有代码已下载完毕，共有 {error_count} 个文件下载出错，其中 {timeout_error_count} 个文件由于超时出错。')


if __name__ == '__main__':
    s1 = time.time()
    main()
    s2 = time.time()
    print('本次操作所用时间:', s2 - s1)
