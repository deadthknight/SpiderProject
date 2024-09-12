#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import time
import requests
import csv
import hashlib
import json
from loguru import logger
from urllib.parse import quote

headers = {
    'origin': 'https://www.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

cookies = {
    'buvid3': '0CDC8525-298A-FE4E-2D04-8EEE36AE0A5906152infoc',
    'b_nut': '1717464006',
    'CURRENT_FNVAL': '4048',
    '_uuid': '6E33273C-93AF-FECF-DD1A-2CD5471055A3405632infoc',
    'buvid_fp': '98c0a2c76d42f2f315231b1ee382feae',
    'buvid4': 'AA0008A4-F8E7-B4D3-2CA1-56A5359BCBF407069-024060401-AilUHu3jf1pP%2Be1Bw0zL1w%3D%3D',
    'rpdid': "|(u~)|)YYR)~0J'u~u~RYR||~",
    'enable_web_push': 'DISABLE',
    'header_theme_version': 'CLOSE',
    'home_feed_column': '5',
    'DedeUserID': '290041701',
    'DedeUserID__ckMd5': '08a0369c598f5324',
    'b_lsid': '1438B536_191E3DB86E2',
    'browser_resolution': '2048-1027',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjYzNjM5MDIsImlhdCI6MTcyNjEwNDY0MiwicGx0IjotMX0.5EuxGHXZsf0d-dZ-WbjCpzPgthguL9pMm70JpA60YKo',
    'bili_ticket_expires': '1726363842',
    'SESSDATA': '94f87b51%2C1741656746%2Cc8508%2A91CjDkSAGdOFMeyeM0gleEAzZCVAEV-oho5aFIK6tCOD-5CRgQht37Zdaz4rnVragSx2cSVjRhOUpscFV0eXdqdzl2RldkQndEMjUwYjdBblBONDJOUmpCR1RFLVhSZnlqbmdFSXhySDlRamZmaGhCamJVY3g5V3drUjNEOUF5bmo4c0ZtblZJaktnIIEC',
    'bili_jct': '4bf888217a220a4bbb3d44c42c5599fc',
    'sid': '7a7ykxli',
}


# 获取 w_rid 值
def get_w_rid(wts, oid, pagination_str):
    a = 'ea1db124af3c7062474693fa704f4ff8'
    pagination_str = quote(f'{{"offset":{pagination_str}}}')
    l = [
        "mode=3",
        f"oid={oid}",
        f"pagination_str={pagination_str}",
        "plat=1",
        "seek_rpid=",
        "type=1",
        "web_location=1315875",
        f"wts={wts}"
    ]
    y = '&'.join(l)
    string = y + a
    MD5 = hashlib.md5()
    MD5.update(string.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid


# 获取页面数据
def get_source_page(url, oid, pagination_str):
    wts = int(time.time())
    w_rid = get_w_rid(wts, oid=oid, pagination_str=pagination_str)
    params = {
        "oid": f"{oid}",
        "type": "1",
        "mode": "3",
        "pagination_str": f'{{"offset":{pagination_str}}}',
        "plat": "1",
        "seek_rpid": '',
        "web_location": "1315875",
        "w_rid": w_rid,
        "wts": wts
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()  # 如果状态码不是200，抛出异常
        data = response.json()
        nextpage = data['data']['cursor']['pagination_reply']['next_offset']
        nextpage_params = json.dumps(nextpage)
        return data, nextpage_params
    except Exception as e:
        logger.error(f"Request error: {e}")
    except KeyError as e:
        logger.error(f"KeyError: {e}")
    return None, None


# 解析数据
def parse_data(data):
    total = []
    try:
        reply_top = data['data']['top']
        dic_top = {'昵称': reply_top["upper"]['member']['uname'],
                   '评论': reply_top["upper"]['content']['message']}
        total.append(dic_top)
    except KeyError:
        logger.info("No top reply found.")
    try:
        reply_list = data['data']["replies"]
        for reply in reply_list:
            dic = {
                "昵称": reply['member']['uname'],
                "评论": reply['content']['message']
            }
            total.append(dic)
    except KeyError as e:
        logger.error(f"KeyError in parse_data: {e}")
    return total


# 将数据写入CSV
def write_to_csv(data_list, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file: # encoding='utf-8' 打开乱码就sig
        writer = csv.DictWriter(file, fieldnames=['昵称', '评论'])
        writer.writeheader()
        writer.writerows(data_list)
    logger.info(f"数据写入 {csv_file}")


def main(url, oid, max_pages=5, csv_file="output.csv"):
    pagination_str = '""'
    data_list = []
    for page in range(max_pages):
        logger.info(f'抓取第{page+1}页')
        data, pagination_str = get_source_page(url, oid=oid, pagination_str=pagination_str)
        if data:
            page_comment = parse_data(data)
            data_list.extend(page_comment)
            logger.info(f"第 {page + 1} 抓取完成, 数据量为: {len(data_list)}个")
        else:
            logger.info("没有其他数据了")
            break
    for page in data_list:
        print(page)
    # 将数据写入CSV文件
    # if data_list:
    #     write_to_csv(data_list, csv_file)
    #     logger.info("写入完成。。。")

if __name__ == "__main__":
    oid = 113091136258502
    url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
    main(url=url, oid=oid, max_pages=3)
