# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import SessionPage
page = SessionPage()
page.get('demo.html')
div1 = page.ele('#one')  # 获取 id 为 one 的元素
p1 = page.ele('@name=row1')  # 获取 name 属性为 row1 的元素
div2 = page.ele('第二个div')  # 获取包含“第二个div”文本的元素
div_list = page.eles('tag:div')  # 获取所有div元素

print(div1)
print(p1.text)
print(div2)
print(div_list)