# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from spider_kfc_restaurant import get_kfc_infor


class KFC:
    def __init__(self, description_dict):
        for key, value in description_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        return (
            f"店面: {self.storeName}店\n"
            f"地址: {self.addressDetail}\n"
            f"其他信息: {self.pro}\n"
        )


def kfc_final():
    keyword, kfc_num, infor = get_kfc_infor()
    # print(keyword, kfc_num, infor)
    print('='*50)
    print(f'{keyword}店面共有{kfc_num}家\n ')
    info_list = []
    for x in infor:
        print('='*50)
        y = KFC(x)
        print(f'{y}')
        info_list.append(y)
    return f'查询结束'


if __name__ == "__main__":
    print(kfc_final())
# {'addressDetail': '朝阳路杨闸环岛西北京通苑30号楼一层南侧',
#    'cityName': '北京市',
#    'pro': '24小时,Wi-Fi,点唱机,店内参观,礼品卡',
#    'provinceName': '北京市',
#    'rownum': 1,
#    'storeName': '京通新城'}
