
if win_client():
    resp=run_command('netsh firewall show state')
if osx_client():
    resp = run_command('/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate')
    resp += run_command('/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode')

send(client_socket,resp)
