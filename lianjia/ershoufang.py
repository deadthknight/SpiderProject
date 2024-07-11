# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests

headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"}
name = input("请输入小区名称:")


def get_source_page(url,page):

    params = {"cityId": 110000,
              "condition": "%2Fpg"+ str(page)+"rs"+name,
              "curPage": page}
    response = requests.get(url,headers=headers,params=params)
    # print(response.request.url)
    return response.json()
def parse_source_page(source_page):
    total = []
    list = source_page["data"]["data"]["getErShouFangList"]["list"]
    for x in list:
        # title = x.get("title")
        # desc = x["desc"]
        # totalPrice = x["totalPrice"]
        # avgPrice = x["unitPrice"]
        title = x.get("title", "")
        desc = x.get("desc", "")
        totalPrice = x.get("totalPrice", "")
        avgPrice = x.get("unitPrice", "")
        if name in title or name in desc:
            dic = {"小区名称": name,
                   "详细信息": desc,
                   "总价": totalPrice,
                   "单价": avgPrice}
            total.append(dic)
    return total

def diff(data_list):
    # 使用集合去重
    data_set = {tuple(data.items()) for data in data_list}
    # 将元组转换回字典
    unique_list = [dict(item) for item in data_set]
    return unique_list

def main():
    url = "https://m.lianjia.com/liverpool/api/ershoufang/getList?"
    page = 1
    get_all= []
    while True:
        source_page = get_source_page(url,page)
        data = parse_source_page(source_page)
        get_all.extend(data)
        if source_page["data"]["data"]["getErShouFangList"]["hasMoreData"]==0:
            break
        page += 1
        # print(page)
    final = diff(get_all)
    return final



if __name__ == '__main__':
    total = main()
    print(len(total))
    total = sorted(total,key=lambda x:float(x["总价"].split('万')[0]))
    for i in total:
       print(i)




