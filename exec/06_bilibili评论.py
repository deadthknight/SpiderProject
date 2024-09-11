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
    'fingerprint': 'f7a5c2aff4d77f79ac67ec5f434805d7',
    'buvid_fp': 'f7a5c2aff4d77f79ac67ec5f434805d7',
    'CURRENT_QUALITY': '80',
    'SESSDATA': '9aa74e6f%2C1741350309%2C2b2ec%2A91CjAFBaJ9-IYWbr9hQ-lb1W0QZJSc-rcw-q8r31aWoq13Kq01_D_AgFp0SkTUB9UCgkUSVlFOUTFMbnpzeF93WHhGY2FvWmV0ekdVTjNkQzY1Q2t0VEFsdjVmNHdlUDR2eV9iTjhocFl0X0ZEVlBPaWtSNndDeVNNUlYyQjlJQnBCNW5hR0htT2N3IIEC',
    'bili_jct': 'a4c4ef3ae5514423920bcbce10a27b41',
    'home_feed_column': '5',
    'sid': '89qo3pho',
    'CURRENT_FNVAL': '4048',
    'bp_t_offset_290041701': '975197974101491712',
    'b_lsid': 'F77813FF_191DC36E8D9',
    'browser_resolution': '1920-875',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjYyMzcxMTMsImlhdCI6MTcyNTk3Nzg1MywicGx0IjotMX0.vRu0jrVxts27p8ly95fRCBCO17DQ3I9WTYYbe91FCP4',
    'bili_ticket_expires': '1726237053',
}

wts = int(time.time())

from urllib.parse import quote

pagination_str = '""'


def get_w_rid(wts, pagination_str):
    a = 'ea1db124af3c7062474693fa704f4ff8'

    pagination_str = quote(f'{{"offset":{pagination_str}}}')
    print(pagination_str)
    l = [
        "mode=3",
        "oid=113114305594915",
        f"pagination_str= {pagination_str}",
        "plat=1",
        "seek_rpid=",
        "type=1",
        "web_location=1315875",
        f"wts={wts}"
    ]
    y = '&'.join(l)
    string = y + a
    print(l)
    # print(y)
    MD5 = hashlib.md5()
    MD5.update(string.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid
get_w_rid(wts,pagination_str)

def get_source_page(url, pagination_str):
    w_rid = get_w_rid(wts, pagination_str)
    params = {"oid": "113114305594915",
              "type": "1",
              "mode": "3",
              "pagination_str": f'{pagination_str}',
              "plat": "1",
              "seek_rpid": '',
              "web_location": "1315875",
              "w_rid": w_rid,
              "wts": wts}
    response = requests.get(url=url, headers=headers, cookies=cookies, params=params)
    data = response.json()
    nextpage = data['data']['cursor']['pagination_reply']['next_offset']
    nextpage_parmas = json.dumps(nextpage)

    return data,nextpage_parmas


def parse_data(data):
    total = []
    reply_list = data['data']["replies"]
    reply_top = data['data']['top']
    dic_top = {'昵称': reply_top["upper"]['member']['uname'],
               'comment': reply_top["upper"]['content']['message']}
    total.append(dic_top)
    for reply in reply_list:
        dic = {
            "昵称": reply['member']['uname'],
            "comment": reply['content']['message']
        }
        total.append(dic)
    return total


def main(url,params):
    data,nextpage_parmas = get_source_page(url,params)
    page_comment = parse_data(data)
    print(page_comment)
    params = nextpage_parmas



if __name__ == '__main__':
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    # params = '{"offset":""}'
    # main(url,params)
    # for x in range(5):
    #     main(x,params)
