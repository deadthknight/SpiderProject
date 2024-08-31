from DrissionPage import ChromiumPage, ChromiumOptions
from DataRecorder import Recorder
from loguru import logger

r = Recorder(path='company.xlsx', cache_size=500)  #创建文件
r.add_data(
    ['公司名', '链接', '序号', "地址", "行业", "成立时间", "交易所", "上市时间", "募集资金", "IPO首日市值"])  #插入表头

# 配置 ChromiumOptions
co = ChromiumOptions()
co.headless(False)  # 不使用无头模式
co.incognito(True)  # 使用无痕模式
page = ChromiumPage(co)


def get_info(href):
    tab = page.new_tab(href)
    company_detail = tab('.company-header-title').text
    company_detail_block = tab('.company-header-round').text
    company_detail_page = tab('x://*[@rel="noopener noreferrer"]').attr("href")
    logger.success(f'======>>>>>>{company_detail}-{company_detail_block}-{company_detail_page}')
    tab.close()


page.get('https://www.itjuzi.com/ipo')
row_list = page.eles('.el-table__row')
detail_all = []
for x in row_list:
    # num = x('x:./td[2]//text()')
    # print(num)
    detail = [td.text.strip().replace('\n', '-') for td in x.eles('x:.//td')[1:]]
    company = x('t:a').text
    href = x('t:a').attr('href')
    detail.insert(0, href)
    detail.insert(0, company)
    detail_all.append(detail)
    get_info(href)

#     r.add_data(detail)  # 加入数据
# r.record()
