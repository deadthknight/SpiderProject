# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from functools import wraps
import time


def run_time():
    def decorator(func):
        @wraps(func)  # 保持func.__name__ func.__doc__
        def print_run_time(*args, **kwargs):  # (*args, **kwargs) 可以接受任意参数
            # 装饰器添加的功能
            t1 = time.time()
            func_result = func(*args, **kwargs)
            t2 = time.time()
            print('本次操作时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
            return func_result  # 返回函数

        return print_run_time  # 返回函数 + 写入返回内容到文件

    return decorator  # 返回函数 + 写入返回内容到文件 + 保持func.__name__ func.__doc__


if __name__ == '__main__':
    # def wrapper(fn):
    #     def inner(*args, **kwargs):
    #         for i in range(5):
    #             ret = fn(*args, **kwargs)
    #         return ret
    #     return inner
    # @wrapper
    # def func(a):
    #     print(a)
    #
    # func('a')

    # 通用装饰器写法
    # def wrapper(fn):
    #     def inner(*args, **kwargs):
    #         ‘’‘执行目标函数之前’‘’
#             ret = fn(*args, **kwargs)
    #         ‘’‘执行目标函数之后’‘’
    #         return ret
    #     return inner
    # @wrapper
    # def func(a):
    #     print(a)
    #         return ret
    #     return inner


    # @wrapper
    # def func(a):
    #     pass
    #
    # func('a')

    def wraggper(fn):
        def inner(*args, **kwargs):
            start_time = time.time()
            ret = fn(*args, **kwargs)
            end_time = time.time()
            print('本次操作时间: %.2f' % (end_time - start_time))
            return ret
        return inner
    @wraggper
    def func(n):
        time.sleep(n)

    func(1)
