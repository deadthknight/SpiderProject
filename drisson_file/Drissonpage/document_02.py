# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
# from DrissionPage import SessionPage
# page = SessionPage()
# page.get('demo.html')
# div1 = page.ele('#one')  # 获取 id 为 one 的元素
# p1 = page.ele('@name=row1')  # 获取 name 属性为 row1 的元素
# div2 = page.ele('第二个div')  # 获取包含“第二个div”文本的元素
# div_list = page.eles('tag:div')  # 获取所有div元素
#
# print(div1)
# print(p1.text)
# print(div2)
# print(div_list)

from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://www.baidu.com')
eles = page('#s-top-left').eles('t:a')  # 获取左上角导航栏内所有<a>元素
# for ele in eles.filter.displayed():  # 筛选出显示的元素列表并逐个打印文本
#     print(ele.text, end=' ')
ele = eles.filter_one(1).text('图')  # 获取第二个文本带有“图”字的元素
print(ele.text)