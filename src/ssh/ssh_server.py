import os
import paramiko
from paramiko.common import OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED, AUTH_SUCCESSFUL
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
SSH_KEY_HOST = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, channel_id):
        return OPEN_SUCCEEDED if kind == "session" else OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # TODO pass key implementation
    def check_auth_password(self, username, password):
        return AUTH_SUCCESSFUL


if __name__ == '__main__':
    ip_server = '192.168.178.69'
    port_server = 2222
    try:
        ssh_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssh_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssh_listener.bind((ip_server, port_server))
        ssh_listener.listen(100)
        print('[+] Listening for connection ...')
        ssh_client, addr_client = ssh_listener.accept()
    except Exception as e:
        print('[-] Listen failed ', str(e))
    else:
        print('[*] Got a connection!', ssh_client, addr_client)

        ssh_session = paramiko.Transport(addr_client)
        ssh_session.add_server_key(SSH_KEY_HOST)
        ssh_server = SSHServer()
        ssh_session.start_server(server=ssh_server)

        # channel: sending/receiving over encrypted transport session (like a socket)
        channel = ssh_session.accept(20)
        if channel is None:
            print('[-] No channel.')
            sys.exit(1)
        print('[*] Authenticated!')
        print(channel.recv(1024))
        channel.send(b'Welcome to the SSH-Server.')
        try:
            while True:
                command = input('Enter command: ')
                if command == 'exit':
                    channel.send(b'exit')
                    ssh_session.close()
                    break
                channel.send(b'command')
                print(channel.recv(8096).decode())
        except KeyboardInterrupt:
            ssh_session.close()
