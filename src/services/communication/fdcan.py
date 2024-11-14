class FDCANSocket:
    class Packet:
        id = 0
        dlc = 0
        payload = []

    def __init__(self, lip, lport, rip, rport): ...

    def recv(self) -> Packet: ...
    def transmit(self, packet: Packet): ...
