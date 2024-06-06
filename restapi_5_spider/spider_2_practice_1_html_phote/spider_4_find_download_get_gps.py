#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.spider_1_find_image import find_images
from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.spider_2_download_image_from_www_site import download_image
from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.spider_3_find_image_gps import find_gps_image
from os.path import basename
from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.core_info import download_dir, web_page


# 下载所有图片到本地, 然后逐个打开图片读取GPS信息的汇总代码
def download_find_gps(url):
    # 找到图片下载链接！
    imgurls = find_images(url)
    # 下载图片到本地，并且返回文件清单！
    img_file_names = download_image(imgurls, download_dir)
    # 逐个分析图片的GPS信息
    for img_downloaded in img_file_names:
        print('=' * 20 + basename(img_downloaded) + '=' * 20)
        print(find_gps_image(img_downloaded))


if __name__ == '__main__':
    # 注意图片源之于内部系统服务器(NGINX部署),正常调试模式的DJANGO图片是没有GPS信息的
    download_find_gps(web_page)
