# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-

import execjs   #pip install execjs
from loguru import logger
url = 'http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/1157403.jhtml'
with open ('example_01_aes.js','r', encoding='utf-8') as f:
    ctx = execjs.compile(f.read())
true_url = ctx.call('req', url)
# print(true_url)

logger.info(f'详情的url：{url}   = ===>>>实际的url：{true_url}')

from  Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def encrypt_aes_ecb(plaintext, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size,style='pkcs7')  #默认就是PKCS7填充
    encrypted = cipher.encrypt(padded_plaintext)
    return base64.b64encode(encrypted).decode('utf-8')

list_url = 'http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/1157403.jhtml'
plaintext = list_url.split('/')[-1].rstrip('.jhtml')
key = 'qnbyzzwmdgghmcnm'
encrypted_list_url = encrypt_aes_ecb(plaintext, key).replace('/','^')[:-2]
true_url_py = list_url.replace(plaintext,encrypted_list_url)
logger.info(f'实际url：{true_url_py}')