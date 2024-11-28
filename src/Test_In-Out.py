from shared_memory import SharedMemory
from pin import DigitalIn,Pinout,PinType


shm = SharedMemory("sim_tests")

for i in range(128):
    shm._gpio_shm.buf[i]=0x01

while(1):
    pass