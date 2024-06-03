#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
import aiohttp
import asyncio
from lxml import etree
from readheader import readheaders
import os
from urllib.parse import urlparse
from time_decorater import run_time

headers = readheaders('./header_code.txt')


async def get_url_list():
    url = 'https://chowluking.com/codes'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            json_data = await response.json()

    name_list = []
    download_url_list = []
    if not os.path.exists('./files'):
        os.mkdir('./files')
    for name in json_data['data']:
        name_list.append(name['name'])
        filename = name['name']
        download_url = 'https://chowluking.com/code/' + filename
        download_url_list.append(download_url)
    return download_url_list


async def download_file(session, download_url, retries=3, timeout=10):
    parsed_url = urlparse(download_url)
    file_name = os.path.basename(parsed_url.path)
    filepath = './files/' + file_name

    for attempt in range(retries):
        try:
            async with session.get(download_url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    try:
                        if file_name.endswith('.py'):
                            mode = 'w'  # 文本模式
                            text = await response.text()
                            tree = etree.HTML(text)
                            download_file = tree.xpath('//code[@class="python"]//text()')[0]
                            content = download_file
                        elif file_name.endswith('.rar') or file_name.endswith('.apk'):
                            mode = 'wb'  # 二进制模式
                            content = await response.read()
                        elif file_name.endswith('.js'):
                            mode = 'w'  # 文本模式
                            content = await response.text()

                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        with open(filepath, mode) as file:
                            file.write(content)
                        print(f"文件 '{file_name}' 下载成功.")
                        return
                    except Exception as e:
                        print(f"处理文件 '{file_name}' 时出错: {e}")
                else:
                    print(f"下载失败: {response.status}")
        except (aiohttp.ClientPayloadError, aiohttp.ClientConnectorError, asyncio.exceptions.TimeoutError) as e:
            print(f"下载文件 '{file_name}' 时出错: {e}")
            if attempt < retries - 1:
                print(f"重试 {attempt + 1}/{retries}...")
            else:
                print(f"文件 '{file_name}' 下载失败. 尝试次数: {retries}")


async def main():
    download_url_list = await get_url_list()
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in download_url_list]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    import time

    t1 = time.time()
    asyncio.run(main())
    print("全部下载完毕！！！")
    t2 = time.time()
    print('本次操作时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
