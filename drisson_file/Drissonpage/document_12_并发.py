from DrissionPage import ChromiumPage, ChromiumOptions
from DataRecorder import Recorder
r = Recorder(path='company.xlsx',cache_size=500)  #创建文件
r.add_data(['公司名', '链接', '序号', "地址", "行业", "成立时间", "交易所", "上市时间", "募集资金", "IPO首日市值"]) #插入表头
# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式

page = ChromiumPage(co)
page.get('https://www.itjuzi.com/ipo')
