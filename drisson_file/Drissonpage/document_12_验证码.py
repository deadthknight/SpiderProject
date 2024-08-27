from DrissionPage import ChromiumPage, ChromiumOptions
import ddddocr
import json
# 读取配置文件
with open('../../selenium/network_school/config.json', 'r') as file:
    config = json.load(file)
# import os
# config_path = os.path.abspath('../../selenium/network_school/config.json')
# print("Resolved Path:", config_path)               #确认文件
username = config['username']
password = config['password']



co = ChromiumOptions()
# co.set_browser_path()  #浏览器地址，默认是chrome
co.headless(False)   # 无头模式
co.incognito(True)  # 无痕模式
co.set_pref('credentials_enable_service', True)  # 阻止“自动保存密码”的提示气泡
co.set_argument('--hide-crash-restore-bubble')   # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
page = ChromiumPage(co)
# page.set.auto_handle_alert(all_tabs=True)  # 这之后出现的弹窗都会自动确认
#===========================================================
page.get('https://www.samrela.com/')
page('#username').input(username)        #输入用户名
page('#pwd').input(password)             #输入密码
while True:
    img_bytes = page('#codeImg').src()             #拿到图片字节
    ocr = ddddocr.DdddOcr()                  #创建对象
    yzm = ocr.classification(img_bytes)
    page('#yzm').clear()
    page('#yzm').input(yzm)
    page('.login_btn').click()
    # txt = page.handle_alert()              # 确认提示框并获取提示框文本
    # print(txt)
    print("点击登录按钮，等待处理...")  # 调试信息

    alert_text = page.handle_alert(timeout=3)
    if alert_text:  # 如果有弹窗信息
        print(f"弹窗信息: {alert_text}")
        if "验证码错误" in alert_text:
            print("验证码错误，重新尝试")
            continue  # 处理验证码错误，重新尝试
    else:  # 没有弹窗信息
        print('登录成功')
        break

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