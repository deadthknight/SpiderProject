# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import random
import datetime
today = datetime.date.today()
lst = []
for i in range(30):
    lst.append('Unit' + str(i + 1))
read = random.sample(lst,5)
print(today)
print(read)
