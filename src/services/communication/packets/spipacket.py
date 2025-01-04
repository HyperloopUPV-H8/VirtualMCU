import struct


class SPIPacket:
    def __init__(self, types):
        self.types = types

    def parse(self, data: bytes) -> tuple:
        if struct.calcsize(self.types) != len(data):
            raise Exception("data size doesn't adjust to defined types")
        return struct.unpack(self.types, data)
    
    def build(self, *data) -> bytes:
        if struct.calcsize(self.types) != len(data):
            raise Exception("data size doesn't adjust to defined types")
        return struct.pack(self.types, data)