# https://www.byhy.net/auto/selenium/01/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

wd = webdriver.Chrome(service=Service(r'/Users/vickyyang/Desktop/study/chromedriver-mac-x64/chromedriver'))
#隐式等待
wd.implicitly_wait(10)

# wd.get('https://cdn2.byhy.net/files/selenium/sample1.html')
#
# element = wd.find_element(By.TAG_NAME, 'head')
# print(element.find_element(By.TAG_NAME,'title').get_attribute('text'))
#
# element = wd.find_element(By.CLASS_NAME,'footer2').find_element(By.TAG_NAME,'a').get_attribute('href')
# print(element)
#
# input()

wd.get('https://www.baidu.com')
element = wd.find_element(By.ID, 'kw')
element.send_keys('日本环球影城')

element = wd.find_element(By.ID, 'su')
element.click()

element_href = wd.find_element(By.ID,'content_left').find_element(By.ID,'1').find_element(By.TAG_NAME,'a').get_attribute('href')
wd.get(element_href)

input('等待回车键结束程序')