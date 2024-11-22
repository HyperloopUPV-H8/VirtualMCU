import socket
import threading
from queue import Queue
from typing import Optional
MAX_SIZE_PACKET = 1024
MAX_LISTEN_CONNECTIONS = 5
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
        self._sock.close()
        if self._recv_thread.is_alive():
            self._recv_thread.join()

    def is_running(self) -> bool:
        return self._running
class Socket: 
    def __init__(self, lip, lport, rip, rport): 
        self.local_ip = lip
        self.remote_ip = rip
        self.local_port = lport
        self.remote_port = rport
        self._running = True
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
        self._recv_thread.start()      
        return True
    
    def _recieve(self):
        while self._running:
            try:
                data = self._sock.recv(MAX_SIZE_PACKET)
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
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self._sock.close()
        if self._recv_thread.is_alive():
            self._recv_thread.join()
    
    def get_packet(self) -> Optional[bytes]:
        if self._queue_packet_received.empty():
            return None
        return self._queue_packet_received.get()    
        
class Server:
    def __init__(self, ip, port): 
        self.local_ip = ip
        self.port = port
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.bind((self.local_ip,self.port))
        self._running = True
        self.connections = {} #dictionary: key = client_address value = connection
        self.recv_clients_threads =[]
        self._queue_packet_receive_dictionary = {} #this dictionary will have key = connection value = queue of the packets received
        self._accept_thread = threading.Thread(target=self._accept, daemon=True)
        self._server.settimeout(TIMEOUT_TIME)
        self._accept_thread.start()
        
        
    def _accept(self) : 
        self._server.listen(MAX_LISTEN_CONNECTIONS)
        while self._running:
            try:
                connection, client_address = self._server.accept()
                print(f"Connection accepted from {client_address}")
                self.connections[client_address] = connection
                self._queue_packet_receive_dictionary[client_address] = Queue()
                # thread to handle_receive__packets from the client
                _recv_thread = threading.Thread(target=self._receive, args=(connection, client_address), daemon=True)
                _recv_thread.start()
                self.recv_clients_threads.append(_recv_thread)
            except socket.timeout:
                continue
            except OSError as e:
                print(f"Error accepting connection: {e}")
    
    
    def _recieve(self,connection: socket.socket, client_address):
        while self._running:
            try:
                data = connection.recv(MAX_SIZE_PACKET)
                self._queue_packet_receive_dictionary[client_address].put(data)
            except socket.timeout:
                continue
            except OSError as e:
                print(f"Error  receiving the packet from the socket: {client_address}, error: {e}")
                break
        connection.close()
        if client_address in self.connections:
            del self.connections[client_address]
        if client_address in self._queue_packet_receive_dictionary:
            del self._queue_packet_receive_dictionary[client_address]

    def transmit(self,buf: bytes,   client_address : tuple[str,int]): 
        if client_address not in self.connections:
            print(f"client {client_address} is not connected")
            return
        connection = self.connections[client_address]
        self._send_packet(buf,connection,client_address)
    
    def _send_packet(self,buf: bytes, connection: socket.socket,client_address : tuple[str,int]):
        try:
            connection.sendall(buf)
            print(f"Data sent to {client_address}")
        except OSError as e:
            print(f"Error transmitting data to {client_address}: {e}")
            self.stop() 
                
    def get_packet(self,client_address: tuple[str, int]) -> Optional[bytes]:
        if client_address not in self._queue_packet_receive_dictionary:
            print(f"No data available for client {client_address}.")
            return None
        queue = self._queue_packet_receive_dictionary[client_address]
        if queue.empty():
            return None
        return queue.get()      
    
      
    def stop(self):
        if not self._running:
            return
        self._running = False
        self._accept_thread.join()  # wait to accept thread to finish    
        # wait until every receive thread has finished
        for thread in self.recv_clients_threads:
            thread.join()
        
        self._server.close()
        print("Server stopped.")
        
    def is_running(self) -> bool:
        return self._running