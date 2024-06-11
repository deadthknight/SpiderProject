# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import chardet
from readheader import readheaders

headers = readheaders('../http_header.txt')

url = 'https://www.shicimingju.com/bookmark/sidamingzhu.html'

response = requests.get(url=url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']
soup = BeautifulSoup(response.text, 'lxml')
book_list = soup.find_all('div', class_='book-item')
book_dic={}
book_list_final =[]
for book in book_list:
    book_name = book.find('h3').find('a').text
    book_url = 'https://www.shicimingju.com' + book.find('a')['href']
    # print(book_name, book_url)
    book_dic = {'name':book_name, 'url':book_url}
    book_list_final.append(book_dic)

print(book_list_final)