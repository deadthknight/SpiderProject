# ！usr/bin/env Python3.11
# -*-coding:utf-8 -*-
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import base64

def encrypt_aes_ecb(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    # 使用 PKCS7 填充明文
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_plaintext)
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_aes_ecb(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = base64.b64decode(encrypted_text)
    decrypted_padded = cipher.decrypt(encrypted)
    # 移除填充
    decrypted = unpad(decrypted_padded, AES.block_size).decode('utf-8')
    return decrypted

# 示例
key = 'your_key_here_16b'  # 16 字节密钥
plaintext = 'Hello World'
encrypted_text = encrypt_aes_ecb(plaintext, key)
print(f'Encrypted: {encrypted_text}')
decrypted_text = decrypt_aes_ecb(encrypted_text, key)
print(f'Decrypted: {decrypted_text}')



# 在 pycryptodome 库中，AES 加密的密钥长度必须为 16 字节（128 位）、24 字节（192 位）或 32 字节（256 位）。
# 明文需要填充是因为 AES 算法要求输入数据的长度必须是块大小的整数倍。AES 算法的块大小是 16 字节（128 位）。
# 如果输入数据的长度不是 16 字节的倍数，AES 算法会无法处理不完整的块，因此需要填充以满足块大小的要求。
# 填充方式：

# 1:PKCS7 填充：PKCS7 填充是最常用的填充方案。它在明文的末尾添加字节，每个字节的值等于添加的字节数。
#   例如，如果需要填充 5 字节，则填充的字节值都是 0x05。

# 2: ISO 10126 填充：在明文的末尾添加随机字节，最后一个字节包含填充的字节数。

# 3: Zero Padding：用零填充到块大小的整数倍。虽然简单，但不如 PKCS7 安全，因为在某些情况下，数据可以被解析为原始数据