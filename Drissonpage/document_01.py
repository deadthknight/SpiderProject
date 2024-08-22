# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get('http://DrissionPage.cn')


# from DrissionPage import SessionPage
#
# # 创建页面对象
# page = SessionPage()
#
# # 爬取3页
# for i in range(1, 4):
#     # 访问某一页的网页
#     page.get(f'https://gitee.com/explore/all?page={i}')
#     # 获取所有开源库<a>元素列表
#     links = page.eles('.title project-namespace-path')
#     # 遍历所有<a>元素
#     for link in links:
#         # 打印链接信息
#         print(link.text, link.link)

from DrissionPage import WebPage

# 创建页面对象
page = WebPage()
# 访问网址
page.get('https://gitee.com/explore/all')
# 切换到收发数据包模式
page.change_mode()
# 获取所有行元素
items = page.ele('.ui relaxed divided items explore-repo__list').eles('.item')
# 遍历获取到的元素
for item in items:
    # 打印元素文本
    print(item('t:h3').text)
    print(item('.project-desc mb-1').text)
    print()