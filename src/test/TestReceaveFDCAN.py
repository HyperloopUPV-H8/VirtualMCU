from src.services.communications.FDCAN import FDCAN
from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout 
import time






ip = "127.0.0.1" 
port = 7070 
sendport = 6969 

shm = SharedMemory("gpio")
fdcan1= FDCAN(Pinout.PA1, Pinout.PA2,shm)
fdcan1.start(ip, port,sendport)
while(True):
    print("Reading...")
    packet = fdcan1.read()
    print(packet.rx_data)
    print(packet.identifier)
    print(packet.data_length)
    print("")
    time.sleep(1)
        


