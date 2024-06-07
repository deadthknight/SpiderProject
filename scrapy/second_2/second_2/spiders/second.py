import scrapy
from second_2.items import Second2Item


class SecondSpider(scrapy.Spider):
    # 爬虫文件名称，唯一标识
    name = "second"
    # 允许的域名
    # allowed_domains = ["apply.daystaracademy.cn"]
    # 起始的url列表：该列表存放url会被scrapy自动进行请求发送
    start_urls = ["https://apply.daystaracademy.cn/"]

    def parse(self, response):

        # title = response.xpath('//*[@id="app"]/nav/div/a/@href')
        # print(f"Page title: {title}")
        # xpath 返回的列表，但列表元素是Selector 对象
        # Pagetitle: [ < Selector query = '//*[@id="app"]/nav/div/a/@href' data = 'https://apply.daystaracademy.cn' >]

        # extract() 可以将selector对象中的date提取出来
        title = response.xpath('//*[@id="app"]/nav/div/a/@href').extract()
        print(f"Page title: {title}")
        # Page title: ['https://apply.daystaracademy.cn']
        title1 = response.xpath('//*[@id="app"]/nav/div/a/@href').extract_first()
        print(f"Page title: {title1}")
        # Page title: https: // apply.daystaracademy.cn
        item = Second2Item()

