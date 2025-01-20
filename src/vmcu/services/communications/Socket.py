import socket
import threading
from queue import Queue
from typing import Optional
MAX_SIZE_PACKET = 1024
TIMEOUT_TIME = 2.0
class Socket: 
    def __init__(self, lip, lport, rip, rport): 
        self.local_ip = lip
        self.remote_ip = rip
        self.local_port = lport
        self.remote_port = rport
        self._running = False
        self._queue_packet_received = Queue()
        self._sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._recv_thread = threading.Thread(target=self._receive, daemon=True)
        self._sock.bind((self.local_ip,self.local_port))
        self._sock.settimeout(TIMEOUT_TIME) 
        
    def connect(self) -> bool:
        #connect the client to the server 
        try: 
            self._sock.connect((self.remote_ip,self.remote_port))
        except OSError as e:
            print(f"Error connecting with the server : {e}")
            self.stop()
            return False
        self._running = True  
        self._recv_thread.start()      
        return True
    
    def _receive(self):
        while self._running:
            try:
                data = self._sock.recv(MAX_SIZE_PACKET)
                if not data:
                    break
            except socket.timeout:
                continue
            except OSError as e:
                print(f"Error  receiving the packet {e}")
                break 
            #add data to the queue
            self._queue_packet_received.put(data)
            
    def transmit(self,buf: bytes): 
        try:
            self._sock.sendall(buf)
        except OSError as e:
            print(f"Error transmiting the packet: {e}")
            self.stop()
    
    def is_running(self) -> bool:
        return self._running
    
    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._recv_thread.is_alive():
            self._recv_thread.join()
        self._sock.close()
    def get_packet(self) -> Optional[bytes]:
        if self._queue_packet_received.empty():
            return None
        return self._queue_packet_received.get()    
    
    def __del__(self):
        self.stop()
    
