import socket

target_host = "127.0.0.1"
target_port = 9997

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4, UDP
client.sendto(b"AAABBBCCC", (target_host, target_port))

data, addr = client.recv(4096)
print(data.decode())
client.close()
