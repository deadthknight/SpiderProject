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
co.set_pref('credentials_enable_service', False)  # 阻止“自动保存密码”的提示气泡
co.set_argument('--hide-crash-restore-bubble')   # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
page = ChromiumPage()
page.get('https://www.samrela.com/')
page('#username').input(username)        #输入用户名
page('#pwd').input(password)             #输入密码
img_bytes = page('#codeImg').src()             #拿到图片字节
ocr = ddddocr.DdddOcr()                  #创建对象
yzm = ocr.classification(img_bytes)
page('#yzm').input(yzm)