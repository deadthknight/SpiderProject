# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
import json

import requests
from readheader import readheaders
import base64
from Crypto.Cipher import  AES
from hashlib import sha1
import binascii
from Crypto.Util.Padding import unpad   #去除padding
headers = readheaders('../http_header.txt')


url = 'https://api.weibotop.cn/currentitems'
response = requests.get(url=url,headers=headers)
# print(response.text)

key_s = "tSdGtmwh49BcR1irt18mxG41dGsBuGKS"
obj = sha1()
obj.update(key_s.encode('utf-8'))
key = obj.hexdigest()[:32]
# key_bs = binascii.a2b_hex(key)   #调用模块实现 key转为字节  方法一
key_bs = bytes.fromhex(key) #内置方法   方法二
# print(len(key_bs)) #验证key，aeskey 至少16位
encrypt_file = response.text
encrypt_file_bs = base64.b64decode(encrypt_file)     #o=n.enc.Base64.parse(i)
aes = AES.new(key=key_bs,mode = AES.MODE_ECB)         #mode:n.mode.ECB   key = r = a
# a->sha1 计算 -> 取前32位->hex转换
decrypt_file = aes.decrypt(encrypt_file_bs)
# print(decrypt_file)
decrypt_file = unpad(decrypt_file,16)

decrypt_file = decrypt_file.decode('utf-8')
print(type(decrypt_file))
lst = json.loads(decrypt_file)
for item in lst:
    print(item)