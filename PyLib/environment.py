import os

resp = ''
for n in os.environ:
    resp += "    {0:35}: {1}\n\n".format(n,os.environ.get(n))
resp = resp.replace(';','\n{0:39}: '.format(""))
send(client_socket,resp)