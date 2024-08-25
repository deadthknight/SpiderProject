from DataRecorder import Recorder
from DrissionPage import ChromiumPage, ChromiumOptions

# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式
co.set_argument('--no-sandbox')  # 无沙盒模式
# 设置启动时最大化
co.set_argument('--start-maximized')

# 创建页面对象
page = ChromiumPage(co)

# 访问网页
page.get('https://www.maoyan.com/board/4')

# 创建记录器对象
recorder = Recorder('data.csv')

# 手动写入表头
recorder.add_data(('排名', '电影名称', '主演', '上映时间', '评分'))

# 开始循环爬取数据
while True:
    dd_list = page.eles('t:dd')
    for item in dd_list:
        # 获取需要的信息
        num = item('t:i').text
        score = item('.score').text
        title = item('@data-act=boarditem-click').attr('title')
        star = item('.star').text
        time = item('.releasetime').text

        # 写入到记录器
        recorder.add_data((num, title, star, time, score))

    # 获取下一页按钮，有就点击
    btn = page('下一页', timeout=2)
    if btn:
        btn.click()
        page.wait.load_start()  # 等待页面开始加载
    else:
        break

# 记录数据到文件
recorder.record()
