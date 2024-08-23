from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
# 无头模式
co.headless(False)
# 无痕模式#无头模式
co.incognito(True)  # 无痕模式
# 阻止“自动保存密码”的提示气泡
co.set_pref('credentials_enable_service', False)
# 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
co.set_argument('--hide-crash-restore-bubble')
page = ChromiumPage()

# page.set.window.max() # 使窗口最大化。
from TimePinner import Pinner  # 导入计时工具

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
print(page(".title-content-title").text)
