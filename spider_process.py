# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
# 何为协议何为自动化
# https://mp.weixin.qq.com/s/Boebq6G92bv3GNEIMaVUxQ

# step1: 浏览器F12 打开开发者工具面板，进行网络抓包
# step2: 进入目标页面，观察网络请求列表，找到关键请求
# step3: 打开关键请求详情，观察请求协议，分析请求参数
# step4: 逆向参数生成逻辑：议破解的关键就是最后一类 签名、加密参数。
#        这类参数的生成伴随着单向散列、加密等逻辑，再配合上客户端代码混淆，参数生成逻辑会藏得较深，需要配合 断点、调用栈 进行调试分析
# step5:脚本伪装客户端逻辑:使用代码将 IP代理、参数伪造、HTTP请求 等逻辑固定下来形成脚本。
#       脱离客户端，略过页面渲染和交互过程，使效率最大化


import requests

url1 = ('https://ygp.gdzwfw.gov.cn/#/44/new/jygg/v3/A?noticeId=52cd39dd-7015-46fb-8072-a088d1bcb8b1&projectCode=E4401000002400710001&bizCode=3C31&siteCode=440100&publishDate=20240312173004&source=%E5%B9%BF%E4%BA%A4%E6%98%93%E6%95%B0%E5%AD%97%E4%BA%A4%E6%98%93%E5%B9%B3%E5%8F%B0&titleDetails=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE&classify=A02&nodeId=1823240830880374785'
       )

import requests


headers = {
    "Referer": "https://ygp.gdzwfw.gov.cn/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "X-Dgi-Req-App": "ggzy-portal",
    "X-Dgi-Req-Nonce": "mNGPNJa9FAAi1bB9",
    "X-Dgi-Req-Signature": "d19545cc1922a8bb9861531f63f0b4441af72c9bb7255967100b16e49cc76475",
    "X-Dgi-Req-Timestamp": "1725200813276",

}

url = "https://ygp.gdzwfw.gov.cn/ggzy-portal/center/apis/trading-notice/new/detail"
params = {
    "nodeId": "1823240830880374785",
    "version": "v3",
    "tradingType": "A",
    "noticeId": "52cd39dd-7015-46fb-8072-a088d1bcb8b1",
    "bizCode": "3C31",
    "projectCode": "E4401000002400710001",
    "siteCode": "440100"
}
response = requests.get(url, headers=headers,  params=params)

print(response.text)
print(response)

# (function() {
#     // 保存原始的 setRequestHeader 方法
#     var headerCache = XMLHttpRequest.prototype.setRequestHeader;
#
#     // 重写 setRequestHeader 方法
#     XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
#         // 打印设置的请求头
#         console.log("Hook set header %s => %s", key, value);
#
#         // 如果请求头的键是 "x-Dgi-Reg Signature"，则触发调试器
#         if (key === "X-Dgi-Req-Signature") {
#             debugger;
#         }
#
#         // 调用原始的 setRequestHeader 方法
#         headerCache.apply(this, arguments);
#     };
# })();
