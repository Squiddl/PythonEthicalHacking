import os
import paramiko
from paramiko.common import  OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED, AUTH_SUCCESSFUL
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, channel_id):
        return OPEN_SUCCEEDED if kind == "session" else OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'username' and password == 'password':
            return AUTH_SUCCESSFUL


if __name__ == '__main__':
    server = '192.168.178.69'
    ssh_port = 22
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed ', str(e))
    else:
        print('[*] Got a connection!', client, addr)

        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(HOSTKEY)
        server = Server()
        bhSession.start_server(server=server)
        chan = bhSession.accept(20)
        if chan is None:
            print('[-] No channel.')
            sys.exit(1)
        print('[*] Authenticated!')
        print(chan.recv(1024))
        chan.send(b'Welcome to bh_ssh')
        try:
            while True:
                command = input('Enter command: ')
                if command != 'exit':
                    chan.send(b'command')
                    print(chan.recv(8096).decode())
                else:
                    chan.send(b'exit')
                    print('exiting')
                    bhSession.close()
                    break
        except KeyboardInterrupt:
            bhSession.close()
