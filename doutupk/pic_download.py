#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
from multiprocessing import Queue
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}


def get_source_pages(page):
    url = f'https://www.doutupk.com/article/list/?page={page}'
    response = requests.get(url,headers=headers)
    return response.text

def get_urls(q):
    for page in range (1,2):
        file = get_source_pages(page)
        tree = etree.HTML(file)
        pic_urls = tree.xpath('//*[@class="col-xs-6 col-sm-3"]/img/@data-original')
        for img_url in pic_urls:
            print(img_url)  # ? 7
            # 把拿到的img_url 塞入队列
            q.put(img_url)  # 固定的
    q.put("滚蛋吧.没了")  # 结束的一个消息

def img_process(q):  # 从队列中提取url. 进行下载
    with ThreadPoolExecutor(30) as t:  # ?
        while 1:  # 这边不确定有多少个. 那就一直拿
            img_url = q.get()  # 没有问题. 这里面, get是一个阻塞的逻辑
            if img_url == '滚蛋吧.没了':
                break
            # 在进程中开启多线程(唐马儒)
            t.submit(download_file, img_url)
def download_file(url):
    filename = url.split('/')[-1]
    if filename.endswith('.gif'):
        file = requests.get(url,headers=headers).content
        with open(filename,'wb') as f:
            f.write(file)



if __name__ == "__main__":

    # print(s2-s1)  #43

    # from multiprocessing.dummy import Pool  #线程池
    # from multiprocessing import Queue
    # import time
    #
    # pool = Pool(30)
    # t1 = time.time()
    # for page in range(1,10):
    #     pool.map(download_file, get_urls(page))
    # pool.close()
    # pool.join()
    # print("全部下载完毕！！！")
    # t2 = time.time()
    # print('本次操作时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
    s1 = time.time()
    q = Queue()  # 主进程 水
    p1 = Process(target=get_urls, args=(q,))  # 单独开辟一个内存 阿大
    p2 = Process(target=img_process, args=(q,))  # 单独开辟一个内存 阿二

    p1.start()
    p2.start()

    p1.join()  # 主进程等待子进程跑完
    p2.join()  # 主进程等待子进程跑完

    s2 = time.time()
    print(s2 - s1)
    #4.8
