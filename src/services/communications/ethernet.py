import socket
import threading
from queue import Queue
from typing import Optional
MAX_SIZE_PACKET = 1024
class DatagramSocket:
    def __init__(self, lip, lport, rip, rport): 
        self.local_ip = lip
        self.remote_ip = rip
        self.local_port = lport
        self.remote_port = rport
        self.running = True
        self.queue_packet_received = Queue()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((self.local_ip,self.local_port))
        self.sock.timeout(2.0) 
        
        self.recv_thread = threading.Thread(target=self.receive, daemon=True)
        self.recv_thread.start()       
    def recieve(self): 
        while self.running:
            try:
                data,address = self.sock.recvfrom(MAX_SIZE_PACKET)
                if address == (self.remote_ip,self.remote_port): #check if the receiving message comes from the ip address correct
                    self.queue_packet_received.put(data)
            except socket.timeout:
                continue
            except OSError as e:
                print(f"Error while receiving data: {e}")
                break
               
    def transmit(self, buf: bytes) -> int:
        bytes_sent = 0
        try:
            while(bytes_sent < len(buf)):
                new_bytes_sent = self.sock.sendto(buf,(self.remote_ip,self.remote_port))
                bytes_sent += new_bytes_sent
        except OSError as e:
            print(f"Error while sending data: {e}")
        return bytes_sent
    
    def get_packet(self) -> Optional[bytes]:
        if self.queue_packet_received.empty():
            return None
        return self.queue_packet_received.get()
    
    def stop(self):
        self.running = False
        self.sock.close()
        self.recv_thread.join()

class Socket:
    def __init__(self, lip, lport, rip, rport): ...
    def __init__(self, socket): ...
    def recieve(): ...
    def transmit(): ...
class Server:
    def __init__(self, ip, port): ...
    def accept(self) -> Socket: ...