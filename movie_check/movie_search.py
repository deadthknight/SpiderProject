# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def search(key):
    wd = webdriver.Chrome(service=Service(r'/Users/vickyyang/Desktop/study/chromedriver-mac-x64/chromedriver'))
    #隐式等待
    wd.implicitly_wait(10)
    wd.get('https://dytt.dytt8.net/index.htm')
    # mainWindow变量保存当前窗口的句柄
    mainWindow = wd.current_window_handle
    element = wd.find_element(By.CLASS_NAME, 'formhue')
    element.clear()
    element.send_keys(key)
    # 发送回车
    element.send_keys(Keys.RETURN)
    finally_list = []
    elements = wd.find_elements(By.XPATH, '//ul/table[@border="0" and @width="100%"]')
    if elements:
        for element in elements:
            try:
                # 在每一个 tbody 元素内查找 a 标签
                a_tag = element.find_element(By.TAG_NAME, 'a')

                href = a_tag.get_attribute('href')
                title = a_tag.text
                if key in title:
                    final = {'Title': title,
                             'Link': href
                             }
                    finally_list.append(final)
            except Exception as e:
                continue  #

        while True:
            try:
                # WebDriver在当前页面中查找一个链接文本为“下一页”的链接元素。
                next_page_element = wd.find_element(By.LINK_TEXT, '下一页')
                # next_page_element.is_enabled()是一个Selenium WebDriver的方法，用于检查页面上的元素是否可点击（即是否处于可用状态）
                if next_page_element and next_page_element.is_enabled():
                    next_page_element.click()
                    time.sleep(3)  # 等待页面加载
                    # 切换到新打开的页面
                    wd.switch_to.window(wd.window_handles[-1])
                    elements = wd.find_elements(By.XPATH, '//ul/table[@border="0" and @width="100%"]')
                    for element in elements:
                        # 在每一个 tbody 元素内查找 a 标签
                        a_tag = element.find_element(By.TAG_NAME, 'a')
                        href = a_tag.get_attribute('href')
                        title = a_tag.text
                        if key in title:
                            final = {'Title': title,
                                     'Link': href
                                     }
                            finally_list.append(final)
                    # time.sleep(5)
                else:
                    break  # 如果没有找到下一页按钮或者下一页按钮不可点击，退出循环
            except:
                break  # 如果找不到下一页按钮，退出循环
        # pages = wd.find_elements(By.XPATH,'//ul/table[@cellpadding=0]')
        #
        # page_urls = []
        #
        # if pages:
        #     for page in pages:
        #         # 不要后2个td/a
        #         urls = page.find_elements(By.XPATH,'//td[position() < last() -1] /a')
        #         for url in urls:
        #             x = url.get_attribute('href')
        #             page_urls.append(x)
        #     for url in page_urls:
        #         wd.get(url)
        #         elements = wd.find_elements(By.XPATH, '//ul/table[@border="0" and @width="100%"]')
        #         for element in elements:
        #             # 在每一个 tbody 元素内查找 a 标签
        #             a_tag = element.find_element(By.TAG_NAME, 'a')
        #             href = a_tag.get_attribute('href')
        #             title = a_tag.text
        #             final = {'Title': title,
        #                      'Link': href
        #                      }
        #             finally_list.append(final)
        #         time.sleep(3)
        wd.close()
        return finally_list
    else:
        return '没有找到相关电影'



if __name__ == '__main__':
    key = input('请输入查询电影的名称：')
    print(search(key))
