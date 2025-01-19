from vmcu.services.communications.spi import SPIMaster, SPISlave
from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType
from multiprocessing import shared_memory

# Init VMCU Shared Memory
shm = SharedMemory("gpio")

slave1 = SPISlave("localhost", 50001, "localhost", 50000, shm, Pinout.PD3)

msg = slave1.receive()
print(msg)