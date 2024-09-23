# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import json

import requests
from pprint import pprint
from urllib.parse import urlparse
import os
from font_03 import font_split_single_img,ocrWords,readImagName
from loguru import logger
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


def download_font_file():
    url = f"https://lf6-awef.bytetos.com/obj/awesome-font/c/96fc7b50b772f52.woff2"
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
        logger.info(f"下载完成: {font_name}")
    else:
        logger.info(f"文件已存在: {font_name}")

    return font_path

def change_code(word,font_dic):
    woed_decode=''
    for num in word:
        try:
            word_real = font_dic[str(ord(num))]
        except:
            word_real = num
        woed_decode += word_real
    return woed_decode

def get_source_page(url):
    params = {
        'aid': '1839',
        'app_name': 'auto_web_pc',
    }
    data = {
        "": "",
        "sh_city_name": "北京",
        "page": "2",
        "limit": "60"
    }
    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取失败：{e}")


def parse_pg_source(pg_source,font_dic):
    data = pg_source['data']['search_sh_sku_info_list']
    for x in data:
        # print(x)
        dic = {
            '标题': x['title'],
            '品牌': x['brand_name'],
            '车型': x['series_name'],
            '城市 ': x['brand_source_city_name'],
            '年份': x['car_year'],
            '价格': change_code(x['sh_price'],font_dic),
            '官方价格': change_code(x['official_price'],font_dic),
            '公里数': change_code(x['sub_title'],font_dic)
        }
        # for i in x['sh_price']:
        #     print(i, ord(i))
        print(dic)



def main():
    url = 'https://www.dongchedi.com/motor/pc/sh/sh_sku_list?'
    font_path = download_font_file()

    # img_dir=font_split_single_img(font_path)
    # img_copy_dir = ocrWords(img_dir)
    # input('确认识别后的文字')
    # word_map = readImagName(img_copy_dir)
    with open('ocr_dddd.json', 'r', encoding='utf-8') as f:
        word_map = json.load(f)  # 直接加载 JSON 数据
    # print(word_map)
    pg_source = get_source_page(url)
    # print(pg_source)
    parse_pg_source(pg_source, word_map)


if __name__ == '__main__':
    main()
    # font = download_font_file()
    # print(font)
