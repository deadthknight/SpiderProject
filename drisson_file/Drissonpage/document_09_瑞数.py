# from DrissionPage import ChromiumPage, ChromiumOptions
# from lxml import etree
# import re
# # 配置 ChromiumOptions
# co = ChromiumOptions()
# co.headless(False)  # 不使用无头模式
# co.incognito(True)  # 使用无痕模式
#
# page = ChromiumPage(co)

# 过瑞数mvp反爬 1、渲染方式 拿到html 2、监听数据包 3、接口的方式（只读取cookies）
# 方法1
# page.get('http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp')
# page('tx=东城').click()
# page.wait(1, 3)
# # iframe = page.get_frame('#rightiframe')     #在iframe里面
# iframe = page('#rightiframe')
# # print(iframe.html)
# tree = etree.HTML(iframe.html)  # type: etree._Element
# tr_list = tree.xpath('//tbody//td/table[2]//tr')[:-1]
# for tr in tr_list:
#     area = tr.xpath('./td[1]/text()')[0]
#     company = tr.xpath('./td[2]/text()')[0]
#     problem = tr.xpath('./td[4]/text()')[0]
#     print(area,company,problem)

#方法二：监听数据包
# page.listen.start('jsp/zdsswfaj/wwquery')
# page.get('http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp')
# page('tx=东城').click()
# page.listen.wait()
# previous_data = []  # 用于存储前一页的数据
# n=1
# # 判断最后的数据跟之前是否相同而终止
# for packet in page.listen.steps():              # 会监听wwquery.jsp 和 wwquery 2个数据包，一个是GET请求，一个是POST请求。
#     # 此方法返回一个可迭代对象，用于for循环，每次循环可从中获取到的数据包。
#     print("开始")
#     if packet.method == 'POST':
#         res_text = packet.response.body
#         iframe = etree.HTML(res_text)
#         tr_list = iframe.xpath('//tbody//td/table[2]//tr')[:-1]
#         # page_max = page('tx:查询结果').text
#         # num = re.search(r'/(?P<max>.*)',page_max)
#         # print(num.group('max'))
#         # num = int(num.group('max'))
#         tr_list_last = tr_list[-1]
#         tr_list_last_data = ''.join(tr_list_last.xpath('.//text()')).strip()
#         print('最后的数据', tr_list_last_data)
#         if tr_list_last_data == previous_data:
#             print("已到达最后一页，停止操作。")
#             break
#         print(f"第{n}页")
#         for tr in tr_list:
#             area = tr.xpath('./td[1]/text()')[0]
#             company = tr.xpath('./td[2]/text()')[0]
#             problem = tr.xpath('./td[4]/text()')[0]
#             print(area,company,problem)
#         n+=1
#         # 更新 previous_tr_list
#         previous_data = tr_list_last_data
#         page('下一页').click()
#     elif packet.method == 'GET':
#         print('不需要')
# page.close()
# for packet in page.listen.steps():              # 会监听wwquery.jsp 和 wwquery 2个数据包，一个是GET请求，一个是POST请求。
#     # 此方法返回一个可迭代对象，用于for循环，每次循环可从中获取到的数据包。
#     if packet.method == 'POST':
#         res_text = packet.response.body
#         iframe = etree.HTML(res_text)
#         tr_list = iframe.xpath('//tbody//td/table[2]//tr')[:-1]
#         page_max = page('tx:查询结果').text
#         num = re.search(r'/(?P<max>.*)',page_max)
#         # print(num.group('max'))
#         num = int(num.group('max'))
#         print(f"第{n}页")
#         for tr in tr_list:
#             area = tr.xpath('./td[1]/text()')[0]
#             company = tr.xpath('./td[2]/text()')[0]
#             problem = tr.xpath('./td[4]/text()')[0]
#             print(area,company,problem)
#         # 更新 previous_tr_list
#         if n == num :
#             print('到最后一页，结束。。。。。。。')
#             break
#         n += 1
#         page('下一页').click()
#     elif packet.method == 'GET':
#         print('不需要')
# page.close()

# 方法三：
from DrissionPage import WebPage, ChromiumOptions
import requests
from lxml import etree

co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式
page = WebPage('d', chromium_options=co)
page.get('http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp', retry=3, interval=2, timeout=15)
# print('======>cookies', page.cookies(as_dict=True))
browser_cookies = page.cookies(as_dict=True)
# print('======>VIP9lLgDcAL2T', browser_cookies['VIP9lLgDcAL2T'])
# print('======>VIP9lLgDcAL2S',browser_cookies['VIP9lLgDcAL2S'])   #瑞数反爬
# page.refresh()
# browser_cookies = page.cookies(as_dict=True)
# print('======>VIP9lLgDcAL2T', browser_cookies['VIP9lLgDcAL2T'])  #网页刷新/点击/超时都会刷新cookies
# print('======>VIP9lLgDcAL2S',browser_cookies['VIP9lLgDcAL2S'])

for pages in range(1,11):
    url = 'http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
               "Cookie": f"VIP9lLgDcAL2T={browser_cookies['VIP9lLgDcAL2T']}; VIP9lLgDcAL2S={browser_cookies['VIP9lLgDcAL2S']};"}
    data = {"orgCode": "11100000000",
            "bz": "dq",
            "dq":"东城",
            "dqy": f"{pages}"}
    # response = requests.post(url=url,headers=headers,data=data)  #cookies 会失效
    # for key, value in response.request.headers.items():      #不是发送全部cookies
    #     print(f"{key}: {value}")
    # print(response.status_code)
    # print(page.cookies())
    max_retries = 3  # 最大重试次数
    for attempt in range(max_retries):
        response = requests.post(url=url, headers=headers, data=data)
        if response.status_code != 200:
            page.refresh()  # 刷新页面
            browser_cookies = page.cookies(as_dict=True)  # 更新cookies
            headers[
                'Cookie'] = f"VIP9lLgDcAL2T={browser_cookies['VIP9lLgDcAL2T']}; VIP9lLgDcAL2S={browser_cookies['VIP9lLgDcAL2S']};"
            print(f"重试第 {attempt + 1} 次，当前页面: {pages}")
        else:
            break
    else:
        # 如果达到最大重试次数，仍然无法成功获取响应，跳过该页
        print(f"第 {pages} 页请求失败，跳过。")
        continue

    print(f'第 {pages} 页')
    tree = etree.HTML(response.text)
    tr_list = tree.xpath('//tbody//td/table[2]//tr')[:-1]
    for tr in tr_list:
        area = tr.xpath('./td[1]/text()')[0]
        company = tr.xpath('./td[2]/text()')[0]
        problem = tr.xpath('./td[4]/text()')[0]
        print(area, company, problem)

