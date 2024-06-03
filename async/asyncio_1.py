#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import asyncio
import time

async def fun1():
    print ("starting1")
    await asyncio.sleep(2)
    print ("ending1")
    return 1
async def fun2():
    print ("starting2")
    await asyncio.sleep(2)
    print ("ending2")
    return 2

async def main():
    print(time.strftime("%X"))
    print("starting main")

    task1 = asyncio.create_task(fun1())
    task2 = asyncio.create_task(fun2())

    # response1 = await task1
    # response2 = await task2

    ret = await asyncio.gather(task1,task2)

    print(ret)
    # print(response1)
    # print(response2)

    print ("ending main")
    print (time.strftime("%X"))
asyncio.run(main())

# 16:39:42
# starting main
# starting1
# starting2
# ending1
# ending2
# 1
# 2
# ending main
# 16:39:44




if __name__ == "__main__":
    pass
