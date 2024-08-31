from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
# co.set_browser_path()  #浏览器地址，默认是chrome
# 无头模式
co.headless(False)
# 无痕模式#无头模式
co.incognito(True)  # 无痕模式
# 阻止“自动保存密码”的提示气泡
co.set_pref('credentials_enable_service', False)
# 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
co.set_argument('--hide-crash-restore-bubble')
# 指定端口
co.set_local_port(9211)
#设置UA 默认是
page = ChromiumPage(co)

# page.set.window.max() # 使窗口最大化。
# from TimePinner import Pinner  # 导入计时工具

# ===================================================
# pinner = Pinner()  # 创建计时器对象
# page = ChromiumPage()
# page.get('https://www.163.com')
#
# pinner.pin()  # 标记开始记录
#
# # 获取所有链接对象并遍历
# links = page('t:body').eles('t:a')
# for lnk in links:
#     print(lnk.text)
#
# pinner.pin('用时')  # 记录并打印时间    13.201472237

# pinner = Pinner()  # 创建计时器对象
# page = ChromiumPage()
# page.get('https://www.163.com')
#
# pinner.pin()  # 标记开始记录
#
# # 获取所有链接对象并遍历
# links = page('t:body').s_eles('t:a')           #转成静态页面 提取元素
# for lnk in links:
#     print(lnk.text)

# pinner.pin('用时')  # 记录并打印时间  用时：2.032593744
# ===========================================================

page.get('https://www.baidu.com', retry=1, interval=1, timeout=1.5)  # 重传次数 间隔 超时时间
print(f'==============================\n'
      f'当前对象地址和端口:{page.address}\n'
      f'请求头:{page.user_agent}\n'
      f'是否正在加载：{page.states.ready_state}')
      # f'cookies:{page.cookies(as_dict=False)}')
# page('x://input[@id="kw"]').input('Drissionpage')  #找到输入框 输入Drissionpage
# page.ele('x://input[@id="su"]').click()   #点击按钮
# page.wait.load_start()   #等待页面加载
#
# print('Page Title:', page('x:/html/head/title').text)