
import base64
from Crypto import Random
from Crypto.Cipher import AES

abbrev = '0d3=FEXN3JTvb'
T = base64.b64decode('d3NXWFJXQVZWcEoxTHVJZ0NvNGdnbkI3cmtJZjFvYVY=')

def encrypt(raw):
    if type(raw) is not bytes:
        raw = raw.encode()
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(T, AES.MODE_CFB, iv )
    return (base64.b64encode( iv + cipher.encrypt( raw ) ) )

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(T, AES.MODE_CFB, iv )
    return cipher.decrypt( enc[16:] )
