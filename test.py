# # ！usr/bin/env Python3.11
# # -*-coding:utf-8 -*-
# import re
#
# lst = ['很多免费的', '质量一般的', 'verygood']
# # lst.insert(1,'量很大')
# # print(lst)
# # lst.remove('质量  一般的'.replace(' ',''))
# # print(lst)
# # lst[2]=lst[2].upper()
# # print(lst)
#
# # 集合set 交集/并集/差集/
# a = {1, 2, 3, 4, 5}
# b = {4, 5, 6, 7, 8}
# # print(a.intersection(b))
# # print(a & b) # 交集
# # print(a.union(b))
# # print(a | b) # 并集
# # print(a.difference(b))
# # print(a - b) # 差集
#
# # 列表删除,循环删除会存在删不干净，
#
# # lst = ['11', '12', '13', '14']
# # for x in lst:
# #     if x.startswith('1'):
# #         lst.remove(x)
# # print(lst)
# # ['12', '14']
# # remove后列表内存会往前移动，所以会出现删不干��的现象
# # 方法一：
# # new_lst = []
# # for x in lst:
# #     if x.startswith('1'):
# #         new_lst.append(x)
# # for y in new_lst:
# #     lst.remove(y)
# # # print(lst)
# # # []
# # # 方法二：
# # for x in lst[:]:
# #     if x.startswith('1'):
# #         lst.remove(x)
# # # print(lst)
# #
# # # 字典删除，循环字典删除，删除数据的数据会报错
# #
# # dic = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
# # # for x in dic:  # dictionary changed size during iteration
# # #     dic.pop(x)
# # # 把要删除的键值放到一个列表中，循环删除
# # lst = list(dic.keys())
# # for x in lst:
# #     dic.pop(x)
# # # print(dic)
# #
# # a = [10, 20, 30, 40, 50, 60, 70, 80]
# # b = [10, 20, 30, 40, 50, 60, 70, 80]
# #
# # print(a == b)  # True ,判断两个内容的值是否一致
# # print(a is b)  # False,判断两个内容的内存地址是否一致
# #
# # # 一般用is来判空
# # c = []
# # if c:
# #     print('c is None')
# # else:
# #     print('c is not None')
# # # c is not None 条件 if c 检查变量 c 是否为“真”。对于列表，非空列表被认为是“真”，而空列表被认为是“假”。
# #
# # d = []
# # if d is None:
# #     print('d is None')
# # else:
# #     print('d is not None')
# # # d is not None 条件 if d is None 检查变量 d 是否为 None。然而，一个空列表 ([]) 不是 None，它是一个空容器。因此，在你的代码中，d 不是 None。
# #
# # str2 = '我的家'
# # str1 = str2.replace('我','你')
# # print(str1)
# #
# # # https://tool.chinaz.com/regex 正则表达式 测试
# # lst = [1,2,3]
# # m = map(lambda x:x*2,lst)
# # print(list(m))
#
# # lst = [{'1':'w'}, {'2':"w"}, {'1':"w"}]
# # x =   [dict(y) for y in   {tuple(x.items()) for x in lst}]
# # print(x)
#
# lst = ['1']
# str = ''.join(lst)
# print(str)
# import time
# n = 11
# for i in range(n):
#     if i == 0:
#         print("[" + '=' * i + ' ' * (n - i-1) + "]", end='\r')
#         time.sleep(0.5)
#     print("["+'=' * i + '>' + ' '*(n-i-1) + "]",end='\r')
#     time.sleep(0.5)


import time
# import sys
# n = 11
# for i in range(n):
#     if i == 0:
#         print("[" + ' ' * (n - 1) + "]", end='\r')  # 初始化进度条的起始状态
#         # sys.stdout.flush()  # 加上延迟效果以观察变化
#     print("[" + '=' * i + '>' + ' ' * (n - i - 1) + "]", end='\r')
#     # sys.stdout.flush()
#     # time.sleep(0.5)  # 加上延迟效果让进度条慢慢更新
# import time
# import sys
#
# n = 11
# for i in range(n):
#     if i == 0:
#         print("[" + ' ' * (n - 1) + "]", end='\r')  # 初始化进度条的起始状态
#         sys.stdout.flush()  # 手动刷新输出缓冲区
#
#     print("[" + '=' * i + '>' + ' ' * (n - i - 1) + "]", end='\r')
#     sys.stdout.flush()  # 手动刷新输出缓冲区
#     time.sleep(0.5)  # 延迟0.5秒，模拟进度更新
#
# print()  # 在最后添加换行以保持终端输出整洁
import time
import sys

# def print_progress_bar(iteration, total, bar_length=50):
#     percent = ("{0:.1f}".format(100 * (iteration / float(total))))
#     filled_length = int(bar_length * iteration // total)
#     bar = '=' * filled_length + '>' + ' ' * (bar_length - filled_length - 1)
#     sys.stdout.write(f'\r[{bar}] {percent}% Complete')
#     sys.stdout.flush()
#
# n = 11  # 进度条总长度
#
# for i in range(n + 1):
#     print_progress_bar(i, n)
#     time.sleep(0.5)  # 模拟进度更新的延迟
#
# print("\nDone")  # 结束时换行，确保“Done”显示在新的一行

# ============================================================================
# 码点（Code Point）是字符集中的一个唯一标识符，用于表示特定的字符。在Unicode标准中，码点是一个非负整数，
# 每个字符对应一个唯一的码点。码点的格式通常表示为 U+XXXX，其中 XXXX 是一个十六进制数。例如：
#
# 字母“A”的码点是 U+0041

print(chr(0x0041))
print(chr(65))
print(ord('A'))
