# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import time

import requests
import csv
# 创建csv
f = open(file='comment.csv', mode='w',encoding='utf-8',newline='')  #创建文件
# 字典写入
csv_writer = csv.DictWriter(f, fieldnames=['昵称', 'comment'])
# 写入表头
csv_writer.writeheader() 

headers = {
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/video/BV1NopHe9Eaw/?spm_id_from=333.337.search-card.all.click&vd_source=30cafa8600362cdbc4203bf0b5bb2903',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
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


wts = int(time.time())*1000   #时间戳

o = 'ea1db124af3c7062474693fa704f4ff8'

params = {"oid": "113109373030327",
          "type": "1",
          "mode": "3",
          "pagination_str": '{"offset":""}',
          "plat": "1",
          "seek_rpid": '',
          "web_location": "1315875",
          "w_rid": "4b02c771880af912f50c6f29e0d0d085",
          "wts": '1725981085'}


def get_source_page(url):
    response = requests.get(url=url,headers=headers,cookies=cookies,params=params)
    print(response.status_code)
    return response.json()

def main(url):
    res = get_source_page(url)
    list1 = []
    reply_list = res['data']["replies"]
    for reply in reply_list:
        dic = {
               "昵称": reply['member']['uname'],
               "comment":reply['content']['message']
        }
        print(dic)
        # csv_writer.writerow(dic)


if __name__ == '__main__':
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    main(url)

