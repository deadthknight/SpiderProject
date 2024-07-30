import requests
from lxml import etree
import uuid
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


def get_page_source(url):
    response = requests.get(url, headers=headers)
    return response.text

def parse_pg_source(pg_source):
    tree = etree.HTML(pg_source) #type: etree._Element
    title = tree.xpath('//title/text()')
    content = tree.xpath('//div[@class="post_body"]')[0]
    html = etree.tostring(content,encoding='utf-8').decode('utf-8')
    img_list = content.xpath('.//img/@src')
    print(html)
    for x in img_list:
        img = requests.get(x, headers=headers)
        img_name = str(uuid.uuid4()).replace("-","")
        with open(f'{img_name}.jpg','wb') as f:
            f.write(img.content)
        html = html.replace(x,img_name)

    with open('NEWS.md','w',encoding='utf-8') as f:
        f.write(html)

def main():
    url = 'https://www.163.com/dy/article/J8AT6PEI05198NMR.html'
    main_pg_source = get_page_source(url)
    parse_pg_source(main_pg_source)

if __name__ == '__main__':
    main()

