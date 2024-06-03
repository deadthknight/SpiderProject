#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

from douban.bs4_2_get_type_id import name_id
from douban.bs4_3_get_top import get_top_movies
from douban.bs4_4_get_comment import get_all_final_movies
from pprint import pprint


def get_all_final():

    list = name_id()

    total_key_length = sum(len(key) + 2 for key in list.keys())

    # print(total_key_length)
    # 打印标题
    title = '电影类型'
    padding_length = (total_key_length - len(title)) // 2
    print('=' * padding_length + "=" * 3 + title + '=' * padding_length + '=' * 3)

    # 打印字典内容
    key_list = []
    for key in list.keys():
        key_list.append(key)
        print(key, end=' ')
    print('\r')
    print()

    while True:

        type_name = input('输入电影类型:')
        if type_name in key_list:
            type = list[type_name]
            limit = input('输入查询排名:')
            movies = get_top_movies(type, limit)
            final = get_all_final_movies(movies)
            break
        elif type_name == 'exit':
            print()
            final = "再见"
            break
        else:
            print('输入错误，请重新输入')
    return final


if __name__ == "__main__":
    pprint(get_all_final())
