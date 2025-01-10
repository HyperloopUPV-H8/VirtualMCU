import struct


class SPIPacket:
    """Class used to facilitates structured data transmission/reception through SPI.

    Args:
        types: format that defines data type in the packet.
            See https://docs.python.org/es/3.13/library/struct.html#format-strings
    """

    def __init__(self, types: str):
        self.types = types

    def parse(self, data: bytes) -> tuple:
        """Transforms binary data into the distinct values based on defined types.

        Args:
            data: binary data received through SPI
        """
        if struct.calcsize(self.types) != len(data):
            raise Exception("data size doesn't adjust to defined types")
        return struct.unpack(self.types, data)

    def build(self, *data) -> bytes:
        """Transforms the values given into binary data, ready to send through SPI

        Args:
            *data: all values you want to send, based on defined types
        """
        if struct.calcsize(self.types) != len(data):
            raise Exception("data size doesn't adjust to defined types")
        return struct.pack(self.types, data)
