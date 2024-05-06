import struct

# length calculation based on the IP header
#4-byte chunks

class ICMPHeader:
    
    def __init__(self, buffer):
        header = struct.unpack('<BBHHH', buffer)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]
    