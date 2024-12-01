import time
from src.services.communication.FDCAN import FDCAN
import src.pin.pinout as pin






ip = "127.0.0.1" #Por poner
port = 7070 #Por poner


#fdcan1= FDCAN(pin.Pinout.PA1, pin.Pinout.PA2)
fdcan1 = FDCAN(ip, port)
while(True):
    print("Reading...")
    packet = fdcan1.read()
    print(packet.rx_data)
    print(packet.identifier)
    print(packet.data_length)
    print("")
    time.sleep(1)
        


