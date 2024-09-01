# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式
co.set_argument('--start-maximized')
page = ChromiumPage(co)
# page.listen.start()
# page.get(
#     'https://ygp.gdzwfw.gov.cn/#/44/new/jygg/v3/A?'
#     'noticeId=52cd39dd-7015-46fb-8072-a088d1bcb8b1&projectCode=E4401000002400710001&bizCode='
#     '3C31&siteCode=440100&publishDate=20240312173004&source='
#     '%E5%B9%BF%E4%BA%A4%E6%98%93%E6%95%B0%E5%AD%97%E4%BA%A4%E6%98%93%E5%B9%B3%E5%8F%B0&titleDetails='
#     '%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&classify=A02&nodeId=1823240830880374785')
# for i in range(100):
#     response = page.listen.wait()
#     print('监听的数据包', response.url)  # 监听所有数据包

page.listen.start('detail?')  # 默认不启动正则匹配，这里是url包含该字符串，启动正则需要配置 is_regex=True
page.get(
    'https://ygp.gdzwfw.gov.cn/#/44/new/jygg/v3/A?'
    'noticeId=52cd39dd-7015-46fb-8072-a088d1bcb8b1&projectCode=E4401000002400710001&bizCode='
    '3C31&siteCode=440100&publishDate=20240312173004&source='
    '%E5%B9%BF%E4%BA%A4%E6%98%93%E6%95%B0%E5%AD%97%E4%BA%A4%E6%98%93%E5%B9%B3%E5%8F%B0&titleDetails='
    '%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&classify=A02&nodeId=1823240830880374785')
data_packet = page.listen.wait()
# print('监听的数据包url', data_packet.url) # 监听到符合正则的数据包
# print('监听数据包方法', data_packet.method)
# print('监听数据包响应', data_packet.response.body)
# print('监听数据包响应头', data_packet.response.headers)
# print('监听数据包请求头', data_packet.request.headers)
title = data_packet.response.body["data"]["title"]
info_list = data_packet.response.body["data"]["tradingNoticeColumnModelList"][1]["tradingNoticeTableColumnModel"]["dataList"]
print(title)
for info in info_list:
    print(info["bidderName"])
    print(info["bidManager"])
    print('======================')