# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from pprint import pprint
from urllib.parse import urlparse
import os
from font_识别 import read_num_by_draw
from loguru import logger
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


def download_font_file():
    url = f"https://lf6-awef.bytetos.com/obj/awesome-font/c/96fc7b50b772f52.woff2"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    parse_url = urlparse(url)
    font_name = parse_url.path.split('/')[-1]
    font_path = f"font/{font_name}"

    # 检查文件是否存在
    if not os.path.exists(font_path):
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 创建目标文件夹（如果不存在）
        os.makedirs("font", exist_ok=True)

        # 保存字体文件
        with open(font_path, 'wb') as f:
            f.write(response.content)
        print(f"下载完成: {font_name}")
    else:
        print(f"文件已存在: {font_name}")
    logger.info('文件检查完')
    font_dic = read_num_by_draw(font_path)
    return font_dic

def get_source_page(url):
    params = {
        'aid': '1839',
        'app_name': 'auto_web_pc',
    }
    data = {
        "": "",
        "sh_city_name": "全国",
        "page": "2",
        "limit": "20"
    }
    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取失败：{e}")


def parse_pg_source(pg_source):
    data = pg_source['data']['search_sh_sku_info_list']
    for x in data:
        # print(x)
        dic = {
            '标题': x['title'],
            '品牌': x['brand_name'],
            '车型': x['series_name'],
            '城市 ': x['brand_source_city_name'],
            '年份': x['car_year'],
            '价格': x['sh_price'],
            '官方价格': x['official_price'],
            '公里数': x['sub_title']
        }
        for i in x['sh_price']:
            print(i, ord(i))
        pprint(dic)
        break


def main():
    url = 'https://www.dongchedi.com/motor/pc/sh/sh_sku_list?'
    pg_source = get_source_page(url)
    # print(pg_source)
    parse_pg_source(pg_source)


if __name__ == '__main__':
    # main()
    font=download_font_file()
    print(font)
