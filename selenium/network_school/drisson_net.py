import ddddocr
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import wait_until
import json
import traceback
import time
from loguru import logger
# import ddddocr

# 读取配置文件
with open('../../selenium/network_school/config.json', 'r') as file:
    config = json.load(file)
# import os
# config_path = os.path.abspath('../../selenium/network_school/config.json')
# print("Resolved Path:", config_path)               #确认文件
username = config['username']
password = config['password']

# 设置 loguru 日志记录配置
# logger.add('error_log.txt', level='ERROR', format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}', rotation='10 MB')
# info以上日志都记录
logger.add('info_log.txt', level='INFO', format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}', rotation='10 MB')


def calculate_time(original_value, percentage_str):
    """计算给定百分比减少后的值"""

    percentage = float(percentage_str.strip('%')) / 100
    decreased_value = int(original_value * (1 - percentage)) * 60
    return max(decreased_value, 60)  # 设置最小等待时间为60秒


co = ChromiumOptions()
co.headless(False)  # 无头模式
co.incognito(True)  # 无痕模式

co.set_argument('--start-maximized')
co.mute(True)
# co.no_imgs(True) 验证码也加载不了
page = ChromiumPage(co)
logger.info('==========================开始运行=================================')
# 打开网站并登录
page.get('https://www.samrela.com/')
page('#username').clear()
page('#username').input(username)  # 输入用户名
page('#pwd').clear()
page('#pwd').input(password)  # 输入密码
ocr = ddddocr.DdddOcr()  # 创建 OCR 对象 在循环里面，每次都会创建一个 对象。移到循环外，以减少资源消耗
max_attempts = 5  # 最大尝试次数
attempts = 0

while attempts < max_attempts:
    img_bytes = page('#codeImg').src()  # 获取验证码图片字节
    yzm = ocr.classification(img_bytes)  # 识别验证码
    page('#yzm').clear()
    page('#yzm').input(yzm)
    page('.login_btn').click()
    logger.info("登录中...")

    alert_text = page.handle_alert(timeout=3)
    # logger.info(f'错误信息==={alert_text}')

    if alert_text:  # 如果有弹窗信息
        if "验证码错误" in alert_text:
            logger.error("验证码错误，重新尝试")
            attempts += 1
            time.sleep(2)  # 等待2秒后重试
            continue
        elif '用户名或密码错误' in alert_text:
            logger.error('用户名或密码错误')
            page.quit()  # 立即退出浏览器
            raise SystemExit  # 退出程序
    else:
        logger.info('登录成功')
        break

if attempts >= max_attempts:
    logger.error('超过最大尝试次数，登录失败')
    page.quit()
    raise SystemExit

new_tab_1 = page('进入学员中心').click.for_new_tab()  # 点击进入新页面
# processed_specials = set()  # 用于存储已处理的专题名称
special_list = new_tab_1.eles('.join_special_list')
nums = len(special_list)
try:
    for num in range(nums):
        # print(special_list[num]('.join_course_name').text)
        special_list = new_tab_1.eles('.join_special_list')
        study_name = special_list[num]('.join_course_name').text
        course = special_list[num]
        if course('已结业'):
            logger.info(f'专题《{study_name}》已结业')
            continue
        logger.info(f'专题《{study_name}》===》开始学习')
        new_tab_2 = course('进入学习').click.for_new_tab()
        lessons = new_tab_2.eles('.hoz_course_row')
        lessons_nums = len(lessons)
        processed_lessons = set()
        for x in range(lessons_nums):# 存储已处理的课程
            lesson = lessons[x]
            logger.info(lesson('.hoz_course_name').text)
        logger.info(f"{study_name}学完")
        new_tab_2.back()


    logger.info('Done')
except Exception as e:
    logger.error(f'专题《{study_name}》出现错误: {e}')
    logger.error('堆栈跟踪信息:\n' + traceback.format_exc())



