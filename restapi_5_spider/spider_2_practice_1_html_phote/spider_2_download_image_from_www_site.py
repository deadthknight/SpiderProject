#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

import requests
from urllib.parse import urlsplit
from os.path import basename
import os
from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.core_info import download_dir

client = requests.session()


# 下载imgurls清单中的每一张图片到下载目录
def download_image(imgurls, folder):
    # 最终返回的,下载到本地的每一张图片的完整路径清单
    img_file_names = []
    # 切换到下载文件存放的目录
    os.chdir(folder)
    print('开始下载文件....')
    for imgurl in imgurls:
        # 逐个得到下载文件的完整链接
        try:
            # 获取图片二进制内容
            img_content = client.get(imgurl).content
            # print(urlsplit(imgurl))
            # SplitResult(scheme='http', netloc='www.qytang.com', path='/gps/gg_gps.jpg', query='', fragment='')
            # urlsplit(imgurl).path = '/gps/gg_gps.jpg'
            # basename(urlsplit(imgurl).path) = 'gg_gps.jpg'
            image_file_name = basename(urlsplit(imgurl).path)  # 得到文件名
            image_file = open(image_file_name, 'wb')
            image_file.write(img_content)  # 写入文件内容
            image_file.close()
            # 产生存放文件的完整路径(目录+文件名),便于后续分析GPS信息的代码读取文件
            img_file_name = str(folder) + str(image_file_name)
            img_file_names.append(img_file_name)  # 把写入的完整文件路径添加到清单imgFileNames

        except Exception as e:
            print(e)
            pass
    return img_file_names


if __name__ == '__main__':
    img_urls = ['https://qytsystem.qytang.com/static/files/images/gps/gg_gps.jpg']
    print(download_image(img_urls, download_dir))
