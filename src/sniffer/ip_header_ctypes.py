from ctypes import *
import socket
import struct


class IPHeader(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),  # Internet Header Length
        ("version", c_ubyte, 4),
        ("tos", c_ubyte, 8),  # Type of Service
        ("len", c_ushort, 16),  # Total Length
        ("id", c_ushort, 16),  # Identification
        ("offset", c_ushort, 16),  # Flags + Fragment Offset
        ("ttl", c_ubyte, 8),  # Time to Live
        ("protocol_num", c_ubyte, 8),  # Protocol Number
        ("sum", c_ushort, 16),  # Checksum
        ("src", c_uint32, 32),  # Source IP Address
        ("dst", c_uint32, 32)  # Destination IP Address
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.src_ip_address = socket.inet_ntoa(struct.pack("<L", self.src))

        # readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # # readable protocol
        # try:
        #     self.protocol = self.protocol_map[self.protocol_num]
        # except Exception as err:
        #     print(f"Protocol not found: {repr(err)}")
        #     self.protocol = str(self.protocol_num)
