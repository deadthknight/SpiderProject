import logging

# 设置基本配置
logging.basicConfig(filename='error_log1.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def log_exception(context, exc):
    logging.error(f"发生了错误 - {context}", exc_info=exc)

try:
    # 代码块可能会引发异常
    x = 1 / 0
except Exception as e:
    log_exception("在计算 x 时", e)

try:
    # 另一段代码块可能会引发异常
    y = int("abc")
except Exception as e:
    log_exception("在转换 y 时", e)