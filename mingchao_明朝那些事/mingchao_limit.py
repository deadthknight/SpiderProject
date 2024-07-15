#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
import chardet
import asyncio
import aiohttp
import aiofiles
import os
from readheader import readheaders
from time_decorater import run_time





def get_chapter_urls(sourcetext):
    chapter_urls = []
    tree = etree.HTML(sourcetext)
    mulu_list = tree.xpath('//*[@class="mulu"]')
    for mulu in mulu_list:
        chapter_name = mulu.xpath('.//tr[1]//text()')
        chapter_name = ''.join(chapter_name).strip().replace('：', '-')
        tr_list = mulu.xpath('.//tr')[1:]
        for tr in tr_list:
            td_list = tr.xpath('./td')
            for td in td_list:
                chapter_name_children = td.xpath('.//text()')
                chapter_name_children = ''.join(chapter_name_children).strip()
                chapter_name_children_url = td.xpath('.//@href')
                chapter_name_children_url = ''.join(chapter_name_children_url).strip()
                if not chapter_name_children:
                    continue
                dic = {"卷名": chapter_name,
                       "章名": chapter_name_children,
                       "url": chapter_name_children_url
                       }
                chapter_urls.append(dic)
    return chapter_urls


def get_source_page(url):
    response = requests.get(url, headers=readheaders('../http_header.txt'), verify=False)
    response.encoding = chardet.detect(response.content)['encoding']  # 解决乱码 方案一
    # response.encoding = "UTF-8"  # 方案二
    return response.text


async def download_one(chapter, i, sem):
    volume_name = chapter['卷名']
    chapter_name = chapter['章名']
    chapter_url = chapter['url']

    if not os.path.exists(f'./{volume_name}'):
        os.makedirs(f'./{volume_name}')
    filepath = f'./{volume_name}/{str(i) + "_" + chapter_name}.txt'  # 下载的txt按顺序排列 i

    async with sem:  # 使用信号量来限制并发数量
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  # ssl 报错
            async with session.get(url=chapter_url, headers=readheaders('../http_header.txt')) as response:
                page_source = await response.text(encoding='utf-8')  # 拿源代码
                # content = await response.content.read() #拿字节流 图片 视频
                tree = etree.HTML(page_source)
                content = tree.xpath('//div[@class="content"]/p[position() != last()]/text()')  # 不要最后一个P里面的text
                content = ''.join(content).replace('\n', '').replace('\r', '').strip()  # 去除里面的回车/换行/空格等
                async with aiofiles.open(filepath, mode='w', encoding='utf-8') as f:
                    await f.write(content)
    print(f'下载完毕: {filepath}')


async def download_file(chapter_list, concurrency_limit):
    sem = asyncio.Semaphore(concurrency_limit)  # 设置并发限制
    await asyncio.gather(*(download_one(chapter, i, sem) for i, chapter in enumerate(chapter_list, 1)))


@run_time
def main():
    url = 'https://www.mingchaonaxieshier.com/'
    source_page = get_source_page(url)
    chapter_list = get_chapter_urls(source_page)
    concurrency_limit = 50  # 设置并发数量
    asyncio.run(download_file(chapter_list, concurrency_limit))  # 如果报错 用下面命令
    # event_loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(event_loop)
    # event_loop.run_until_complete(download_file(chapter_list))
    print('所有文章已下载完毕')


if __name__ == '__main__':
    main()  # 不限制并发3.7s    limit=50 5.52s  limit=30  7.79s   limit=10  15.23s



