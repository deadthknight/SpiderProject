# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import asyncio
import time


# 定义协程函数

async def fun():
    print('starting')
    await asyncio.sleep(3)
    print('ending')
# await + 可等待的对象 （协程对象、task对象>io）

async def main():
    urls = []
    tasks = []
    for url in urls:
        f = fun(url)
        t = asyncio.create_task(f)
        tasks.append(t)
    await asyncio.wait(tasks)


# fun()

if __name__ == "__main__":
    s1 = time.time()
    asyncio.run(fun())
    s2 = time.time()
    print(f"Time elapsed: {s2 - s1}")  # 3.0019984245300293
