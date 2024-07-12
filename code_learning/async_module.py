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
    urls= ['www.baidu.com','www.sohu.com']
    # ...  获取 url 列表
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download_file(url)))
    await asyncio.wait(tasks)
    # await asyncio.gather(download_file(url))