# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests


url = 'https://search.kongfz.com/pc-gw/search-web/client/pc/product/keyword/list?'
params = {"keyword": "9787040010251",
          "dataType": "0",
          "page": "1",
          "userArea": "1006000000"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
response = requests.get(url=url,headers=headers,params=params)

page_source = response.json()
# print(page_source)

for item in page_source["data"]["itemResponse"]["list"]:
    print(f'书名：{item.get("title").replace('（','')},'
          f'品质：{item["quality"]},'
          f'价格{item["price"]},'
          f'运费{item["postage"]["shippingList"][0]["shippingFee"]}\n'
          f'运费=={item.get("postage").get("shippingList")[0].get("shippingFee")}')