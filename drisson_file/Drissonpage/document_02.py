# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import SessionPage
page = SessionPage()
page.get('demo.html')
div1 = page.ele('#one')  # 获取 id 为 one 的元素
p1 = page.ele('@name=row1')  # 获取 name 属性为 row1 的元素
div2 = page.ele('第二个div')  # 获取包含“第二个div”文本的元素
div_list = page.eles('tag:div')  # 获取所有div元素
div3 = page.eles('@!name="row1"')
#
# print(div1.text)
print('test========================================')
test = page('第一行').attr('name')   #文本是第一行的name的属性
print(test)
print('test1=======================================')
test1 = page('@@class=p_cls@@name=row2').text            #属性class=p_cls和name=row2
print(test1)
print('test2=======================================')
test2 = page(('@@class=p_cls@!name=row1')).text          #class=p_cls且name不等于row1
print(test2)
print('test3=======================================')
test3 = page.eles(('@|class=p_cls4@|id=two'))            #class=p_cls或者id=two
for x in test3:
    print(x.text)
print('test4=======================================')
test4 = page('.$4').text                                #class以4结尾
print(test4)
# print('==============')
# print(p1.text)
# print('==============')
# print(div2.text)
# print('==============')
# for x in div3:
#     print(x.text)
#     print('==============')
# print(div_list)

# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get('https://www.baidu.com')
# eles = page('#s-top-left').eles('t:a')  # 获取左上角导航栏内所有<a>元素
# # for ele in eles.filter.displayed():  # 筛选出显示的元素列表并逐个打印文本
# #     print(ele.text, end=' ')
# ele = eles.filter_one(1).text('图')  # 获取第二个文本带有“图”字的元素
# print(ele.text)