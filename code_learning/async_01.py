# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import asyncio
import time

async def say_after(delay,what):
    await asyncio.sleep(delay)
    return f'{what}-{delay}'


# gather 会转化为task
# async def main():
#     print(f'started at {time.strftime("%X")}')
#
#     ret = await asyncio.gather(say_after(1,'hello'),say_after(2,'world'))
#     print(ret)
#
#     print(f'finished at {time.strftime("%X")}')


async def main():
    print(f'started at {time.strftime("%X")}')

    # 创建 Task 对象
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    # 使用 asyncio.gather 运行任务
    # ret = await asyncio.gather(task1, task2)
    # print(ret)
    ret1 = await (task1)
    ret2 = await (task2)
    print(f'ret1: {ret1}, ret2: {ret2}')
    print(f'finished at {time.strftime("%X")}')

asyncio.run(main())