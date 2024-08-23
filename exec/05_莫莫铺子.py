# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from readheader import readheaders

headers = readheaders('../http_header.txt')
url = 'https://openapiv2.dataoke.com/open-api/goods/list-super-goods'
params = {"pageId": "1",
"pageSize": "100",
"keyWords": "休闲零食",
"sort": "0",
"type": "0",
"tmall": "1",
"startTkRate": "3",
"hasCoupon": "1",
"appKey": "622b674f76e31",
"iCmss":"1"}

response = requests.get(url=url,headers=headers,params=params)
print(response.json())