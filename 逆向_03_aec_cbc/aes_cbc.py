from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from binascii import unhexlify, a2b_hex
import requests


# def aes_decrypt_text(encrypt_text, key, iv):
#     # Step 1: Parse the hex string to bytes
#     hex_bytes = unhexlify(encrypt_text)
#
#     # Convert key and iv to bytes
#     key_bytes = key.encode('utf-8')
#     iv_bytes = iv.encode('utf-8')
#
#     # Create AES cipher for decryption
#     cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
#
#     # Decrypt the data
#     decrypted_bytes = cipher.decrypt(hex_bytes)
#
#     # Unpad and decode the decrypted bytes
#     decrypted_text = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
#
#     return decrypted_text


def aes_decrypt_text(encrypt_text, key, iv, model="CBC"):
    aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode("utf-8"))
    decrypt_text = aes.decrypt(a2b_hex(encrypt_text)).decode("utf-8")
    return decrypt_text


key = 'Dt8j9wGw%6HbxfFn'
iv = '0123456789ABCDEF'
headers = {
    "Referer": "https://jzsc.mohurd.gov.cn/data/company",
    "v": "231012",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

url = 'https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list'
params = {"pg": "0", "pgsz": "15", "total": "0"}
res = requests.get(url, headers=headers, params=params)
# print(res.text)

# Assume the response text is in hex string format
decrypt_text = aes_decrypt_text(res.text, key=key, iv=iv)
print(decrypt_text)
