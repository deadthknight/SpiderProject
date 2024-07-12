# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
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
    wd.implicitly_wait(10)

    finally_list = []

    try:
        while True:
            retry_count = 0
            max_retries = 3

            while retry_count < max_retries:
                try:
                    wd.get('https://dytt.dytt8.net/index.htm')  # 隐式等待

                    element = wd.find_element(By.CLASS_NAME, 'formhue')
                    element.clear()
                    element.send_keys(key)
                    # 发送回车
                    element.send_keys(Keys.RETURN)

                    while True:

                        elements = wd.find_elements(By.XPATH, '//table[@border="0" and @width="100%"]//a')

                        if not elements:
                            # print("No elements found, retrying page...")
                            # retry_count += 1
                            # time.sleep(2)
                            break  # 退出内循环，重新尝试加载页面

                        for element in elements:
                            href = element.get_attribute('href')
                            title = element.text
                            if key in title:
                                finally_list.append({'Title': title, 'Link': href})

                        try:
                            # 查找“下一页”链接
                            next_page_element = wd.find_element(By.LINK_TEXT, '下一页')
                            if next_page_element.is_enabled():
                                next_page_element.click()
                                time.sleep(3)  # 等待页面加载
                                wd.switch_to.window(wd.window_handles[-1])
                                if wd.find_element(By.XPATH, '/html/body').text == '亲，您刷新太快哦！':
                                    time.sleep(3)
                                    wd.switch_to.window(wd.window_handles[-2])
                            else:
                                break  # 如果没有找到下一页链接或者不可点击，退出循环
                        except Exception:
                            break  # 如果发生异常，退出循环

                    if finally_list:
                        return finally_list  # 如果找到了结果，返回结果

                except Exception as e:
                    print(f"An error occurred: {e}. Retrying {retry_count + 1}/{max_retries}...")
                    retry_count += 1
                    time.sleep(2)  # 等待一段时间后重试

            # 如果达到最大重试次数，则退出外部循环
            if retry_count >= max_retries:
                break
    finally:
        wd.quit()  # 确保在所有尝试完成后关闭浏览器

    return '没有找到相关电影'



if __name__ == '__main__':
    key = input('请输入查询电影的名称：')
    print(search(key))
