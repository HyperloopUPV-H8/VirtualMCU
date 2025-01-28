import socket
import threading
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
        self._sock.settimeout(TIMEOUT_TIME)  
    
    def connect(self):
        self._sock.bind((self.local_ip,self.local_port))
        self._sock.settimeout(TIMEOUT_TIME) 
        self._running = True                 
               
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
        while self._running:
            try:
                data,address = self._sock.recvfrom(MAX_SIZE_PACKET)
                if address == (self.remote_ip,self.remote_port): #check if the receiving message comes from the ip address correct
                    return data
            except socket.timeout:
                continue
            except OSError as e:
                if self._running == False:
                    return
                print(f"Error while receiving data: {e}")
                break
    
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


                 
                 



        