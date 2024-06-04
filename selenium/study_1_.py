# https://www.byhy.net/auto/selenium/01/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

wd = webdriver.Chrome(service=Service(r'/Users/vickyyang/Desktop/study/chromedriver-mac-x64/chromedriver'))
#隐式等待
wd.implicitly_wait(5)

# wd.get('https://cdn2.byhy.net/files/selenium/sample1.html')

# element = wd.find_element(By.TAG_NAME, 'head')
# print(element.get_attribute('outerHTML'))
# print('='*30)
# print(element.get_attribute('innerHTML'))
# print(element.find_element(By.TAG_NAME,'title').get_attribute('text'))
# ==============================================================
# CSS 选择器
# elements = wd.find_elements(By.CSS_SELECTOR,'.animal')
# for element in elements:
#     print(element.text)

# id的话 需要#id
# elements = wd.find_elements(By.CSS_SELECTOR,'#inner11')
# for element in elements:
#     print(element.text)
# wd.quit()
# 根据class属性 选择元素的语法是在 class 值 前面加上一个点： .class值
# elements = wd.find_elements(By.CSS_SELECTOR,'.plant')
# for element in elements:
#     print(element.text)
# ===================================================================
# element = wd.find_element(By.CLASS_NAME,'footer2').find_element(By.TAG_NAME,'a').get_attribute('href')
# print(element)
# 对于input输入框的元素，要获取里面的输入文本，用text属性是不行的，这时可以使用 element.get_attribute('value')

wd.get('https://www.baidu.com')
element = wd.find_element(By.ID, 'kw')
element.send_keys('日本环球影城')

element = wd.find_element(By.ID, 'su')
element.click()

element_href = wd.find_element(By.ID, 'content_left').find_element(By.ID, '1').find_element(By.TAG_NAME,
                                                                                            'a').get_attribute('href')
wd.get(element_href)

input('等待回车键结束程序')

# 有时候，元素的文本内容没有展示在界面上，或者没有完全完全展示在界面上。 这时，用WebElement对象的text属性，获取文本内容，就会有问题。
# 出现这种情况，可以尝试使用 element.get_attribute('innerText') ，或者 element.get_attribute('textContent')
# 使用 innerText 和 textContent 的区别是，前者只显示元素可见文本内容，后者显示所有内容（包括display属性为none的部分）
