import sys
import socket
import threading

'''
TCP-Proxies to help you understand unknown protocols/traffic in a network. 
Inspection -> Modification -> Sending
'''

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


# output packet details through the proxy in real time (hex & ascii)
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i + length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c): 02X}' for c in word])
        hex_width = length * 3
        results.append(f'{i:04x} {hexa:<{hex_width}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results


# receiving data from the two ends of the proxy
def receive_from(connection: socket):
    buffer = b''
    connection.settimeout(5)  # increase timeout if you are proxying traffic over lossy networks
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except ConnectionError as e:
        print('[*] Connection lost.\n', e)
    finally:
        return buffer


# TODO perform fuzzing tasks, check authentication issues (admin instead of own username)
def request_handler(buffer):
    # perform request packet modifications
    return buffer


def response_handler(buffer: bytes) -> bytes:
    # perform response packet modifications
    return buffer


def proxy_handler(client_socket: socket, remote_host: str, remote_port: int, receive_first: bool):
    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    remote_buffer = receive_from(connection=remote_socket)
    # check if a connection and request data is needed (e.g. FTP servers sending banners)
    if receive_first:
        hexdump(src=remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print(f"[<==] Sending {len(remote_buffer)} bytes to localhost.")
        client_socket.send(remote_buffer)

    # read from local|remote client, process data, send to remote|local client
    while True:
        # read from local client, process data, send to remote client
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print(f"[<==] Received {len(local_buffer)} bytes from localhost.")
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # read from remote client, process data, send to local client
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[==>] Sent to localhost.")

        # check if there's data left on both sides of connection
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # binding server socket to the local host
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"Problem on bind: {repr(e)}")

        print(f"[!] Failed to listen on {local_host}:{local_port}")
        print(f"[!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print(f"[*] Listening on {local_host}:{local_port}")
    server.listen(5)

    # Hand off fresh connections to the proxy_handler in a new thread
    while True:
        client_socket, addr = server.accept()
        # display information about local connection
        print(f"[*] Received incoming connection from {addr[0]}:{addr[1]}")
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 192.168.178.69 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    receive_first = True if "True" in receive_first else False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == '__main__':
    main()
    