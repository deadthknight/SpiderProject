from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 设置 ChromeDriver 路径
chromedriver_path = '/usr/local/bin/chromedriver'
# 设置 Chrome 浏览器的二进制文件路径
chrome_binary_path = '/usr/bin/google-chrome'

# 配置 Chrome 选项
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 无头模式：在服务器或没有图形界面的环境中，Chrome 需要运行在无头模式下（--headless），这样才能在没有显示的情况下运行。添加 --headless 选项后，Chrome 可以在后台运行而不需要显示窗口。
#
# 资源限制：服务器环境可能有资源限制，导致 Chrome 无法正常启动。添加 --no-sandbox 和 --disable-dev-shm-usage 选项可以解决一些与资源限制相关的问题。
#
# --no-sandbox：在没有沙盒的环境中运行，可以避免一些权限问题。
# --disable-dev-shm-usage：使用 /tmp 而不是 /dev/shm，可以解决共享内存不足的问题。
# 二进制路径：指定 Chrome 浏览器的二进制文件路径（binary_location）确保 Selenium 正确找到并使用安装的 Chrome 浏览器。

# 创建 WebDriver 对象
wd = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

# 调用 WebDriver 对象的 get 方法可以让浏览器打开指定网址
wd.get('https://www.baidu.com')

print(wd.title)

# 百度一下，你就知道

# 程序运行完会自动关闭浏览器，这里加入等待用户输入，防止闪退
input('等待回车键结束程序')
