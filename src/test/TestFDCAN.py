import time
import sys
sys.path.append('/c:/Users/dani4/OneDrive - UPV/HUPV/Projectos/VirtualMCU')
from src.services.communication.FDCAN import FDCAN
import src.pin.pinout as pin





def __main__():
    ip = 0x5A4AB969 #Por poner
    port = 3000 #Por poner
    
    fdcan1= FDCAN.FDCAN(pin.PA1, pin.PA2)
    fdcan1.start(ip,port)
    transmitir = -1
    transmitir = input("Introduce 1 para transmitir")
    if transmitir == 1:
        fdcan1.transmit(0x123, b"Hello",FDCAN.DLC.BYTES_8)
    while(True):
        packet = fdcan1.read()
        print(packet.rx_data)
        print(packet.identifier)
        print(packet.data_length)
        print("")
        time.sleep(1)
        
__main__()

