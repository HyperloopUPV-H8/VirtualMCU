from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from enum import Enum
import socket

class FDCAN:
    class DLC(Enum):
        BYTES_0 = 0x00000000
        BYTES_1 = 0x00010000
        BYTES_2 = 0x00020000
        BYTES_3 = 0x00030000
        BYTES_4 = 0x00040000
        BYTES_5 = 0x00050000
        BYTES_6 = 0x00060000
        BYTES_7 = 0x00070000
        BYTES_8 = 0x00080000
        BYTES_12 = 0x00090000
        BYTES_16 = 0x000A0000
        BYTES_20 = 0x000B0000
        BYTES_24 = 0x000C0000
        BYTES_32 = 0x000D0000
        BYTES_48 = 0x000E0000
        BYTES_64 = 0x000F0000
        DEFAULT = 0xFFFFFFFF

    dlc_to_len = {
        DLC.BYTES_0: 0,
        DLC.BYTES_1: 1,
        DLC.BYTES_2: 2,
        DLC.BYTES_3: 3,
        DLC.BYTES_4: 4,
        DLC.BYTES_5: 5,
        DLC.BYTES_6: 6,
        DLC.BYTES_7: 7,
        DLC.BYTES_8: 8,
        DLC.BYTES_12: 12,
        DLC.BYTES_16: 16,
        DLC.BYTES_20: 20,
        DLC.BYTES_24: 24,
        DLC.BYTES_32: 32,
        DLC.BYTES_48: 48,
        DLC.BYTES_64: 64
    }
    class Packet:
        def __init__(self, identifier: int, data_length: "FDCAN.DLC"):
            self.rx_data = b""
            self.identifier: int = identifier
            self.data_length: FDCAN.DLC = data_length
    
    _ip: str = ""
    _sock = None
    _port:int = None
            
            
   
    def __init__(self, TX: Pinout, RX: Pinout):
        self._TX = SharedMemory.get_pin(TX, memory.PinType.FDCAN)
        self._RX = SharedMemory.get_pin(RX, memory.PinType.FDCAN)
    
    def start(self, ip: str, port: int):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._port = port
        self._ip = ip
        self._sock.bind((self.ip,self.port))
    
        
    def transmit(self, message_id: int, data:list[bytes], data_length: "FDCAN.DLC")->bool:
        data_length = self.dlc_to_len[data_length]
        aux_data = b""
        aux_data += (message_id >> 24)
        aux_data += (message_id >> 16)
        aux_data += (message_id >> 8)
        aux_data += (message_id)
        aux_data += (data_length >> 24)
        aux_data += (data_length >> 16)
        aux_data += (data_length >> 8)
        aux_data += (data_length)
        aux_data += data
        totalsent = 0
        while totalsent < len(aux_data):
            sent = self._sock.sendto(aux_data[totalsent:], (FDCAN.ip, self.port))
            if sent <=0:
                return False
            totalsent += sent
        return True
        
    def read(self )->Packet:
        aux_data = b""
        bytes_recv = 0
        while chunk_aux_data>0 or bytes_recv<72:
            chunk_aux_data= self._sock.recvfrom(72)
            aux_data += chunk_aux_data
            bytes_recv += len(chunk_aux_data)
        
        aux_identifier= (aux_data[0] << 24) | (aux_data[1] << 16) | (aux_data[2] << 8) | aux_data[3]
        aux_dlc = ((aux_data[4] << 24) | (aux_data[5] << 16) | (aux_data[6] << 8) | aux_data[7])
        self.Packet(aux_identifier, aux_dlc)
        self.Packet.rx_data = aux_data[8:]
        return self.Packet
            
            

        
        
        
        