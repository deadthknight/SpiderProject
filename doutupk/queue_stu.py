import requests
from lxml import etree
import queue
from threading import Thread
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

class Downloader(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_file(url)
            finally:
                self.queue.task_done()

    def download_file(self, url):
        try:
            filename = url.split('/')[-1]
            if filename.endswith('.gif'):
                file = requests.get(url, headers=headers).content
                with open(filename, 'wb') as f:
                    f.write(file)
        except Exception as e:
            print(f"下载 {url} 时出错: {e}")

def get_source_pages(page):
    url = f'https://www.doutupk.com/article/list/?page={page}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    return response.text

def get_urls(page):
    file = get_source_pages(page)
    tree = etree.HTML(file)
    pic_urls = tree.xpath('//*[@class="col-xs-6 col-sm-3"]/img/@data-original')
    return pic_urls

def main():
    queue_of_urls = queue.Queue()

    # 生产者：将所有页面的图片URL放入队列
    for page in range(1, 10):
        urls = get_urls(page)
        for url in urls:
            queue_of_urls.put(url)

    # 创建消费者线程并启动
    start_time = time.time()
    num_threads = 30  # 可以根据实际情况调整线程数量
    for _ in range(num_threads):
        downloader = Downloader(queue_of_urls)
        downloader.daemon = True  # 设置为守护线程，主线程结束时自动退出
        downloader.start()

    # 等待所有任务完成
    queue_of_urls.join()

    # 打印操作时间
    end_time = time.time()
    print("全部下载完毕！！！")
    print('本次操作时间: %.2f 秒' % (end_time - start_time))

if __name__ == "__main__":
    main()
