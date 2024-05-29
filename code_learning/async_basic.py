# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import asyncio


# 定义协程函数

async def fun():
    print('studying')
# await + 可等待的对象 （协程对象、task对象>io）



# fun()
asyncio.run(fun())
if __name__ == "__main__":
    pass
