# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import logging

# 设置日志记录配置  所有文件日志写在同一个文件里面
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# 例子===============================================================
#
# import logging
#
# # 设置基本配置
# logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')
#
# try:
#     # 代码块可能会引发异常
#     x = 1 / 0
#     print(x)
# except :
#     # 捕获异常并记录到日志
#     logging.error("发生了错误", exc_info=True)


# 例子封装===================================================================
# import logging
#
# # 设置基本配置
# logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')
#
# def log_exception(context, exc):
#     logging.error(f"发生了错误 - {context}", exc_info=exc)
#
# try:
#     # 代码块可能会引发异常
#     x = 1 / 0
# except Exception as e:
#     log_exception("在计算 x 时", e)
#
# try:
#     # 另一段代码块可能会引发异常
#     y = int("abc")
# except Exception as e:
#     log_exception("在转换 y 时", e)
#=====================================================================================
# 如果想要把日志记录在不同的文件中

# # 创建一个操作日志的对象logger（依赖FileHandler）
# file_handler = logging.FileHandler('l1.log', 'a', encoding='utf-8')  # f = open()
# file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s"))
#
# logger1 = logging.Logger('财务系统', level=40)  # 创建日志对象
# logger1.addHandler(file_handler)  # 给日志对象设置文件信息
#
#
# # 再创建一个操作日志的对象logger（依赖FileHandler）
# file_handler2 = logging.FileHandler('l2.log', 'a', encoding='utf-8')
# file_handler2.setFormatter(logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s"))
#
# logger2 = logging.Logger('会计系统', level=40)
# logger2.addHandler(file_handler2)


from loguru import logger

logger.add("file.log", format="{time} {level} {message}")

logger.info("This message has a custom format")
