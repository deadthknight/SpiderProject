# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import ChromiumPage
page = ChromiumPage()
page.get('https://news.qq.com/')
page.wait.load_start() # 等待页面开始加载
# page.wait(1) #强制等待1s  根time.sleep()一样
result = []
times = 0
page_i = 1

while True:
    print(f'开始滚动{page_i}次')
    page.scroll.to_bottom()     #滚动到底部
    page_i += 1
    page.wait.load_start()
    len_result = len(result)
    print(f'total_result is {len_result}')
    items = page.eles('x://div[@class="channel-feed-list"]/div')
    print(len(items))
    for item in items:
        title = item('x://span[@class="article-title-text" or @class="question-title-text"]').text
        url = item('x://a').attr('href')
        if url in result:
            continue
        print(title,url)
        result.append(url)
        now_len_result = len(result)
        if now_len_result == len_result:
            times += 1
        else:
            times = 0
        if times > 3:
            print('加载完毕')
            break
