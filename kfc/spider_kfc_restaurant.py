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


    try:
        response = requests.post(url=url, headers=headers, params=param)

        # print(response.status_code)

        response.raise_for_status() # 检查请求是否成功 不成功抛异常

        response = response.json()

        # print(response)

        # response结果
        # {'Table': [{'rowcount': 272}], 'Table1': [
        #     {'rownum': 1, 'storeName': '京通新城', 'addressDetail': '朝阳路杨闸环岛西北京通苑30号楼一层南侧',
        #      'pro': '24小时,Wi-Fi,点唱机,店内参观,礼品卡', 'provinceName': '北京市', 'cityName': '北京市'}]}

        num_total = response['Table']
        kfc_infor = response['Table1']

        # print(kfc_infor)

        kfc_num = [x['rowcount'] for x in num_total][0]

        return keyword, kfc_num, kfc_infor

    except Exception as e:
        return print(e)









if __name__ == "__main__":
    from pprint import pprint

    get_kfc_infor()
