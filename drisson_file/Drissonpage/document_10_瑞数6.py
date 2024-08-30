from DrissionPage import WebPage, ChromiumOptions
import requests
from lxml import etree

co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式
page = WebPage(mode='d',chromium_options=co)
page.listen.start('api/internet/event/homePage/list')
page.get('https://www.urbtix.hk/')
page.wait.load_start()
page.listen.wait()
item = []
clicked = False
for packet in page.listen.steps():
    response = packet.response.body
    for x in response['data']:
        print(x)
        item.append(x)
    page.scroll.to_bottom()
    if not clicked:
        page('展开全部').click(by_js=True)
        clicked = True  # 设置标志变量，表示已经点击了“展开全部”
    elif clicked:
        break  # 点击后的下一次循环，退出循环
print(len(item))