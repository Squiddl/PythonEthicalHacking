import socket
import os
import sys


# RCVALL_ON: receive all packages
def enable_promiscuous_mode(sniffer):
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


# RCVALL_OFF: receive only packages addressed to this host
def disable_promiscuous_mode(sniffer):
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


def is_windows():
    return os.name == 'nt'


TARGET_HOST_IP = '82.180.155.154'
MAX_PACKET_BYTES = 65565  # max size of an IP packet


def create_raw_socket(host_ip):
    try:
        # windows: sniff all packages, linux forces to specify protocol (Internet Control Message Protocol)
        socket_protocol = socket.IPPROTO_IP if is_windows() else socket.IPPROTO_ICMP

        # using ipv4/raw for low-level network interface access (no transport layer)
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host_ip, 0))  # listen on all ports (0)

        # include IP headers in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if is_windows():
            enable_promiscuous_mode(sniffer)

        return sniffer
    except socket.error as err:
        print(f"Socket creation failed with error: {repr(err)}")
        sys.exit(0)


# reads in a single packet and prints its contents
def sniff(sniffer):
    sniffed_packet = sniffer.recvfrom(MAX_PACKET_BYTES)[0]
    if is_windows():
        disable_promiscuous_mode(sniffer)
    print(sniffed_packet)


if __name__ == '__main__':
    print("Creating raw socket...")
    network_sniffer = create_raw_socket(TARGET_HOST_IP)
    print("Sniffing network traffic...")
    sniff(network_sniffer)
