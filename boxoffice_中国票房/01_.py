# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import time

import requests
from lxml import etree
import requests
from pprint import pprint

def wraggper(fn):
    def inner(*args, **kwargs):
        start_time = time.time()
        ret = fn(*args, **kwargs)
        end_time = time.time()
        print('本次操作时间: %.2f' % (end_time - start_time))
        return ret
    return inner

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
}

def get_page_source(url,delay=3):
    while True:
        try:
            response = requests.get(url=url,  headers=headers, verify=False)
            response.raise_for_status()
            # 自动检测：chardet 可以自动检测字节流的编码，确保我们能够正确解码网页内容
            # response.encoding = chardet.detect(response.content)['encoding']
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"获取失败：{e}，将在 {delay} 秒后重试...")
            time.sleep(delay)


def parse_data(pg_source):
    tree = etree.HTML(pg_source)
    tr_list = tree.xpath('//*[@class="entry-content"]//tr')[1:]
    total = []
    for tr in tr_list:
        name = tr.xpath('./td[3]//text()')
        if name:
            name = ''.join(name)
            if '#' in name:
                name = name.replace('#','') + '(上映又撤档)'
        else:
            continue
        year = tr.xpath('./td[2]//text()')[0]
        price = tr.xpath('./td[last()]//text()')[0].replace(',','.')
        if '（' in price:
            price = price.split('（')[0] + "万元" + '（' + price.split('（')[1]
        elif '–' in price or '暂无' in price or '未知' in price:
            price = '0'
        else:
            price = price + "万元"
        dic = {"年代":year,"电影名": name, "票房": price}
        total.append(dic)
    # total = sorted(total,key=lambda x:float(x['票房'].split('万元')[0]))
    return total

def savedata(data):
    with open('boxoffice.txt', 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"{item['电影名']},{item['票房']}\n")


def main(url):
    # url = 'http://www.boxofficecn.com/boxoffice2024'
    page_source = get_page_source(url)
    data = parse_data(page_source)
    # savedata(data)
    return data

@wraggper
def all_data():
    url_list = []
    for i in range (2014 , 2024):
        url = f'http://www.boxofficecn.com/boxoffice{i}'
        url_list.append(url)

    total = []
    for url in url_list:
        data = main(url)
        total.extend(data)
    total = sorted(total, key=lambda x: float(x['票房'].split('万元')[0]))
    return total


if __name__ == "__main__":
    pprint(all_data())

