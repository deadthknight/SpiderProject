#!/usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import ddddocr
import random


def random_wait(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

def calculate_time(original_value, percentage_str):
    """
    计算给定百分比减少后的值。

    参数:
    original_value (float 或 int): 原始值
    percentage_str (str): 百分比字符串，格式如 '2.37%'

    返回:
    float: 减少后的值
    """
    # 提取百分比数字并转换为浮点数
    percentage = float(percentage_str.strip('%')) / 100

    # 计算减少后的值
    decreased_value = int(original_value * (1 - percentage))*60

    return decreased_value


ocr = ddddocr.DdddOcr()

# 创建一个Chrome选项对象
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')    #关闭https
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# 启动浏览器
driver = webdriver.Chrome(options=chrome_options,
                          service=Service(r'E:\PycharmProjects\chromedriver_win32\chromedriver.exe'))


# 最大化浏览器窗口
driver.maximize_window()

# 第一次访问目标网站
driver.get('https://www.samrela.com/')

driver.implicitly_wait(5)




# 输入用户名、密码和验证码
username_input = driver.find_element(By.ID, 'username')
password_input = driver.find_element(By.ID, 'pwd')
captcha_input = driver.find_element(By.ID, 'yzm')

username_input.send_keys('13810909692')  # 替换为实际的用户名
random_wait()
password_input.send_keys('Oa@82261222')  # 替换为实际的密码
random_wait()

while True:
# 获取验证码
    pngData = driver.find_element(By.ID, 'codeImg').screenshot_as_png
    result = ocr.classification(pngData)  # 验证码
    # print('验证码是', result)
    captcha_input.clear()  # 清除之前的验证码输入
    captcha_input.send_keys(result)  # 输入验证码

    login_button = driver.find_element(By.XPATH, "//div/input[@type='button' and @value='登录']")
    login_button.click()

    # 处理验证码错误的弹出框
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        random_wait()
        alert.accept()  # 接受弹出框
        print('验证码错误，重新获取验证码...')
        random_wait()
        continue  # 重新循环获取新验证码
    except:
        # 如果没有弹出框，说明登录可能成功
        print('登录尝试完成')
        break  # 退出循环

# # 登录状态检查
login_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '进入学员中心')]")))

login_input.click()

# 切换到新打开的页面
driver.switch_to.window(driver.window_handles[-1])
elements = driver.find_elements(By.XPATH, '//div[@class="join_special_list"]')

for element in elements:
    study_status = element.find_elements(By.XPATH, './/*[@class="join_status"]')
    study_in_element = element.find_element(By.XPATH, './/img')
    last_join_status = study_status[-1]
    if last_join_status.text == '未结业':
        # 滚动到指定位置
        # driver.execute_script("arguments[0].scrollIntoView();", study_in_element)
        # time.sleep(1)
        study_in_element.click()
        # 点击
        # driver.execute_script("arguments[0].click();", study_in_element)
        lessons = driver.find_elements(By.XPATH, '//div[@class="hoz_course_row"]')
        for lesson in lessons:
            learning_process = lesson.find_element(By.XPATH, './/span[@class="h_pro_percent"]')
            learning_time = lesson.find_element(By.XPATH, './/p[@class="hoz_four_info"]/span')
            print(learning_process.text, learning_time.text)
            learning_time = int(learning_time.text.strip().split(' ')[0])
            sleep_time = calculate_time(learning_time,learning_process.text)

            print(sleep_time)
            if learning_process.text == '100.0%':
                continue
            click_study = lesson.find_element(By.XPATH, './/a[contains(text(), "我要学习")]')
            click_study.click()
            driver.switch_to.window(driver.window_handles[-1])
            wait = WebDriverWait(driver, 10)
            start_study = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "开始学习")]')))
            if start_study:
                driver.execute_script("$(arguments[0]).click();", start_study)
                time.sleep(1000)
            else:
                time.sleep(1000)
# for element in elements:
#     # 重新查找状态元素
#     study_status = element.find_elements(By.XPATH, './/*[@class="join_status"]')
#     last_join_status = study_status[-1]
#     if last_join_status.text == '未结业':
#         study_in_element = element.find_element(By.XPATH, './/img')
#         # # 滚动到指定位置
#         # driver.execute_script("arguments[0].scrollIntoView();", study_in_element)
#         time.sleep(1)
#         study_in_element.click()
#         # 等待课程元素加载
#         lessons = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, '//div[@class="hoz_course_row"]'))
#         )
#
#         for lesson in lessons:
#             learning_process = lesson.find_element(By.XPATH, './/span[@class="h_pro_percent"]')
#             learning_time = lesson.find_element(By.XPATH, './/p[@class="hoz_four_info"]/span')
#
#             if learning_process.text == '100.0%':
#                 continue
#
#             # print(learning_process.text, learning_time.text)
#
#             click_study = lesson.find_element(By.XPATH, './/a[contains(text(), "我要学习")]')
#             # 点击并切换到新窗口
#             click_study.click()
#             driver.switch_to.window(driver.window_handles[-1])
#             try:
#                 # 等待并开始学习
#                 start_study = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, './/div[contains(text(), "开始学习")]'))
#                 )
#                 driver.execute_script("arguments[0].click();", start_study)
#                 time.sleep(1000)
#
#             except StaleElementReferenceException as e:
#                 print(f"S======: {e}")
#                 # 在捕获到 StaleElementReferenceException 时，可以尝试重新查找元素
#                 continue


if __name__ == "__main__":
    pass
