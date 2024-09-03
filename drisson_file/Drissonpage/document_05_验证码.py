from DrissionPage import ChromiumPage, ChromiumOptions
import ddddocr
import json
from loguru import logger

# 读取配置文件
with open('../../selenium/network_school/config.json', 'r') as file:
    config = json.load(file)
# import os
# config_path = os.path.abspath('../../selenium/network_school/config.json')
# print("Resolved Path:", config_path)               #确认文件
username = config['username']
password = config['password']

# 设置 loguru 日志记录配置
logger.add('error_log.txt', level='ERROR', format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}', rotation='10 MB')
# logger.add('info_log.txt', level='INFO', format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}')

def calculate_time(original_value, percentage_str):
    """计算给定百分比减少后的值"""
    percentage = float(percentage_str.strip('%')) / 100
    decreased_value = int(original_value * (1 - percentage)) * 60
    return max(decreased_value, 60)  # 设置最小等待时间为60秒

co = ChromiumOptions()
co.headless(False)  # 无头模式
# co.incognito(True)  # 无痕模式
co.set_browser_path(r'C:\Program Files (x86)\Microsoft\Edge Dev\Application\129.0.2792.10\msedge.exe')   # edge 运行
co.set_pref('credentials_enable_service', True)  # 阻止“自动保存密码”的提示气泡
co.set_argument('--hide-crash-restore-bubble')  # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
co.set_argument('--start-maximized')
co.mute(True)
# co.no_imgs(True) 验证码也加载不了
page = ChromiumPage(co)

# 打开网站并登录
page.get('https://www.samrela.com/')
page('#username').input(username)  # 输入用户名
page('#pwd').input(password)  # 输入密码

while True:
    img_bytes = page('#codeImg').src()  # 获取验证码图片字节
    ocr = ddddocr.DdddOcr()  # 创建 OCR 对象
    yzm = ocr.classification(img_bytes)  # 识别验证码
    page('#yzm').clear()
    page('#yzm').input(yzm)
    page('.login_btn').click()
    logger.info("登录中...")

    alert_text = page.handle_alert(timeout=3)
    if alert_text:  # 如果有弹窗信息
        if "验证码错误" in alert_text:
            logger.error("验证码错误，重新尝试")
            continue  # 处理验证码错误，重新尝试
    else:
        logger.info('登录成功')
        break

new_tab_1 = page('进入学员中心').click.for_new_tab()  # 点击进入新页面

processed_specials = set()  # 用于存储已处理的专题名称

while True:
    try:
        special_list = new_tab_1.eles('.join_special_list')
        for course in special_list:
            study_name = course(".join_course_name").text
            if study_name in processed_specials:  # 如果专题已处理过，跳过
                continue
            if course('已结业'):
                logger.info(f'专题《{study_name}》已结业')
                processed_specials.add(study_name)  # 标记为已处理
                continue  # 已结业的专题，跳过
            logger.info(f'专题《{study_name}》===》开始学习')

            course('进入学习').click()
            lessons = new_tab_1.eles('.hoz_course_row')

            for lesson in lessons:
                try:
                    learning_process = lesson('.h_pro_percent').text
                    learning_time = int(lesson('.hoz_four_info').text.strip().split(' ')[0])
                    sleep_time = calculate_time(learning_time, learning_process)

                    if learning_process == '100.0%':
                        break

                    new_tab_2 = new_tab_1('我要学习').click.for_new_tab(by_js=True)
                    new_tab_2.wait(1,3)
                    new_tab_2('@|tx()=继续学习@|tx()=开始学习').click()
                    new_tab_2.wait(sleep_time + 100)
                    new_tab_2.close()  # 关闭新窗口
                except Exception as e:
                    logger.error(f'课程《{lesson.text}》学习过程中出现错误: {e}')
                    if new_tab_2.exists:
                        new_tab_2.close()  # 关闭新窗口
                    continue  # 继续处理下一个课程

            logger.info(f'专题《{study_name}》已学习完毕')
            new_tab_1.back()  # 返回上一页
            new_tab_1.refresh()  # 刷新页面
            break  # 处理完一个专题后跳出循环
    except Exception as e:
        logger.error(f'处理专题时出现错误: {e}')
        new_tab_1.refresh()  # 如果出现错误，刷新页面并继续
        continue

    logger.info('全部专题已学习完毕')
    break

page.quit()  # 退出浏览器


#     try:
#         alert_text = page.handle_alert(timeout=5)  # 等待弹窗出现
#         print(f"弹窗信息: {alert_text}")
#         if "验证码错误" in alert_text:
#             print("验证码错误，重新尝试")
#             continue  # 处理验证码错误，重新尝试
#     except Exception as e:
#         print(f"异常信息: {e}")  # 打印异常信息
#         print('登录成功')
#         break
#
# print('等待')
# 点击登录按钮，等待处理...
# 弹窗信息: False
# 异常信息: argument of type 'bool' is not iterable
# 登录成功
# 等待
# handle_alert() 返回了 False，这是因为当没有弹窗时，它会返回 False，而不是抛出异常。
# 这也解释了 try-except 块中出现的异常提示。False 不能被用于字符串的匹配检查（"验证码错误" in alert_text），这导致了异常。