from src.shared_memory import *
from src.pin import *


shm = SharedMemory("sim_tests")

button = Pin(Pinout.PA0, shm._gpio_shm, PinType.DigitalIn)

button._data.state = DigitalIn.State.High