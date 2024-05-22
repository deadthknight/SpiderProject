#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import re
# from bs4
from douban.bs4_1_get_main_page import main_page


# 获取类型和id
def name_id():
    types = main_page.find('div', class_='types').find_all('a')

    get_type_id = {}
    name_list = []
    for get_type in types:
        pattern = re.compile(r'type_name=(\S+)&type=(\d+)')
        result = re.search(pattern, get_type.get('href')).groups()
        get_type_id[result[0]] = result[1]

    return get_type_id


if __name__ == "__main__":
    print(name_id())
