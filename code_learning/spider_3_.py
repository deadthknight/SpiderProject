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
# sys.stdout.reconfigure(encoding='utf-8')

error_count = 0  # 全局变量，用于统计出错的文件数量

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

async def download_one(session, url, i, retries=3):
    global error_count
    filename = url.split('/')[-1]
    if not os.path.exists('./codes'):
        os.makedirs('./codes')
    filepath = f'./codes/{str(i) + "_" + filename}'
    try:
        async with session.get(url=url, timeout=aiohttp.ClientTimeout(total=60)) as response:
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
    except Exception as e:
        if retries > 0:
            print(f"下载 {url} 出错: {str(e)}. 正在重试...({retries}次剩余)")
            await download_one(session, url, i, retries - 1)
        else:
            print(f"下载 {url} 出错: {str(e)}. 已放弃重试")
            error_count += 1  # 记录错误文件数量

async def download_all(url_list):
    conn = aiohttp.TCPConnector(limit_per_host=20, ssl=False)  # 提升并发限制
    async with aiohttp.ClientSession(connector=conn, headers=readheaders('../http_header.txt')) as session:
        tasks = [download_one(session, url, i) for i, url in enumerate(url_list, 1)]
        await asyncio.gather(*tasks)

def main():
    url = 'https://chowluking.com/codes'
    source_page = get_source_page(url)
    url_list = parse_source_page(source_page)
    asyncio.run(download_all(url_list))
    print('所有代码已下载完毕')
    print(f'总共有 {error_count} 个文件下载出错')

if __name__ == '__main__':
    s1 = time.time()
    main()
    s2 = time.time()
    print('本次操作所用时间：', s2 - s1)
