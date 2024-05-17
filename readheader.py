#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import re


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
    print(readheaders('http_header.txt'))

