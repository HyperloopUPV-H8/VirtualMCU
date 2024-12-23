
from multiprocessing import shared_memory
from src.pin.pinout import Pinout
from src.pin import Pin, PinType

class SharedMemory:
    pin_size_in_memory = 18 # Remember to keep in sync with C++

    def __init__(self, gpio_name):
        self._gpio_shm = shared_memory.SharedMemory(gpio_name, create=False)

    def get_pin(self, pin: Pinout, pin_type: PinType) -> Pin:
        return Pin(pin, self._gpio_shm.buf, pin_type)
    