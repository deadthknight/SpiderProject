#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ddddocr
import random
import json
import logging
from datetime import datetime

# 设置日志记录配置
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def log_error(e):
    """记录错误日志"""
    logging.error(f"Error occurred: {e}")


# 读取配置文件
with open('config.json', 'r') as file:
    config = json.load(file)

username = config['username']
password = config['password']


def random_wait(min_time=1, max_time=3):
    """生成随机等待时间"""
    time.sleep(random.uniform(min_time, max_time))


def calculate_time(original_value, percentage_str):
    """计算给定百分比减少后的值"""
    percentage = float(percentage_str.strip('%')) / 100
    decreased_value = int(original_value * (1 - percentage)) * 60
    return max(decreased_value, 60)  # 设置最小等待时间为60秒


ocr = ddddocr.DdddOcr()

# 创建一个Chrome选项对象
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# 启动浏览器
driver = webdriver.Chrome(options=chrome_options,
                          service=Service(r'F:\Python\tool\chromedriver-win64\chromedriver.exe'))
try:
    driver.maximize_window()

    # 第一次访问目标网站
    driver.get('https://www.samrela.com/')
    driver.implicitly_wait(5)

    # 输入用户名、密码和验证码
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'pwd')
    captcha_input = driver.find_element(By.ID, 'yzm')

    username_input.send_keys(username)
    random_wait()
    password_input.send_keys(password)
    random_wait()

    while True:
        # 获取验证码
        pngData = driver.find_element(By.ID, 'codeImg').screenshot_as_png
        result = ocr.classification(pngData)  # 验证码识别
        captcha_input.clear()
        captcha_input.send_keys(result)

        login_button = driver.find_element(By.XPATH, "//div/input[@type='button' and @value='登录']")
        login_button.click()

        # 处理验证码错误的弹出框
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            random_wait()
            alert.accept()
            print('验证码错误，重新获取验证码...')
            random_wait()
        except Exception:
            print('登录尝试完成')
            break

    # 登录状态检查并进入学员中心
    login_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '进入学员中心')]"))
    )
    login_input.click()

    # 切换到新打开的页面
    driver.switch_to.window(driver.window_handles[-1])

    # 初始化索引
    current_index = 0

    while True:
        # 显式等待并获取页面上的元素
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="join_special_list"]'))
        )
        elements = driver.find_elements(By.XPATH, '//div[@class="join_special_list"]')

        if current_index >= len(elements):
            break

        # 处理当前专题班
        while current_index < len(elements):
            element = elements[current_index]
            study_status = element.find_elements(By.XPATH, './/*[@class="join_status"]')
            study_in_element = element.find_element(By.XPATH, './/img')
            last_join_status = study_status[-1]
            if last_join_status.text == '未结业':
                driver.execute_script("arguments[0].scrollIntoView();", study_in_element)
                time.sleep(1)
                study_in_element.click()

                lessons = driver.find_elements(By.XPATH, '//div[@class="hoz_course_row"]')
                for lesson in lessons:
                    learning_process = lesson.find_element(By.XPATH, './/span[@class="h_pro_percent"]')
                    learning_time = lesson.find_element(By.XPATH, './/p[@class="hoz_four_info"]/span')
                    learning_time = int(learning_time.text.strip().split(' ')[0])
                    sleep_time = calculate_time(learning_time, learning_process.text)
                    if learning_process.text == '100.0%':
                        continue

                    click_study = lesson.find_element(By.XPATH, './/a[contains(text(), "我要学习")]')
                    click_study.click()
                    driver.switch_to.window(driver.window_handles[-1])

                    # 等待并点击“开始学习”按钮
                    start_study = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[contains(text(), "开始学习") or contains(text(), "继续学习")]')
                        )
                    )
                    start_study.click()
                    time.sleep(sleep_time + 100)

                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])
                driver.back()

                # 等待并获取重新加载的元素
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="join_special_list"]'))
                )
                time.sleep(2)

                current_index += 1
                print("本专题班学习完毕，开始下一个")
                break
            else:
                current_index += 1

except Exception as e:
    log_error(e)
finally:
    driver.quit()
    print('全部课程学习完毕')

if __name__ == "__main__":
    pass
