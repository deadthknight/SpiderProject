# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get('https://www.baidu.com')
# page.new_tab('https://www.baidu.com')
#
# tabs = page.get_tabs(url='baidu.com')
# print(tabs)

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