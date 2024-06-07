#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By

# 创建 WebDriver 对象
wd = webdriver.Chrome()

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
wd.get('https://www.byhy.net/_files/stock1.html')

# 根据id选择元素，返回的就是该元素对应的WebElement对象
element = wd.find_element(By.ID, 'kw')

# 通过该 WebElement对象，就可以对页面元素进行操作了
# 比如输入字符串到 这个 输入框里
element.send_keys('通讯\n')

# 根据class属性 elements 所有返回的是列表 element返回的是一个元素
wd.find_elements(By.CLASS_NAME, 'animal')

# 有 多个class类型 ，多个class类型的值之间用 空格 隔开，比如
#
#
# <span class="chinese student">张三</span>
# 注意，这里 span元素 有两个class属性，分别 是 chinese 和 student， 而不是一个 名为 chinese student 的属性。
#
# 我们要用代码选择这个元素，可以指定任意一个class 属性值，都可以选择到这个元素，如下
# element = wd.find_elements(By.CLASS_NAME,'chinese')
# 或者
# element = wd.find_elements(By.CLASS_NAME,'student')


# 根据 tag name 选择元素，返回的是 一个列表
# 里面 都是 tag 名为 div 的元素对应的 WebElement对象
# elements = wd.find_elements(By.TAG_NAME, 'div')
#
# # 取出列表中的每个 WebElement对象，打印出其text属性的值
# # text属性就是该 WebElement对象对应的元素在网页中的文本内容
# for element in elements:
#     print(element.text)


# 使用 find_elements 选择的是符合条件的 所有 元素， 如果没有符合条件的元素， 返回空列表
#
# 使用 find_element 选择的是符合条件的 第一个 元素， 如果没有符合条件的元素， 抛出 NoSuchElementException 异常
if __name__ == "__main__":
    pass
