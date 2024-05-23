#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import requests
from readheader import readheaders

headers = readheaders('./kfc_header.txt')


def get_kfc_infor():
    print('查询KFC地区门店')
    keyword = input('请输入需要查询地区:')
    num = input('请输入需要查询门店的数量：')
    param = {'cname': '',
             'pid': '',
             'keyword': keyword,
             'pageIndex': 1,
             'pageSize': num}  #查询店面的数量

    url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

    response = requests.post(url=url, headers=headers, params=param).json()

    num_total = response['Table']
    kfc_infor = response['Table1']

    kfc_num = [x['rowcount'] for x in num_total][0]

    return keyword, kfc_num, kfc_infor


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_kfc_infor())
