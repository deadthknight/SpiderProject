#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！

from bs4 import BeautifulSoup
import requests
import re

map_dict = {'0': '4',
            '1': '6',
            '2': '0',
            '3': '2',
            '4': '7',
            '5': '1',
            '6': '8',
            '7': '9',
            '8': '3',
            '9': '5'}


def change_num(need_change_num_str):
    changed_num_list = []
    for x in need_change_num_str:
        changed_num_list.append(map_dict.get(x, x))
    return ''.join(changed_num_list)


class Courses:
    """
    分析,并且储存课程的类,传入的数据为课程的li标签
    """
    def __init__(self, course):
        # 找到课程名字,并且存储为self.courses_name属性
        self.courses_name = course.find('h3', class_='kc-course-card-name').get('title')
        # 找到课程报名人数,并且存储为self.courses_students属性
        self.courses_students = course.find('span', class_=re.compile("^kc-course-card-student-apply-num.*")).text.split('人')[0].strip()
        # 找到课程价格,并且存储为self.courses_price属性
        price_result = course.find('span', class_=re.compile("^kc-coursecard-price.*"))
        self.courses_price = price_result.text if price_result else '免费'

    def __repr__(self):
        # 格式化类的打印输出字符串
        return "课程名: {} \n 课程报名人数: {} \n 课程价格: {} \n".format(self.courses_name,
                                                             self.courses_students,
                                                             self.courses_price)


# 获取任何一个方向direction, 任何一页id的内容
def getpage(direction, id):
    client = requests.session()
    url = "https://ke.qq.com/course/list/" + direction + "?page=" + str(id)
    qqketang_page = client.get(url)

    # lxml HTML 解析器
    qqketang_page_soup = BeautifulSoup(qqketang_page.text, 'lxml')
    # 找到每一个课程'li'标签,直接放入page_courses_list列表
    course_card_items = qqketang_page_soup.find('div', class_="course-list").find_all('div',
                                                                                      class_='kc-course-card-content')
    page_courses_list = []
    for course in course_card_items:
        page_courses_list.append(Courses(course))

    return page_courses_list


if __name__ == "__main__":
    # print(change_num('0922.22'))
    print(getpage("ccie", 1))
