#! /usr/bin/python3
import socket

from tabulate import tabulate

"""
"Banner Grabbing" is used to retrieve information of a service running its open ports.
The objective is to grab information regarding the utilized software, and hints about the operating system.
"""
common_ports = {
    "FTP": 21,
    "SSH": 22,
    "Telnet": 23,
    "SMTP": 25,
    "DNS": 53,
    "HTTP": 80,
    "HTTPS": 443,
    "POP3": 110,
    "IMAP": 143,
    "LDAP": 389,
    "LDAP SSL": 636,
    "SMB": 445,
    "NetBIOS": 139,
    "RDP": 3389,
    "VNC": 5900,
    "MySQL": 3306,
    "PostgreSQL": 5432,
    "SNMP": 161,
    "SNMP Trap": 162,
    "HTTP Alt": 8080,
    "HTTP Alt SSL": 8443,
    "RIP": 520,
    "PPTP": 1723,
    "TFTP": 69,
    "Syslog": 514,
    "NTP": 123,
    "NetFlow": 2055,
    "Bittorrent": 6881,
    "Discord": 443,
    "Steam": 27015,
    "Minecraft": 25565
}

ip_addr = "127.0.0.1"


def render_grabbed_banner():
    print(tabulate(headers=("Port", "Service", "Banner"),
                   tabular_data=[[port, service, banner]],
                   missingval="/",
                   colalign=("center", "center", "center"),
                   tablefmt="fancy_grid"))


if __name__ == '__main__':
    for service, port in common_ports.items():
        s = socket.socket()
        try:
            s.connect((ip_addr, port))
            banner = s.recv(100)
        except ConnectionRefusedError:
            banner = None
        finally:
            render_grabbed_banner()
            s.close()
