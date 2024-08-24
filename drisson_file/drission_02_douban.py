
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式

# 创建页面对象
page = ChromiumPage(co)

# 访问网页
page.get('https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4')
for x in range(3):
    li_list = page.eles('.subject-item')
    for li in li_list:
        img = li('t:img')
        # 保存图片
        img.save(r'.\imgs')
    print(f"第{x+1}页下载完毕")
    btn = page('后页', timeout=2)   #2s超时  默认page.set.timeout = 10
    if btn:
        btn.click()
        page.wait.load_start()  # 等待页面开始加载
print("全部下载完毕")


