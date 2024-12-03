from src.services.communication.FDCAN import FDCAN
from src.pin.pinout import Pinout 
import time






ip = "127.0.0.1" 
port = 6969
sendport = 7070


fdcan1= FDCAN(Pinout.PA1, Pinout.PA2)
fdcan1.start(ip, port,sendport)

while(True):
    fdcan1.transmit(16,"Hello",FDCAN.DLC.BYTES_8)
    print("mensaje enviado", flush=True)
    time.sleep(5)


