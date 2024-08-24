# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import logging

# 设置基本配置
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

try:
    # 代码块可能会引发异常
    x = 1 / 0
    print(x)
except :
    # 捕获异常并记录到日志
    logging.error("发生了错误", exc_info=True)


