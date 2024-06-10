#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import re


# Beatuiful Soup
# https://beautifulsoup.readthedocs.io/zh-cn/v4.4.0/
def readheaders(file):
    header_dict = {}
    f = open(file, 'r')
    headers_text = f.read()
    headers = re.split("\n", headers_text)
    for header in headers:
        result = re.split(":", header, maxsplit=1)
        header_dict[result[0]] = result[1].strip()
    f.close()
    return header_dict


if __name__ == '__main__':
    # print(readheaders('http_header.txt'))
    # lst =['1.a','a.b','1.c']
    # n = 0
    # for x in lst:
    #
    #     if x.startswith('1'):
    #         lst[n]='MM'
    #     n+=1
    # print(lst)
    #
    # for x in range(len(lst)):
    #     if lst[x].startswith('1'):
    #         lst[x]='MM'
    # print(lst)
    # print(dir(list))

    lst = [11,22,33,44,55,66,77,88,99]
    result = {}
    # {'bigger':[55,66,77,88,99],'smaller':[11,22,33,44]}
    # print()
    for item in lst:
        if item > 50:
            result.setdefault('bigger',[]).append(item)
        else:
            result.setdefault('smaller',[]).append(item)
    print(result)
    print(result.setdefault('medium'))
    print(result.setdefault('taller',100))
    print(result)