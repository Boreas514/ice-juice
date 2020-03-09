import os
import sys
import zipfile

if win_client():
    temp = 'C:\\Windows\\Temp\\'
else:
    temp = '/tmp/'
cur_dir = os.getcwd()
content = ''
d_file = receive(client_socket).decode()
if temp in d_file:
    if os.path.exists(d_file):
        os.chdir(temp)
        d_file = os.path.basename(d_file)

d_file = d_file.strip('\\/')
d_zip = ''
d_zpath = ''

if os.path.exists(d_file):
    if os.path.isdir(d_file):
        d_zip = '{}.zip'.format(d_file)
        d_zpath = os.path.join(temp,d_zip)
        zipf = zipfile.ZipFile(d_zpath, 'w', zipfile.ZIP_DEFLATED)
        zipdir(d_file,zipf)
        zipf.close()
    else:
        if '.' in d_file and not d_file.startswith('.'):
            extension = d_file.index('.')
            d_base = d_file[:extension]
            d_zip = '{}.zip'.format(d_base)
        else:
            d_zip = '{}.zip'.format(d_file)
        d_zpath = os.path.join(temp,d_zip)
        zipf = zipfile.ZipFile(d_zpath, 'w', zipfile.ZIP_DEFLATED)
        zipf.write(d_file)
        zipf.close()
    d_size = os.stat(d_zpath)
    send(client_socket, str(d_size.st_size))
    with open (d_zpath, 'rb') as download:
        line = download.read(1024)
        while line:
            send(client_socket,line)
            line = download.read(1024)
    send(client_socket,'download complete')
    os.remove(d_zpath)
else:
    err = f"ERROR: could not find {d_file}"
    send(client_socket,err)
os.chdir(cur_dir)
