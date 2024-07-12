#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from multiprocessing import Pool, Manager
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def get_source_pages(page):
    url = f'https://www.doutupk.com/article/list/?page={page}'
    response = requests.get(url, headers=headers)
    return response.text

def get_urls(page):
    html = get_source_pages(page)
    tree = etree.HTML(html)
    pic_urls = tree.xpath('//*[@class="col-xs-6 col-sm-3"]/img/@data-original')
    return pic_urls

def download_file(url, results_queue):
    try:
        filename = url.split('/')[-1]
        if filename.endswith('.gif'):
            response = requests.get(url, headers=headers)
            with open(filename, 'wb') as f:
                f.write(response.content)
            results_queue.put(filename)  # 把文件名放入队列以便汇总
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    page_count = 10
    manager = Manager()
    results_queue = manager.Queue()

    with Pool(processes=30) as pool:
        for page in range(1, page_count + 1):
            urls = get_urls(page)
            pool.starmap(download_file, [(url, results_queue) for url in urls])

    # 输出已下载完成的文件名
    while not results_queue.empty():
        print(f"已下载文件: {results_queue.get()}")

if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print("全部下载完毕！！！")
    print('本次操作时间: %.2f' % (t2 - t1))
