#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

import random
import asyncio
import aiohttp
from lxml import etree
from time_decorater import run_time

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
}
async def download_one(url):
    while True:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        page_source = await response.text(encoding='utf-8')
                        tree = etree.HTML(page_source)
                        tr_list = tree.xpath('//*[@class="entry-content"]//tr')[1:]
                        total = []
                        for tr in tr_list:
                            name = tr.xpath('./td[3]//text()')
                            if name and name!='-':
                                name = ''.join(name)
                                if '#' in name:
                                    name = name.replace('#', '') + '(上映又撤档)'
                            else:
                                continue
                            year = tr.xpath('./td[2]//text()')[0]
                            price = tr.xpath('./td[last()]//text()')[0].replace(',', '.')
                            if '（' in price:
                                price = price.split('（')[0] + "万元" + '（' + price.split('（')[1]
                            elif '–' in price or '暂无' in price or '未知' in price:
                                price = '0'
                            else:
                                price = price + "万元"
                            dic = {"年代": year, "电影名": name, "票房": price}
                            total.append(dic)
                        return total
                    else:
                        print(f"Failed to fetch URL {url}, status code: {response.status}")
                        await asyncio.sleep(random.uniform(1, 3))  # 添加随机延迟
            except aiohttp.ClientError as e:
                print(f"Error fetching URL {url}: {e}")
                await asyncio.sleep(random.uniform(1, 3))  # 添加随机延迟


async def download_file(url_list):

    return await asyncio.gather(*(download_one(url) for url in url_list))


@run_time
def main():
    url_list = []
    for i in range(2017, 2019):
        url = f'http://www.boxofficecn.com/boxoffice{i}'
        url_list.append(url)
    totals = asyncio.run(download_file(url_list))
    totals = analyse_data(totals)
    return totals


def analyse_data(data):
    total_list = []
    for x in data:
        for i in x :
            total_list.append(i)
    total_list = sorted(total_list, key=lambda x: float(x['票房'].split('万元')[0]))
    return total_list

if __name__ == "__main__":
    result = main()
    for i in result:
        if i["票房"]=='0':
            i["票房"]='暂无数据'
        print(i)




