# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import random

# 假设你有一个包含unit的集合
unit_list= [f"unit{i}" for i in range(1, 31)]

selected_units = random.sample(unit_list, 5)

for x in  selected_units:
    print(f'要读的课文为:{x}')
