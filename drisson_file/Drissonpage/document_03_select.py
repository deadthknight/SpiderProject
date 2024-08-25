# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import ChromiumPage

page = ChromiumPage()
# page.get('http://deal.ggzy.gov.cn/ds/deal/dealList.jsp')
# # select_tag = page('#provinceId')
# # select_tag.select('北京')
# # page('#provinceId')('x:./option[2]').click()
# page('x://option[text()="山西"]').click()
# page('x://option[text()="太原市"]').click()
# page('x://option[text()="山西省公共资源交易平台"]').click()


page.get('https://www.jiansheku.com/search/personnel')
page('.el-input__icon el-icon-arrow-down').click()
# page('住建部人员资格').click()
# page('x://span[text()="一级注册建造师"]').click()
# page('x://span[text()="建筑工程"]').click()
