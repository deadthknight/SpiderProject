# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import os.path

from DrissionPage import ChromiumPage, ChromiumOptions
# import ddddocr
import json


def click_img(yzm_xy):
    # # 鼠标点击图片输出该点像素坐标  pip install opencv-python --upgrade   pip install opencv-contrib-python
    import cv2
    # 鼠标点击事件的回调函数
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # 在图片上画一个圆标记鼠标点击的点
            cv2.circle(img, (x, y), 1, (0, 255, 0), -1)

            # 输出鼠标点击处的像素坐标
            print(f"鼠标点击处的像素坐标：({x}, {y})")

            # 获取点击处的像素颜色值
            pixel_color = img[y, x]
            print(f"像素颜色值：{pixel_color}")

    img = cv2.imread('./captcha.jpg')  # 读取图片，输入需要点击的图片的路径
    cv2.namedWindow('image')  # 创建图片显示窗口
    cv2.setMouseCallback('image', mouse_callback)  # 设置鼠标回调函数
    while True:
        cv2.imshow('image', img)  # 在窗口中显示图片
        if cv2.waitKey(1) == 27:  # 按下ESC键退出循环
            break
    cv2.destroyAllWindows()  # 关闭窗口


co = ChromiumOptions()
# co.set_browser_path()  #浏览器地址，默认是chrome
co.headless(False)  # 无头模式
co.incognito(True)  # 无痕模式
co.set_pref('credentials_enable_service', True)  # 阻止“自动保存密码”的提示气泡
co.set_argument('--hide-crash-restore-bubble')  # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
page = ChromiumPage(co)
# page.set.auto_handle_alert(all_tabs=True)  # 这之后出现的弹窗都会自动确认
page.get("http://www.ccgp-yunnan.gov.cn/page/procurement/procurementList.html")
print(f'=======加载状态=======\n'
      f'是否在加载中：{page.states.is_loading}\n'
      f'是否在加载完成：{page.states.ready_state}')
# page.refresh(ignore_cache=True)   #网站刷新 忽略缓存
page.wait.ele_displayed('x://a[@data-page="next"]')  #等待next这个元素出现
page.ele('x://a[@data-page="next"]').click()  # 点击next 出发验证码弹窗
page.wait(1, 3)  #随机等待 1 到 3 秒之间的时间
print('要点击到文字', page('.verify-msg').text)
# print('要点击到文字', page('x://span[@class="verify-msg"]').text)
# ====================================================
img_obj = page(".back-img")
if os.path.exists('./captcha.jpg'):
    os.remove('./captcha.jpg')
img_obj.save('./', name='captcha.jpg')  #保存验证码图片
yzm_xy = list()
click_img(yzm_xy)
print('点击到坐标是', yzm_xy)
for xy in yzm_xy:
    page.actions.move_to(img_obj, offset_x=int(xy['x'] / 310 * 300), offset_y=int(xy['y'] / 155 * 175),
                         duration=.1).click()
    page.wait(1, 3)
