import socket


target_host = '127.0.0.1'
target_port = 9998
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP
client.connect((target_host, target_port))
client.send(b"GET / HTTP/1.1\r\nHost: 127.0.0.1:9998\r\n\r\n")

response = client.recv(4096)
print(response.decode())
client.close()
