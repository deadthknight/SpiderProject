from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://www.baidu.com')
page.new_tab('https://www.sohu.com')
page.new_tab('https://www.163.com/')

tab = page.get_tab(1)
tab2 = page.get_tab(2)
tab3 = page.get_tab(3)
print(tab.title)
print(tab2.title)
print(tab3.title)

# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get('https://gitee.com/explore/all')  # 访问网址，这行产生的数据包不监听
#
# page.listen.start('gitee.com/explore')  # 开始监听，指定获取包含该文本的数据包
# for _ in range(5):
#     page('@rel=next').click()  # 点击下一页
#     res = page.listen.wait()  # 等待并获取一个数据包
#     print(res.url)  # 打印数据包url

# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.listen.start('gitee.com/explore')  # 开始监听，指定获取包含该文本的数据包
# page.get('https://gitee.com/explore/all')  # 访问网址
#
# i = 0
# for packet in page.listen.steps():
#     print(packet.url)  # 打印数据包url
#     page('@rel=next').click()  # 点击下一页
#     i += 1
#     if i == 5:
#         break


#动作链
# from DrissionPage import ChromiumPage
# from loguru import logger
# page = ChromiumPage()
# page.get('https://www.baidu.com')
# page.actions.move_to('#kw').click().type('天气')
# page.actions.move_to('#su').click()
from loguru import logger

#pip install data-recorder
# 存储文件
# @logger.catch
# def divide(a, b):
#     return a / b
#
# divide(10, 0)  # 发生异常时，loguru 会自动记录异常信息

