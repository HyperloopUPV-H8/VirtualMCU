
from vmcu.services.communications.FDCAN import FDCAN
from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout 
import time






ip = "127.0.0.1" 
port = 6969
sendport = 7070

shm = SharedMemory("gpio__blinking_led","state_machine__blinking_led")
fdcan1= FDCAN(Pinout.PD1, Pinout.PD0,shm)
fdcan1.start(ip, port,sendport)

while(True):
    fdcan1.transmit(16,b"Hello",FDCAN.DLC.BYTES_5)
    print("mensaje enviado", flush=True)
    time.sleep(1)


