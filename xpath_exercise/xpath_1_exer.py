# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
from time_decorater import run_time
from multiprocessing import cpu_count, Pool as ProcessPool
from multiprocessing.pool import ThreadPool
from multiprocessing import freeze_support
import time
from pprint import pprint

headers = readheaders('../http_header.txt')


# text_all = []
# prices = []
# for num in range(1,3):
#     url = 'https://bj.58.com/ershoufang/p'+ str(num)
# print(url)


def page_num(num):
    page_list = []
    for x in range(1, num):
        url = 'https://bj.58.com/ershoufang/p' + str(x)
        page_list.append(url)
    return page_list

def get_infor_house(url):
    text_all = []
    prices = []

    response = requests.get(url=url, headers=headers).text

    tree = etree.HTML(response)

    div_list = tree.xpath('//section[@class="list"]/div')

    for div in div_list:
        # text = div.xpath('./a/div[2]/div[1]/div[1]/h3/text()')
        text1 = div.xpath('.//h3/text()')[0]
        # print(text1)
        text_all.append(text1)
        price = div.xpath('.//span[@class="property-price-total-num"]/text()')[0] + '万'
        # print(price)
        prices.append(price)
        # time.sleep(2)
    # print(len(text_all))
    final = list(zip(text_all, prices))
    # print(final)
    final_sorted = sorted(final, key=lambda price: price[1], reverse=True)
    return final_sorted

@run_time()
def get_all_together():
    num = int(input("输入page："))
    get_all = []
    url_list = page_num(num)
    n = 1
    for x in url_list:
        get_all.append('Page' + n + "Done")
        get_all.append(get_infor_house(x))
        n+=1

    return get_all

# print(len(final_sorted))
# pprint(final_sorted)
if __name__ == "__main__":

    # @run_time()
    # def async_test():
    #     freeze_support()
    #     pool = ThreadPool(10)
    #     results = []
    #     num = int(input("输入page："))
    #     for x in page_num(num):
    #         result = pool.apply_async(get_infor_house,args=(x,))
    #         results.append(result)
    #     pool.close()
    #     pool.join()
    #     for i in results:
    #         print(i.get())
    # #
    # async_test()

    # 多线程
    from multiprocessing.dummy import Pool

    pool = Pool(10)
    x = pool.map(get_infor_house,page_num(10))
    # print(get_all_together())
    # print(len(x))
    sor=[]
    for i in x:
        for j in i:
            sor.append(j)
    sor = sorted(sor,key=lambda x:x[1],reverse=True)
    print(sor)
