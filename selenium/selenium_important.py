#!/usr/bin/env python3.12
# -*- coding:utf-8 -*-
import os
import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def create_driver():
    # 配置 ChromeOptions
    options = Options()

    # 禁用 WebDriver 特征
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 无头访问
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    # 创建服务对象
    service = Service(r'/Users/vickyyang/Desktop/study/chromedriver-mac-x64/chromedriver')

    # 忽略 SSL 证书错误
    options.add_argument('--ignore-certificate-errors')

    # 创建 Chrome 浏览器实例
    driver = uc.Chrome(options=options, service=service)
    # 清理缓存
    driver.delete_all_cookies()
    return driver


def random_wait(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))


driver = create_driver()
driver.get("https://www.baidu.com")
# random_wait()

# 使用显式等待替代静态等待
wait = WebDriverWait(driver, 10)
search_box = wait.until(EC.presence_of_element_located((By.ID, 'kw')))
search_box.send_keys('日本环球影城')
random_wait()
search_button = driver.find_element(By.ID, 'su')
search_button.click()

# 等待搜索结果并获取第一个结果的链接
first_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content_left .result a')))
element_href = first_result.get_attribute('href')
# href =driver.get(element_href)
print(element_href)

time.sleep(5)
driver.quit()
