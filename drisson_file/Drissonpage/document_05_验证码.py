# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import ChromiumPage, ChromiumOptions
# import ddddocr
# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式

page = ChromiumPage(co)
page.get('https://spxksq.amr.guizhou.gov.cn:9081/TopFDOAS/searchDoc.action')
page('#nameLicNo').input('多彩贵州文化艺术股份有限公司')
img_bytes = page('#captchaImg').src()   #图片字节
print(img_bytes)
page('#cxBut').click()
wrong = page('#newvbutton')
if wrong:
    wrong.click()
# ocr = ddddocr.DdddOcr(show_ad=False)
# yzm = ocr.classification(img_bytes)
# page('#yzm').input(yzm)
# page('#cxBut').click()