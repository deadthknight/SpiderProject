# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
import chardet
import random
headers = readheaders('./pear_header.txt')
url = 'https://www.pearvideo.com/videoStatus.jsp?'
mrd = random.random()
param = {"contId": "1795528",
         "mrd":f"{mrd}"}

response = requests.get(url=url, headers=headers,params=param)
response.encoding = chardet.detect(response.content)['encoding']

source = response.json()
srcUrl = source['videoInfo']['videos']['srcUrl']
print(source)
print(srcUrl)
systemTime = source['systemTime']
contId = param["contId"]
video_url = srcUrl.replace(systemTime, f"cont-{contId}")
print("拼接后的URL为：", video_url)
# https://video.pearvideo.com/mp4/short/20240727/1722323089020-16033679-hd.mp4
# https://video.pearvideo.com/mp4/short/20240727/cont-1795528-16033679-hd.mp4


# video_date = requests.get(url=video_url, headers=headers).content
#
# with open('./video.mp4', 'wb') as fp:
#     fp.write(video_date)


# print(tree)

if __name__ == "__main__":
    pass
