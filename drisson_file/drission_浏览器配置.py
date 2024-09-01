from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.headless(False)  # 无头模式
co.incognito(True)  # 无痕模式
co.set_pref('credentials_enable_service', False)  # 阻止“自动保存密码”的提示气泡
co.set_argument('--hide-crash-restore-bubble')  # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
co.set_argument('--start-maximized')   # 设置启动时最大化
co.auto_port(True)   # 自动使用可用的端口
co.mute(True)    # 方法用于设置是否静音
# co.ignore_certificate_errors()   # 该方法用于设置是否忽略证书错误。可以解决访问网页时出现的“您的连接不是私密连接”、“你的连接不是专用连接”等问题。
# co.set_local_port(9211)    # 指定端口
# co.set_user_agent(user_agent='Mozilla/5.0 (Macintos.....')   # 设置UA
# co.set_browser_path()  # 若不指定浏览器路径，DrissionPage会使用系统自带的chromium
page = ChromiumPage(co)

page.get('https://www.baidu.com', retry=1, interval=1, timeout=1.5)  # 重传次数 间隔 超时时间
print(f'==============================\n'
      f'访问的URL{page.url}\n'
      f'当前对象地址和端口:{page.address}\n'
      f'请求头:{page.user_agent}\n'
      f'是否正在加载：{page.states.ready_state}\n'
      f'链接是否可用：{page.url_available}\n'
      f'当前标签页id：{page.tab_id}\n'
      f'浏览器进程id：{page.process_id}\n'
      f'返回页面是否存在弹出框：{page.states.has_alert}\n'
      f'返回窗口当前状态：{page.rect.window_state}')
      # f'cookies:{page.cookies(as_dict=False)}')
# page.get_screenshot(path='./截图',name='百度',full_page=True) #截图
page.get('https://tls.browserleaks.com/json')
page.get_screenshot(path='./截图',name='无头',full_page=True) #截图
# page.quit()





# 如果要点击的元素就是没有位置的，可以强制使用 js 点击，用法是 .click(by_js=True)，可以简写为 .click('js')。
# 使用无头模式，一定要设置UA，无头模式：HeadlessChrome/128.0.0.0 Safari/537.36，容易被反爬
# co.set_user_agent（user_agent='Mozilla/5.0 (Macintos.....'）


# co.set_proxy('http://1.1.1.1:64256')   #设置代理

# 代理 插件
# SwitchyOmega
# co.add_extension(r'f:\package\Proxy_SwitchOmega_2.5.21')   # 设置插件

# docker 搭建代理池
# https://blog.csdn.net/weixin_43411585/article/details/131798495?ops_request_misc=%257B%2522request%255Fid%2522%253A%25228AAA8C2A-92F2-451A-A6EA-97E008D8AEBA%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=8AAA8C2A-92F2-451A-A6EA-97E008D8AEBA&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-131798495-null-null.142^v100^pc_search_result_base2&utm_term=%E4%BD%BF%E7%94%A8%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE%E5%B9%B6%E4%BD%BF%E7%94%A8docker&spm=1018.2226.3001.4187