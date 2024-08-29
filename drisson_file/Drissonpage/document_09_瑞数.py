from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
import re
# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式

page = ChromiumPage(co)

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
page.listen.start('jsp/zdsswfaj/wwquery')
page.get('http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp')
page('tx=东城').click()
page.listen.wait()
previous_data = []  # 用于存储前一页的数据
n=1
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
for packet in page.listen.steps():              # 会监听wwquery.jsp 和 wwquery 2个数据包，一个是GET请求，一个是POST请求。
    # 此方法返回一个可迭代对象，用于for循环，每次循环可从中获取到的数据包。
    if packet.method == 'POST':
        res_text = packet.response.body
        iframe = etree.HTML(res_text)
        tr_list = iframe.xpath('//tbody//td/table[2]//tr')[:-1]
        page_max = page('tx:查询结果').text
        num = re.search(r'/(?P<max>.*)',page_max)
        # print(num.group('max'))
        num = int(num.group('max'))
        print(f"第{n}页")
        for tr in tr_list:
            area = tr.xpath('./td[1]/text()')[0]
            company = tr.xpath('./td[2]/text()')[0]
            problem = tr.xpath('./td[4]/text()')[0]
            print(area,company,problem)
        # 更新 previous_tr_list
        if n == num :
            print('到最后一页，结束。。。。。。。')
            break
        n += 1
        page('下一页').click()
    elif packet.method == 'GET':
        print('不需要')
page.close()

