# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from lxml import etree
from readheader import readheaders
import os
from urllib.parse import urlparse
from time_decorater import run_time

headers = readheaders('./header_code.txt')


def get_url_list():
    # print(headers)
    url = 'https://chowluking.com/codes'
    # # 打印解析后的各个部分
    # print("scheme:", parsed_url.scheme)           # URL scheme (e.g. http or https)
    # print("netloc:", parsed_url.netloc)           # Network location (e.g. video.pearvideo.com)
    # print("path:", parsed_url.path)               # Hierarchical path (e.g. /mp4/short/20240524/1716776652507-16029373-hd.mp4)
    # print("params:", parsed_url.params)           # Parameters for the last path element
    # print("query:", parsed_url.query)             # Query component (e.g. token=123456789&expires=1716776652507)
    # print("fragment:", parsed_url.fragment)       # Fragment identifier
    # print("username:", parsed_url.username)       # User name
    # print("password:", parsed_url.password)       # Password
    # print("hostname:", parsed_url.hostname)       # Hostname (lower case)
    # print("port:", parsed_url.port)               # Port number
    response = requests.get(url=url, headers=headers).json()

    json_data = response['data']

    name_list = []
    download_url_list = []
    if not os.path.exists('./files'):
        os.mkdir('./files')
    for name in json_data:
        name_list.append(name['name'])
        filename = name['name']
        download_url = 'https://chowluking.com/code/' + filename
        download_url_list.append(download_url)
    return download_url_list


def download_file(download_url):
    parsed_url = urlparse(download_url)
    file_name = os.path.basename(parsed_url.path)
    filepath = './files/' + file_name
    download_file_origin = requests.get(download_url, headers=headers)

    if download_file_origin.status_code == 200:
        # 判断文件后缀并选择合适的写入模式
        try:
            if file_name.endswith('.py'):
                mode = 'w'  # 文本模式
                tree = etree.HTML(download_file_origin.text)
                download_file = tree.xpath('//code[@class="python"]//text()')[0]
                content = download_file
            elif file_name.endswith('.rar') or file_name.endswith('.apk'):
                mode = 'wb'  # 二进制模式
                content = download_file_origin.content
            elif file_name.endswith('.js'):
                mode = 'w'  # 文本模式
                content = download_file_origin.text
            with open(filepath, mode) as file:
                file.write(content)
            print(f"文件 '{file_name}' 下载成功.")
        except Exception as e:
            print(e)

    else:
        print(f"下载失败: {download_file_origin.status_code}")


if __name__ == "__main__":
    # pass
    from multiprocessing.dummy import Pool
    import time

    pool = Pool(30)
    t1 = time.time()
    pool.map(download_file, get_url_list())
    print("全部下载完毕！！！")
    t2 = time.time()
    print('本次操作时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
    # #514秒

# 测试js文件
# download_url = 'https://chowluking.com/code/stealth.min.js'
# parsed_url = urlparse(download_url)
# file_name = os.path.basename(parsed_url.path)
# filepath = './files/' + file_name
# download_file_orgin = requests.get(download_url, headers=headers)
# with open(filepath, 'w') as file:
#     file.write(download_file_orgin.text)

# 统计文件数量
#     sum_count = {'py': 0, 'rar': 0, 'js': 0}
#     lists = get_url_list()
#     for list in lists:
#         parsed_url = urlparse(list)
#         file_name = os.path.basename(parsed_url.path)
#         if file_name.endswith('.py'):
#             sum_count['py']+=1
#         elif file_name.endswith('.rar'):
#             sum_count['rar'] += 1
#         elif file_name.endswith('.js'):
#             sum_count['js'] += 1
#     print(sum_count)
#     print(len(lists))
