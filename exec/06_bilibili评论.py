# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import time
import requests
import csv
import hashlib
import json

# 创建csv
f = open(file='comment.csv', mode='w', encoding='utf-8', newline='')  # 创建文件
# 字典写入
csv_writer = csv.DictWriter(f, fieldnames=['昵称', 'comment'])
# 写入表头
csv_writer.writeheader()

headers = {
    'origin': 'https://www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

cookies = {
    'buvid3': '9AFEF60D-B253-D97F-3026-BE61E781D76C16768infoc',
    'b_nut': '1717419416',
    '_uuid': '7E828CA5-4142-FBE7-596C-82127AF56F9817242infoc',
    'enable_web_push': 'DISABLE',
    'DedeUserID': '290041701',
    'DedeUserID__ckMd5': '08a0369c598f5324',
    'PVID': '1',
    'rpdid': "|(k|kmkY)|J~0J'u~u~RumRm)",
    'header_theme_version': 'CLOSE',
    'hit-dyn-v2': '1',
    'buvid_fp_plain': 'undefined',
    'buvid4': '50E17A7D-533E-9F58-59BB-51E9D575850217985-024060312-d1kKipACZEBAnJ%2FkykWItg%3D%3D',
    'CURRENT_QUALITY': '80',
    'CURRENT_FNVAL': '4048',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjYyMzcxMTMsImlhdCI6MTcyNTk3Nzg1MywicGx0IjotMX0.vRu0jrVxts27p8ly95fRCBCO17DQ3I9WTYYbe91FCP4',
    'bili_ticket_expires': '1726237053',
    'fingerprint': 'c32a4b8711ecf7f2cdb678fd5ed0e262',
    'buvid_fp': 'c32a4b8711ecf7f2cdb678fd5ed0e262',
    'home_feed_column': '5',
    'browser_resolution': '1920-970',
    'SESSDATA': 'f6719299%2C1741610194%2Cef807%2A91CjDJlOQt0XSTvx3GFy-Ty_uZILB7FZNn79QpQNGmpkUbu6WEQ7YnHuRpToLU55deQocSVlZ6REhtby1ZX0oxMjhNcnRuZGdHSy1lSnd4QXAyQnJ6RDRwbHFPNll3RmIxa3B6anM1TUhFQnFOZUtWcXZjd0lWdWI5UzluQ1JrSk1yamVXNC1tR253IIEC',
    'bili_jct': '0cc379a57bd523dbd7567cfec319bb52',
    'sid': '85jopfcu',
    'bp_t_offset_290041701': '975928921700696064',
    'b_lsid': '1053F1F104_191E181CC7C',
}


wts = int(time.time())

from urllib.parse import quote

# pagination_str = '""'


def get_w_rid(wts, pagination_str):
    a = 'ea1db124af3c7062474693fa704f4ff8'
    pagination_str = quote(f'{{"offset":{pagination_str}}}')
    # print(pagination_str)
    l = [
        "mode=3",
        "oid=1255942505",
        f"pagination_str={pagination_str}",
        "plat=1",
        "seek_rpid=",
        "type=1",
        "web_location=1315875",
        f"wts={wts}"
    ]
    y = '&'.join(l)
    string = y + a
    # print(l)
    # print(y)
    MD5 = hashlib.md5()
    MD5.update(string.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid


def get_source_page(url, pagination_str):
    w_rid = get_w_rid(wts, pagination_str)
    params = {"oid": "1255942505",
              "type": "1",
              "mode": "3",
              "pagination_str": f'{{"offset":{pagination_str}}}',
              "plat": "1",
              "seek_rpid": '',
              "web_location": "1315875",
              "w_rid": w_rid,
              "wts": wts}
    # print(params)
    response = requests.get(url=url, headers=headers, cookies=cookies, params=params)
    data = response.json()
    try:
        nextpage = data['data']['cursor']['pagination_reply']['next_offset']
        nextpage_parmas = json.dumps(nextpage)  # 字符串转换为字典
        return data,nextpage_parmas
    except KeyError as e:
        return None, None


def parse_data(data):
    total = []
    reply_list = data['data']["replies"]
    try:
        reply_top = data['data']['top']
        dic_top = {'昵称': reply_top["upper"]['member']['uname'],
                   'comment': reply_top["upper"]['content']['message']}
        total.append(dic_top)
    except Exception as e:
        print(f'Error: {e}')
    for reply in reply_list:
        dic = {
            "昵称": reply['member']['uname'],
            "comment": reply['content']['message']
        }
        total.append(dic)
    return total

#
# def main(url,params):
#     data,parmas = get_source_page(url,params)
#     page_comment = parse_data(data)
#     return page_comment





if __name__ == '__main__':
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main?'
    list1 = []
    parmas = '""'
    for x in range(5):
        data,parmas = get_source_page(url,pagination_str=parmas)
        if data:
            page_comment = parse_data(data)
            list1.extend(page_comment)
        else:
            break
    for i in list1:
        print(i)

