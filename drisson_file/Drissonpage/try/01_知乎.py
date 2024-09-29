#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(False)  # 使用无痕模式
co.set_argument('--start-maximized')
page = ChromiumPage(co)
page.get('https://www.zhihu.com/question/635637744')

page.listen.start('/api/v4/questions/635637744/feeds')
data_packet = page.listen.wait()
print('监听数据包响应', data_packet.response.body)

if __name__ == "__main__":
    pass
