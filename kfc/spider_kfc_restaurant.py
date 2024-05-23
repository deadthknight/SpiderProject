#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import requests
from readheader import readheaders

headers = readheaders('./kfc_header.txt')





def get_kfc_infor():
    keyword = input('请输入地区:')

    param = {'cname': '',
             'pid': '',
             'keyword': keyword,
             'pageIndex': 1,
             'pageSize': 10}

    url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    response = requests.post(url=url, headers=headers, params=param).json()

    num = response['Table']
    kfc_infor = response['Table1']

    kfc_num = [x['rowcount'] for x in num][0]

    # print(kfc_num)

    return kfc_num,kfc_infor


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_kfc_infor())

