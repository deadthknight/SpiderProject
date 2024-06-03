#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome(service=Service(r'f:\Python\tool\chromedriver-win64\chromedriver.exe'))

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
# wd.get('https://www.baidu.com')
#
# element = wd.find_element(By.ID, 'kw')
# element.send_keys('天气')
#
# element = wd.find_element(By.ID, 'su')
# element.click()
# 程序运行完会自动关闭浏览器，就是很多人说的闪退
# 这里加入等待用户输入，防止闪退
# input('等待回车键结束程序')

if __name__ == "__main__":
    # https: // www.byhy.net / auto / selenium / 02 /
    # 根据 class属性 选择元素
    # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
    wd.get('https://cdn2.byhy.net/files/selenium/sample1.html')

    # elements = wd.find_elements(By.CLASS_NAME, 'animal')
    # for element in elements:
    #     print (element.text)
    elements = wd.find_elements(By.TAG_NAME,'div')

    # 程序运行完会自动关闭浏览器，就是很多人说的闪退
    # 这里加入等待用户输入，防止闪退
    input('等待回车键结束程序')

