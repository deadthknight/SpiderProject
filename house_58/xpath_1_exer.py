# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
import time
from pprint import pprint

headers = readheaders('../http_header.txt')
text_all = []
prices = []
for num in range(1,3):
    url = 'https://bj.58.com/ershoufang/p'+ str(num)
    # print(url)
    response = requests.get(url=url, headers=headers).text

    # print(response)

    tree = etree.HTML(response)

    div_list = tree.xpath('//section[@class="list"]/div')
    # nu = len(div_list)
    # print(nu)

    for div in div_list:
        # text = div.xpath('./a/div[2]/div[1]/div[1]/h3/text()')
        text1 = div.xpath('.//h3/text()')[0]
        # print(text1)
        text_all.append(text1)
        price = div.xpath('.//span[@class="property-price-total-num"]/text()')[0]+'万'
        # print(price)
        prices.append(price)
        # time.sleep(2)
    # print(len(text_all))
final = list(zip(text_all, prices))
# print(final)
final_sorted = sorted(final, key=lambda price:price[1],reverse=True)
# print(len(final_sorted))
pprint(final_sorted)
if __name__ == "__main__":
    # l1 = ['beijing' , 'shanghai']
    # l2 = ['100' , '1000']
    # l3 = list(zip(l1, l2))
    # print(l3)
    # l3_sorted = sorted(l3,key=lambda price:int(price[1]),reverse=True)
    # print(l3_sorted)
    pass