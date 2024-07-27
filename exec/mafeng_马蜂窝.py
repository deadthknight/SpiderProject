# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
import time
from urllib.parse import urljoin
from readheader import readheaders

headers = readheaders('../http_header.txt')
def get_page_source(url):
    for x in range(1,25):
        try:
            params = {"act": "GetContentList",
                      "s_dept_time[]": "all",
                      "price[]": "all",
                      "from": "NaN",
                      "kw": '',
                      "to": "M10765P日本",
                      "salesType": "NaN",
                      "page": f"{x}",
                      "group": "1",
                      "sort": "smart",
                      "sort_type": "desc",
                      "limit": "20"}
            response = requests.get(url=url,  headers=headers, params=params)
            response.raise_for_status()
            # 自动检测：chardet 可以自动检测字节流的编码，确保我们能够正确解码网页内容
            # response.encoding = chardet.detect(response.content)['encoding']
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取失败：{e}")


def join(data):
    return ''.join(data).strip()
def parse_data(url,pg_source):
    # item_list = pg_source["html"]  #get比较好
    item_list = pg_source.get("html", "")
    tree = etree.HTML(item_list)
    items = tree.xpath('//a')
    lst = []
    for item in items:
        url_part = item.xpath('.//@href')
        url_final = urljoin(url,join(url_part))
        title = item.xpath('.//div[@class="detail"]//h3/text()')
        price = item.xpath('.//span[@class="price"]/strong/text()')
        dic = {"url" : url_final,
               "title": join(title),
               "price": join(price)}
        lst.append(dic)
    return lst




def main():
    url = 'https://www.mafengwo.cn/sales/ajax_2017.php?'
    pg_source = get_page_source(url)
    data = parse_data(url,pg_source)
    print(len(data))


if __name__ == '__main__':
    main()
