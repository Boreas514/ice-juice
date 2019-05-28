
import os

no_error = True
posdir = '/\n'
windir = '\\\n'
complete = os.listdir('.')
c = ''
for n in complete:
    if os.path.isdir(n):
        if sys.platform.startswith('win'):
            c += '%s%s' %(n,windir)
        else:
            c += '%s%s' %(n,posdir)
    else:
        c += '%s\n' %n
send(client_socket, c)
path = get_path()
send(client_socket,path)
