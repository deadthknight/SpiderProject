#!/usr/bin/env Python3.11
# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def search(key):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    wd = webdriver.Chrome(service=Service(r'/Users/vickyyang/Desktop/study/chromedriver-mac-x64/chromedriver'),
                          options=chrome_options)

    try:
        # 隐式等待
        wd.implicitly_wait(10)
        wd.get('https://dytt.dytt8.net/index.htm')

        element = wd.find_element(By.CLASS_NAME, 'formhue')
        element.clear()
        element.send_keys(key)
        # 发送回车
        element.send_keys(Keys.RETURN)

        finally_list = []
        while True:
            elements = wd.find_elements(By.XPATH, '//table[@border="0" and @width="100%"]//a')
            if elements:
                for element in elements:
                    try:
                        href = element.get_attribute('href')
                        title = element.text
                        if key in title:
                            final = {'Title': title, 'Link': href}
                            finally_list.append(final)
                    except Exception:
                        continue  # 如果发生异常，继续处理下一个元素

            try:
                # 查找“下一页”链接
                next_page_element = wd.find_element(By.LINK_TEXT, '下一页')
                if next_page_element and next_page_element.is_enabled():
                    next_page_element.click()
                    time.sleep(3)  # 等待页面加载
                    wd.switch_to.window(wd.window_handles[-1])
                else:
                    break  # 如果没有找到下一页链接或者不可点击，退出循环
            except Exception:
                break  # 如果发生异常，退出循环

        return finally_list if finally_list else '没有找到相关电影'
    finally:
        wd.quit()  # 确保正确关闭浏览器


if __name__ == '__main__':
    key = input('请输入查询电影的名称：')
    results = search(key)
    for result in results:
        print(result)
