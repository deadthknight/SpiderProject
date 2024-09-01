# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import re

url = 'https://www.regulations.gov/docket/FDA-2016-D-1399/document'

# https://spidertools.cn/#/curl2Request

import requests


# headers = {
#     # "origin": "https://www.regulations.gov",
#     "referer": "https://www.regulations.gov/",   #经测试：origin和referer需要任意一个
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
#     # "x-api-key": "5F20SbTVakeYfU9i5gX1dxx96sw4KELUQxAHhcHa"
# }
# url = "https://api.regulations.gov/v4/documents?filter%5BdocketId%5D=FDA-2016-D-1399&page%5Bnumber%5D=1&sort=-commentEndDate"
# params = {
#     "filter[docketId]": "FDA-2016-D-1399",
#     "page[number]": "1",
#     "sort": "-commentEndDate"
# }
# response = requests.get(url, headers=headers, params=params)
#
# print(response.text)
# print(response)
# ===========================================================

doc_url = 'https://www.regulations.gov/docket/FDA-2016-D-1399/document'

headers = {
    # "origin": "https://www.regulations.gov",
    "referer": "https://www.regulations.gov/",   #经测试：origin和referer需要任意一个
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
     }
res = requests.get(doc_url,headers=headers)
api_key = re.search(r'apiKey%22%3A%22(?P<key>.*?)%22%2C%22api',res.text)
print(f'返回的api_key:{api_key.group('key')}')
headers.update({"x-api-key": api_key.group('key')})

url = "https://api.regulations.gov/v4/documents?filter%5BdocketId%5D=FDA-2016-D-1399&page%5Bnumber%5D=1&sort=-commentEndDate"
params = {
    "filter[docketId]": "FDA-2016-D-1399",
    "page[number]": "1",
    "sort": "-commentEndDate"}
response = requests.get(url, headers=headers, params=params)
print(response)