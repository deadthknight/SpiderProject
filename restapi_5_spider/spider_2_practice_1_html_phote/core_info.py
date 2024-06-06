#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐堂NetDevOps课程！


import os

# BS爬取的站点URL
web_page = 'https://flask.netdevops.com/spider'

# 下载图片存放的路径
# ------目录名-----==========当前文件========
# os.path.dirname(os.path.realpath(__file__))
download_dir = f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}download_img{os.sep}'


