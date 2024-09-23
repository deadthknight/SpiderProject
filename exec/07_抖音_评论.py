#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
# co.incognito(True)  # 使用无痕模式
co.mute(True)    # 方法用于设置是否静音
co.set_argument('--start-maximized')
page = ChromiumPage(co)
page.listen.start('/aweme/v1/web/comment/list/?')
page.get('https://www.douyin.com/user/MS4wLjABAAAA6TkUZqEal5TpCEjdgIPAlzAP-DxKRUjJsx3ut7ZYaLw?from_tab_name=main&modal_id=7409233393348594996')
data_packet = page.listen.wait()

print('监听数据包响应', data_packet.response.body)

if __name__ == "__main__":
    pass
