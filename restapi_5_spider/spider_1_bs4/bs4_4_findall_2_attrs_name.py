 #!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


from part1_restapi.restapi_5_spider.spider_1_bs4.bs4_1_get_soup import qytang_soup
import re

# find_all( name , attrs , recursive , text , **kwargs )
# find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
# 注意：如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索,如果包含一个名字为 id 的参数,Beautiful Soup会搜索每个tag的”id”属性


# 一号方案,传方法, 这种方法可以用于判断是否有相应的属性
# def has_class_but_no_id(tag):
#     return tag.has_attr('class') and not tag.has_attr('id') and \
#            not tag.has_attr('href') and \
#            tag.has_attr('data-sku') and \
#            tag.get('data-sku').startswith('10006') and tag.name == 'li'
#
#
# for a in qytang_soup.find_all(has_class_but_no_id):
#     print(a.attrs)


# 二号方案: 基于属性的名字, 多个属性的时候可以使用字典
# 严重注意class需要使用class_!!!

# print(qytang_soup.find('ul', class_="gl-warp clearfix"))
# print(qytang_soup.find_all('li', class_="gl-item"))

# 找产品信息，支持一级一级的查找 先找到find('ul', class_="gl-warp clearfix")，再找到find_all('li', class_="gl-item")
for item_card in qytang_soup.find('ul', class_="gl-warp clearfix").find_all('li', class_="gl-item"):
    # 找到产品的文本介绍
    print(item_card.find('div', class_="p-name p-name-type-2").find('em').text)
    # 找到产品的价格
    print(item_card.find('div', class_="p-price").find('i').text)
    # 找大图
    print(item_card.find('div', class_="p-img").find('a').find('img').get('data-lazy-img'))


# 三号方案: 基于属性的正则表达式匹配
# print(qytang_soup.find_all('a', href=re.compile(r"jd\.com")))
# print(len(qytang_soup.find_all('a', href=re.compile(r"jd\.com"))))
# 可以同时对多个属性进行正则表达式匹配
# print(qytang_soup.find_all(href=re.compile(r"jd\.com"), rel=re.compile("dns")))


# 有些tag属性在搜索不能使用,例如HTML5中的data-*属性
# data-name="search"
# print(qytang_soup.find_all(data-name="search")) 报错SyntaxError: keyword can't be an expression
# 需要使用如下方式来查找data-*属性
# print(qytang_soup.find_all('div', attrs={"class": "dorpdown", "data-type": "default"}))
