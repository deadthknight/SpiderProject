# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import asyncio
import aiohttp   #request
import aiofiles   #open


async def download_file(url):
    file_name = url.split("/")[-1]
    async with aiohttp.ClientSession() as session:  # session =request.session()
        async with session.get(url) as response:   # response = session.get()
            # page_source = await.response.text(encoding='utf-8') 源代码
            # json = await.response.json()  json 数据
            if response.status == 200:
                data = await response.content.read()
                # with open('image.jpg', 'wb') as f:    # 同步代码 慢
                #     f.write(data)
                async with aiofiles.open(file_name, mode='wb') as f:
                    await f.write(data)
                    print(f"File {file_name} downloaded successfully.")
async def main():
    urls= ['http://img.doutupk.com/production/uploads/image/2024/06/17/20240617588532_JyYsgQ.jpeg',
'http://img.doutupk.com/production/uploads/image/2024/06/17/20240617588532_wSVbLs.jpeg']
    # ...  获取 url 列表
    tasks = []
    # for url in urls:
    #     tasks.append(asyncio.create_task(download_file(url)))
    # await asyncio.wait(tasks)

    await asyncio.gather(*(download_file(url) for url in urls))


if __name__ == '__main__':

    import time
    t1 = time.time()
    asyncio.run(main())
    print("全部下载完毕！！！")
    t2 = time.time()
    print('本次操作时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间