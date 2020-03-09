
import socket
import struct
from st_encryption import *

st_eof = base64.b64decode('V2hhdCBpcyB0aGUgbWVhbmluZyBvZiBsaWZl')
st_complete = base64.b64decode('NDI=')

def recvall(sock, count, size=False):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    if size: return buf
    else: return decrypt(buf)

def send(sock, data, encryption=True):
    while data:
        if encryption:
            cmd = encrypt(data[:1024])
        else:
            cmd = data[:1024]
        length = len(cmd)
        sock.sendall(struct.pack('!i', length))
        if type(cmd) is not bytes:
            cmd = cmd.encode()
        sock.sendall(cmd)
        data = data[1024:]
    if encryption:
        eof = encrypt(st_eof)
    else:
        eof = st_eof
    eof_len = len(eof)
    sock.sendall(struct.pack('!i', eof_len))
    sock.sendall(eof)

def receive(sock,silent=False,timeout=True):
    full_response=b''
    while True:
        lengthbuf = recvall(sock, 4, size=True)
        length, = struct.unpack('!i', lengthbuf)
        response = recvall(sock, length)
        if response != st_eof:
            full_response += response
        else:
            break
    return full_response
