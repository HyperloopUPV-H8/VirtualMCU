import socket
import threading
import time
import struct
from queue import Queue
from typing import Optional

MAX_SIZE_PACKET = 1024
TIMEOUT_TIME = 2.0

class DatagramSocket:
    def __init__(self, lip, lport, rip, rport): 
        self.local_ip = lip
        self.remote_ip = rip
        self.local_port = lport
        self.remote_port = rport
        self._queue_packet_received = Queue()
        self._sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self._sock.bind((self.local_ip,self.local_port))
        self._sock.settimeout(TIMEOUT_TIME) 
        self._running = True
        self._recv_thread = threading.Thread(target=self._receive, daemon=True)
        self._recv_thread.start()      
    
    def _receive(self): 
        while self._running:
            try:
                data,address = self._sock.recvfrom(MAX_SIZE_PACKET)
                if address == (self.remote_ip,self.remote_port): #check if the receiving message comes from the ip address correct
                    self._queue_packet_received.put(data)
            except socket.timeout:
                continue
            except OSError as e:
                if self._running == False:
                    return
                print(f"Error while receiving data: {e}")
                break
        self._running = False
               
               
    def transmit(self, buf: bytes) -> int: 
        bytes_sent = 0
        try:
            while(bytes_sent < len(buf)):
                new_bytes_sent = self._sock.sendto(buf,(self.remote_ip,self.remote_port))
                bytes_sent += new_bytes_sent
        except OSError as e:
            print(f"Error while sending data: {e}")
            self.stop()
        return bytes_sent
    
    def get_packet(self) -> Optional[bytes]:
        if self._queue_packet_received.empty():
            return None
        return self._queue_packet_received.get()
    
    def stop(self):
        if not self._running:
            return
        self._running = False
        
        if self._recv_thread.is_alive():
            self._recv_thread.join()
        self._sock.close()

    def is_running(self) -> bool:
        return self._running
    
    def __del__(self):
        self.stop()

class UDP_Packets:
    def __init__(self,*packets): 
        #packets is a list where first goes an ID uint16_t and then string with types
        self._dict_packets = {}
        for packet in packets:
            if len(packet) < 1:
                raise ValueError ("Every packet need a ID at least")
            if not isinstance(packet[0],int) or not (0 <= packet[0] <= 0xFFFF):
                raise ValueError(f"The id must be an uint16_t, {packet[0]}")
            id = packet[0]
            self._dict_packets[id] = list()
            for data_type in packet[1:]:
                self._dict_packets[id].append(data_type)

    def serialize_packet(self,packet_id,*values):
        if packet_id not in self._dict_packets:
            raise KeyError(f"Packet ID {packet_id} not found in the map")
        
        expected_sizes = self._dict_packets[packet_id]
        
        if len(values) != len(expected_sizes):
            raise ValueError(f"Expected {len(expected_sizes)} but received {len(values)}")
        
        binary_packet = struct.pack('<H',packet_id)
        for value, data_type in zip(values,expected_sizes):
            match data_type:
                case "uint8" | "enum": 
                    binary_packet += struct.pack('<B',value)
                case "int8": 
                    binary_packet += struct.pack('<b',value)
                case "uint16" : 
                    binary_packet += struct.pack('<H',value)
                case "int16": 
                    binary_packet += struct.pack('<h',value)
                case "uint32": 
                    binary_packet += struct.pack('<I',value)
                case "int32" : 
                    binary_packet += struct.pack('<i',value)
                case "float32" : 
                    binary_packet += struct.pack('<f',value)
                case "uint64": 
                    binary_packet += struct.pack('<Q',value)
                case "int64": 
                    binary_packet += struct.pack('<q',value)
                case "float64" : 
                    binary_packet += struct.pack('<d',value)
                case _:
                    raise ValueError(f"Unsupported data type: {data_type}") 
        return binary_packet
                 
                 
udp_receive = DatagramSocket("127.0.0.1",8081,"127.0.0.1",8085)
udp_send = DatagramSocket("127.0.0.1",8085,"127.0.0.1",8081)
def receive():
    while True:
        packet = udp_receive.get_packet()
        if packet != None:
            print(packet)
            print(f"New packet id: {struct.unpack('<H',packet[:2])[0]}")
        time.sleep(1)

if __name__ == "__main__":
    mypackets = [1]
    packets = UDP_Packets(mypackets)
    receive__thread = threading.Thread(target=receive, daemon=True)
    receive__thread.start()
    try:
        while True:
            time.sleep(2)
            bytes = packets.serialize_packet(1)
            udp_send.transmit(bytes)
    except KeyboardInterrupt as e:
        print("finish due to keyboard")
        udp_receive.stop()
        udp_send.stop()
        exit(0)



        