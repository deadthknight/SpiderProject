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
from loguru import logger
import traceback

# 设置 loguru 日志记录配置 每个日志文件的大小将限制在 10 MB。当文件大小超过 10 MB 时，loguru 会自动创建一个新的日志文件，并在文件名中添加时间戳或序号，以区分不同的日志文件。
logger.add('error_log_chen.txt', level='ERROR', format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}', rotation='10 MB')
logger.add('info_log_chen.txt', level='INFO', format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}')

def log_error(e):
    """记录错误日志并输出异常详细信息"""
    logger.error(f"Exception occurred: {traceback.format_exc()}")

# 读取配置文件
with open('config.json', 'r') as file:
    config = json.load(file)

username = config['username_chen']
password = config['password_chen']

def random_wait(min_time=2, max_time=5):
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
chrome_options.add_argument('--mute-audio')  # 静音所有标签页
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# 启动浏览器
driver = webdriver.Chrome(options=chrome_options,
                          service=Service(r'F:\Python\tool\chromedriver-win64\chromedriver.exe'))
try:
    driver.maximize_window()
    logger.info("====================开始学习=======================")
    # 第一次访问目标网站
    driver.get('https://www.samrela.com/')
    driver.implicitly_wait(5)

    # 输入用户名、密码和验证码
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'pwd')
    captcha_input = driver.find_element(By.ID, 'yzm')
    logger.info("登录中。。。")
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
            logger.error('验证码错误，重新获取验证码...')
            random_wait()
        except Exception:
            logger.info('登录成功')
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
            logger.info('全部课程学习完毕')
            break

        # 处理当前专题班
        while current_index < len(elements):
            element = elements[current_index]
            study_name = element.find_element(By.XPATH, './/*[@class="join_course_name"]').text
            logger.info(f'学习第{current_index + 1}个专题{study_name}')
            study_status = element.find_elements(By.XPATH, './/*[@class="join_status"]')
            study_in_element = element.find_element(By.XPATH, './/img')
            last_join_status = study_status[-1]
            if last_join_status.text == '未结业':
                logger.info(f'开始学习=====>{study_name}')
                driver.execute_script("arguments[0].scrollIntoView();", study_in_element)
                random_wait()
                study_in_element.click()

                # 尝试学习每个课程
                try:
                    lessons = driver.find_elements(By.XPATH, '//div[@class="hoz_course_row"]')
                    for lesson in lessons:
                        learning_process = lesson.find_element(By.XPATH, './/span[@class="h_pro_percent"]')
                        learning_time = lesson.find_element(By.XPATH, './/p[@class="hoz_four_info"]/span')
                        # logger.info(f"学习进度: {learning_process.text}")
                        learning_time = int(learning_time.text.strip().split(' ')[0])
                        sleep_time = calculate_time(learning_time, learning_process.text)
                        if learning_process.text == '100.0%':
                            continue
                        click_study = lesson.find_element(By.XPATH, './/a[contains(text(), "我要学习")]')
                        click_study.click()
                        driver.switch_to.window(driver.window_handles[-1])
                        logger.info("尝试点击 '开始学习' .....")
                        try:
                            start_study = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//div[contains(text(), "开始学习") or contains(text(), "继续学习")]')
                                )
                            )
                            driver.execute_script("arguments[0].scrollIntoView(true);", start_study)  # 元素滚动到可视区域顶部
                            time.sleep(1)  # 确保元素可见
                            driver.execute_script("arguments[0].click();", start_study)
                            time.sleep(sleep_time + 100)
                            random_wait()
                            driver.close()
                            driver.switch_to.window(driver.window_handles[-1])
                            random_wait()
                        except Exception as e:
                            log_error(f"点击 '开始学习' 按钮失败: {e}")
                            logger.info("尝试刷新页面并重新尝试...")
                            driver.refresh()
                            time.sleep(5)  # 等待页面刷新
                            driver.execute_script("arguments[0].scrollIntoView(true);", start_study)  # 再次滚动到元素
                            driver.execute_script("arguments[0].click();", start_study)  # 再次点击
                            time.sleep(sleep_time + 100)
                            random_wait()

                    logger.info(f'{study_name}学习完毕，开始学习下一个专题')
                except Exception as e:
                    log_error(e)
                finally:
                    driver.back()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="join_special_list"]'))
                    )
                    time.sleep(2)
                    current_index += 1
                    break
            else:
                logger.info(f'{study_name}已结业')
                current_index += 1

except Exception as e:
    log_error(e)
finally:
    logger.info('关闭浏览器')
    driver.quit()

if __name__ == "__main__":
    pass
