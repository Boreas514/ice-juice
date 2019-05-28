import os

read_file = receive(client_socket)
if os.path.exists(read_file):
    if os.path.isfile(read_file):
        try:
            with open (read_file,'rb') as n:
                send(client_socket,'SUCCESS')
                line = n.read(1024)
                while line:
                    send(client_socket,line)
                    line=n.read(1024)
                send(client_socket, st_complete)
        except Exception as e:
            err = f'[!] {e}'
            send(client_socket,err)
    else:
        err = f"ERROR: {read_file}/: Is a directory\n"
        send(client_socket, err)
else:
    err = f"ERROR: {read_file}: No such file or directory\n"
    send(client_socket,err)
