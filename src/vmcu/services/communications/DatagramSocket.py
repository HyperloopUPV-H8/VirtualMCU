import socket
import threading
import asyncio
from vmcu.test_lib.input import Input
from vmcu.test_lib.condition import Condition
from vmcu.services.communications.Packets import Packets 
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

    class Raw_Data_Input(Input):
        def __init__(self,DatagramSocket,raw_data):
            self._DatagramSocket = DatagramSocket
            self._raw_data = raw_data
        
        def apply(self):
            self._server.transmit(self._raw_data)
    
    def transmit_raw_data(self,raw_data : bytes) -> Input:
        return self.Raw_Data_Input(self,raw_data)
    
    def serialize_and_transmit_data(self, formatted_data : Packets, *values) -> Input:
        raw_data = formatted_data.serialize_packet(values)
        return self.Raw_Data_Input(self,raw_data)
    
    class WaitForPacketCondition(Condition):
        def __init__(self, Datagram_socket, cond):
            self._DatagramSocket = Datagram_socket
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._DatagramSocket.get_packet()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_packet_condition(self, cond: function) -> Condition:
        return self.WaitForPacketCondition(self, cond)
    

                 
                 



        