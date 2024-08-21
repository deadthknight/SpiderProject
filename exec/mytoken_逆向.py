import requests
from readheader import readheaders
import hashlib
import time

headers = readheaders('../http_header.txt')



def main():
    url = "https://api.mytokenapi.com/ticker/currencylistforall"

    r = str(int(time.time() * 1000))

    # 拼接字符串
    combined_string = r + "9527" + r[:6]

    # 使用 hashlib 生成哈希值
    e = hashlib.md5(combined_string.encode()).hexdigest()

    params = {"pages": "1,1",
              "sizes": "100,100",
              "subject": "market_cap",
              "language": "en_US",
              "timestamp": r,
              "code": e,
              "platform": "web_pc",
              "v": "0.1.0",
              "legal_currency": "USD",
              'international': "1"}
    response = requests.get(url=url, headers=headers, params=params)
    return response.json()


def parse_data(json):
    data = json["data"]['list']
    for x in data:
        print(x["symbol"])


if __name__ == '__main__':
    json = main()
    print(json)
    # data = parse_data(json)
