# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import ChromiumPage, ChromiumOptions

# import ddddocr
# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式

page = ChromiumPage(co)
page.get('https://cszg.mca.gov.cn/biz/ma/csmh/g/cszzsearch.html?value=社会')
# 1.获取滑块背景图/缺口图 字节
background_bytes = page('#oriImg').src()  #背景图 字节
cut_bytes = page('#cutImg').src()  #缺口图 字节
# 2.识别滑块缺口并获得滑动轨迹
det = ddddorc.DdddOcr(det=False, ocr=False, show_ad=False)
result = det.slide_match(cut_bytes, background_bytes, simple_target=True)
