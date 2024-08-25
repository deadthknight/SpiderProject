# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('http://deal.ggzy.gov.cn/ds/deal/dealList.jsp')
select_tag = page('#provinceId')
select_tag.select('北京')