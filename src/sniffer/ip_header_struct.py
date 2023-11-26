import struct
import ipaddress


class IPHeaderStruct:
    """
          <     Little-endian
          B     1-byte unsigned char
          H     2-byte unsigned short
          s     byte array (must be specified), e.g. 4s for 4-byte array)
    """
    format = "<BBHHHBBH4s4s"

    def __init__(self, buffer):
        header = struct.unpack(IPHeaderStruct.format, buffer)

        # assign version-variable only high-order nibble (4 bits)
        self.version = header[0] >> 4  # 0101 0110 >> 4 = 0000 0001

        # assign internet_header_length-variable only low-order nibble (4 bits)
        self.internet_header_length = header[0] & 0xF  # 0101 0110 & 0000 1111 = 0000 0110
        self.type_of_service = header[1]
        self.total_length = header[2]
        self.identification = header[3]
        self.offset = header[4]
        self.time_to_live = header[5]
        self.protocol_num = header[6]
        self.checksum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # readable IP's
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}