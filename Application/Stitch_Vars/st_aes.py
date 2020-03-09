
# 生成的secret为二进制
import base64

aes_encoded = 'd3NXWFJXQVZWcEoxTHVJZ0NvNGdnbkI3cmtJZjFvYVY='
aes_abbrev = f'{aes_encoded[21]}{aes_encoded[0]}{aes_encoded[1]}{aes_encoded[43]}{aes_encoded[5]}{aes_encoded[13]}{aes_encoded[7]}{aes_encoded[24]}{aes_encoded[31]}{aes_encoded[35]}{aes_encoded[16]}{aes_encoded[39]}{aes_encoded[28]}'
secret=base64.b64decode(aes_encoded)