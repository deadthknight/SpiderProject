#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

# pip3 install exifread
import exifread
import re
from part1_restapi.restapi_5_spider.spider_2_practice_1_html_phote.core_info import download_dir


# 读取图片的元数据, 提取GPS信息
def find_gps_image(filepath):
    gps = {}
    image_date = ''
    f = open(filepath, 'rb')
    # 读取元数据, 提取标签和值
    tags = exifread.process_file(f)
    for tag, value in tags.items():
        if re.match('GPS GPSLatitudeRef', tag):
            gps['GPSLatitudeRef'] = str(value)
        elif re.match('GPS GPSLongitudeRef', tag):
            gps['GPSLongitudeRef'] = str(value)
        elif re.match('GPS GPSAltitudeRef', tag):
            gps['GPSAltitudeRef'] = int(str(value))
        elif re.match('GPS GPSLatitude', tag):
            try:
                match_result = re.match(r'\[(\w*), (\w*), (\w.*)/(\w.*)\]', str(value)).groups()
                gps['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])/int(match_result[3])
            except Exception:
                gps['GPSLatitude'] = str(value)
        elif re.match('GPS GPSLongitude', tag):
            try:
                match_result = re.match(r'\[(\w*), (\w*), (\w.*)/(\w.*)\]', str(value)).groups()
                gps['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])/int(match_result[3])
            except Exception:
                gps['GPSLongitude'] = str(value)
        elif re.match('GPS GPSAltitude', tag):
            gps['GPSAltitude'] = str(value)
        elif re.match('Image DateTime', tag):
            image_date = str(value)
    return {'GPS信息': gps, '时间信息': image_date}
    # ttp://www.gpsspg.com/maps.htm


if __name__ == '__main__':
    print(find_gps_image(download_dir + "gps_test_5.jpg"))

# 运行结果
# {'GPS信息': {'GPSLatitudeRef': 'N', 'GPSLatitude': (39, 58, 38.481445), 'GPSLongitudeRef': 'E', 'GPSLongitude': (116, 17, 59.598999), 'GPSAltitudeRef': 1, 'GPSAltitude': '0'}, '时间信息': '2016:05:25 20:43:46'}
