import struct

# length calculation is based on the IP header
# number of 32-bit words (4-byte chunks)
class ICMPHeader:
    """ multiplying this field """
    def __init__(self, buffer):
        header = struct.unpack('<BBHHH', buffer)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]
    # type value of 3 --> corresponds to the Destination Unreachableclass of ICMP messages
    # code value of 3 --> indicates that the Port Unreachable error has been caused