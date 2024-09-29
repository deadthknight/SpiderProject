# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import requests
from loguru import logger

# url_source= 'https://beijing.yiche.taocheche.com/all/'


def get_pg_source(url,page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    data = {
        "liveSwitch": 1,
        "terminal": 40,
        "aggreCarSeries": 0,
        "aggreCarbrands": 0,
        "bangMai": False,
        "bangMaiChe": False,
        "baseScore": 0,
        "bigArea": 0,
        "brandId": 0,
        "brandPro": 0,
        "canNonLocal": 2,
        "carAgeId": 0,
        "carBasicId": 0,
        "carLevel": 0,
        "carType": 0,
        "cityId": 201,
        "color": 0,
        "commonFlag": 4,
        "country": 0,
        "curCity": 0,
        "customizeSortFlag": 0,
        "days": 0,
        "directSaleCar": 0,
        "distanceKm": 0,
        "districtId": 0,
        "drivingMileageId": 0,
        "exhaust": 0,
        "financialPriceHigh": 0,
        "financialPriceLower": 0,
        "firstPic": 0,
        "gearBoxType": 0,
        "highAge": 0,
        "highDrivingMileage": 0,
        "highPrice": 0,
        "isAuthenticated": 0,
        "isCarId": 0,
        "isCheckReportJson": 0,
        "isDealerAuthorized": 0,
        "isDealerRecommend": 0,
        "isExcludeYDG": 0,
        "isJDActivity": 0,
        "isLicensePhoto": 0,
        "isLicensed": 0,
        "isNeglect": 0,
        "isNewCar": 0,
        "isShowMr": 0,
        "isShowRecom": 0,
        "isVideo": 0,
        "isWarranty": 0,
        "level": 0,
        "licenseCityId": 0,
        "liveBroadcast": 0,
        "loanFirstPayHigh": 0,
        "loanFirstPayLower": 0,
        "loanMonthPayHigh": 0,
        "loanMonthPayLower": 0,
        "loanUserid": 0,
        "lowAge": 0,
        "lowDrivingMileage": 0,
        "lowPrice": 0,
        "mainBrandId": 0,
        "newCarHighPrice": 0,
        "newCarLowPrice": 0,
        "noAudit": False,
        "notCity": 0,
        "notUcarID": 0,
        "orderDirection": 0,
        "pageIndex": f'{page}',
        "pageSize": 20,
        "picCount": 0,
        "price": 0,
        "provinceId": 0,
        "publishTimeStatus": 0,
        "purchaseCityId": 0,
        "regions": False,
        "requestReferer": 0,
        "requestSource": 0,
        "returnCaryears": False,
        "score": 0,
        "scorePerformance": 0,
        "seatNumHigh": 0,
        "seatNumLower": 0,
        "seriesId": 0,
        "showPosition": 0,
        "siteIds": "5",
        "sortBoostFlag": 0,
        "sourceType": 0,
        "splitFlowAlgorithm": "",
        "startNum": 0,
        "supperiorId": 0,
        "uCarID": 0,
        "uCarStatus": "1",
        "useBlackUserList": False,
        "userID": 0,
        "userType": 0,
        "warrantyType": 0
    }
    response = requests.post(url=url,headers=headers,json=data)
    return response.json()

def parse_pg_source(pg_source):
    data = pg_source['data']['uCarBasicInfoList']['dataList']
    data_list = []
    for info in data:
        dic = {'价格': info['activityPriceText'],
               '名称': info['carName'],
               '上牌时间':info['carYear'],
               '城市': info['cityName'],
               '里程':info['drivingMileageText'],
               '链接': info['carLink'],
               }
        data_list.append(dic)
    # data_list = sorted(data_list,key=lambda x:float(x['价格'].replace('万','')))

    return data_list

def savedata():
    pass
def main():
    url = 'https://proconsumer.taocheche.com/c-car-consumer/carsource/getUcarLocalList'
    total = []
    for page in range (1,11):
        pg_source = get_pg_source(url,page)
        data_list = parse_pg_source(pg_source)
        total.extend(data_list)

    total = sorted(total,key=lambda x:float(x['价格'].replace('万','')))
    for data in total:
        print(data)


if __name__ == "__main__":
    main()
