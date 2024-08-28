#!/usr/bin/env python3.11
# -*- coding:utf-8 -*-
import os
from DrissionPage import ChromiumPage, ChromiumOptions
import cv2
from PIL import Image

def click_img(yzm_xy):
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
            yzm_xy.append((x, y))
            print(f"鼠标点击处的像素坐标：({x}, {y})")

    img = cv2.imread('./captcha.jpg')
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_callback)
    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(1) == 13:  # 按下回车键退出循环
            break
    cv2.destroyAllWindows()


def main():
    co = ChromiumOptions()
    co.headless(False)  # 关闭无头模式，显示浏览器
    co.incognito(True)  # 开启无痕模式
    co.set_pref('credentials_enable_service', True)  # 阻止“自动保存密码”的提示
    co.set_argument('--hide-crash-restore-bubble')  # 阻止“要恢复页面吗？”的提示
    page = ChromiumPage(co)

    page.get("http://www.ccgp-yunnan.gov.cn/page/procurement/procurementList.html")
    print(f'=======加载状态=======\n'
          f'是否在加载中：{page.states.is_loading}\n'
          f'是否在加载完成：{page.states.ready_state}')

    page.wait.ele_displayed('x://a[@data-page="next"]')  # 等待 'next' 元素出现
    page.ele('x://a[@data-page="next"]').click()  # 点击 'next' 出发验证码弹窗
    page.wait(1, 3)  # 随机等待 1 到 3 秒之间的时间

    print('要点击到文字', page('.verify-msg').text)

    img_obj = page(".back-img")
    if os.path.exists('./captcha.jpg'):
        os.remove('./captcha.jpg')
    img_obj.save('./', name='captcha.jpg')  # 保存验证码图片
    # 打开图像文件
    img = Image.open('captcha.jpg')

    # 获取图像尺寸
    image_width, image_height = img.size
    print(f"Image Width: {image_width}, Image Height: {image_height}")    #下载的图片大小

    yzm_xy = list()  # 初始化坐标列表
    click_img(yzm_xy)  # 将列表传递给 click_img 函数

    print('点击到坐标是', yzm_xy)
    for xy in yzm_xy:
        # 下载的图片大小跟网页中的不一样 点选的坐标也不同，需要等比例调整
        page.actions.move_to(img_obj, offset_x=int(xy[0] / 310 * 350), offset_y=int(xy[1] / 155 * 175),
                             duration=.1).click()
        page.wait(1, 3)


if __name__ == "__main__":
    main()
