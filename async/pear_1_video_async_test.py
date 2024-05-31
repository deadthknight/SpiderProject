# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
from bs4 import BeautifulSoup
from pprint import pprint

headers = readheaders('./pear_header.txt')
url = 'https://www.pearvideo.com/videoStatus.jsp?contId=1794456'

response = requests.get(url=url, headers=headers).json()

# tree = etree.HTML(response.json())

# print(response)
video_url = response['videoInfo']['videos']['srcUrl']

print(video_url)

# video_date = requests.get(url=video_url, headers=headers).content
#
# with open('./video.mp4', 'wb') as fp:
#     fp.write(video_date)


# print(tree)

if __name__ == "__main__":
    pass
