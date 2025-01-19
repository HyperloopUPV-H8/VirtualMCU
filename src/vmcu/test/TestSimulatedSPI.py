from vmcu.services.communications.spi import SPIMaster, SPISlave
from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType
from multiprocessing import shared_memory

# Simulate Shared Memory
try:
    shm_simulated = shared_memory.SharedMemory("gpio", create=True, size=18 * 114)
except:
    shm_simulated = shared_memory.SharedMemory("gpio", create=False, size=18 * 114)

# Init VMCU Shared Memory
shm = SharedMemory("gpio")

# Put pin PA0 as a SPI type, and power it on
shm_simulated.buf[0] = 7  # PinType -> SPI
shm_simulated.buf[1] = 1  # is_on -> True

master = SPIMaster("localhost", 50000, shm)
slave1 = SPISlave("localhost", 50001, "localhost", 50000, shm, Pinout.PA0)
slave2 = SPISlave("localhost", 50002, "localhost", 50000, shm, Pinout.PA0)


master.transmit(b"Hello world", "localhost", 50001)
master.transmit(b"Hello world", "localhost", 50001)
msg = slave1.receive()
print(msg)

master.transmit(b"Hello world", "localhost", 50002)
msg = slave2.receive()
print(msg)
print(slave1.receive())

shm_simulated.unlink()
