import time
import src.services.communication.FDCAN as FDCAN
import src.pin





def __main__():
    ip = 0x5A4AB9FF #Por poner
    port = 3001 #Por poner
    
    fdcan1= FDCAN.FDCAN(src.pin.Pinout.PA1, src.pin.Pinout.PA2)
    fdcan1.start(ip,port)
    transmitir = -1
    transmitir = input("Introduce 1 para transmitir")
    if transmitir == 1:
        fdcan1.transmit(0x124, b"Hello",FDCAN.DLC.BYTES_8)
    while(True):
        packet = fdcan1.read()
        print(packet.rx_data)
        print(packet.identifier)
        print(packet.data_length)
        print("")
        time.sleep(1)
        
__main__()