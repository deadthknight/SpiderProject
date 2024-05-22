#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

import requests

from douban.bs4_1_get_main_page import headers
from pprint import pprint
from bs4 import BeautifulSoup
import re


def get_top_movies(type,limit):
    url = 'https://movie.douban.com/j/chart/top_list?'
    param = {'type': type,
             'interval_id': '100:90',
             'action': None,
             'start': 0,
             'limit': limit}

    response = requests.get(url=url, params=param, headers=headers)

    get_top_list = response.json()

    get_top_list_final = []
    for get_top in get_top_list:
        # print(get_top)
        # movies(get_top)
        get_top_list_final.append({'电影名': get_top['title'],
                                   '电影排名': get_top['rank'],
                                   '电影id': get_top['id'],
                                   'url': get_top['url']})
    # print(get_top_list_final)

    for top in get_top_list_final:
        # print(top['url'])
        movie_response = requests.get(top['url'], headers=headers)
        movie_response_soup = BeautifulSoup(movie_response.text, 'lxml')
        # print(movie_response_soup)
        if movie_response_soup.title.text == '页面不存在':
            top.update({'概览': '无'})
        else:
            comments = movie_response_soup.find('div', class_='indent', id='link-report-intra')
            if comments.find('span', class_='all hidden'):
                comments = comments.find('span',class_='all hidden').text.replace('\r\n', '').strip()
                cleaned_comments = re.sub(r'\s+', ' ', comments).strip()
                cleaned_comments = re.split('©豆瓣', cleaned_comments)[0]
                # print(cleaned_comments)
                top.update({'概览': cleaned_comments})
            else:
                comments = comments.text.replace('\r\n', '').strip()
                cleaned_comments = re.sub(r'\s+', ' ', comments).strip()
                cleaned_comments = re.split('©豆瓣', cleaned_comments)[0]
                # print(cleaned_comments)
                top.update({'概览': cleaned_comments})


    return get_top_list_final


if __name__ == "__main__":
    type = input('输入电影类型:')
    limit  = input('输入查询排名:')
    pprint(get_top_movies(type,limit))
    # url = 'https://movie.douban.com/subject/1291561/'
    # movie_response = requests.get(url=url, headers=headers)
    # movie_response_soup = BeautifulSoup(movie_response.text, 'lxml')
    # comments = movie_response_soup.find('div', class_='indent', id='link-report-intra')
    # if comments.find('span', class_='all hidden'):
    #     comments = comments.find('span',class_='all hidden').text.replace('\r\n', '').strip()
    #     cleaned_comments = re.sub(r'\s+', ' ', comments).strip()
    #     cleaned_comments = re.split('©豆瓣', cleaned_comments)[0]
    #     print(cleaned_comments)
    # else:
    #     print(comments.text)