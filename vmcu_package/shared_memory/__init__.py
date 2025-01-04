
from multiprocessing import shared_memory
from vmcu_package.pin.pinout import Pinout
from vmcu_package.pin import Pin, PinType

class SharedMemory:
    gpio_memory = memoryview()
    pin_size_in_memory = 14 # Remember to keep in sync with C++

    def __init__(self, gpio_name):
        self._gpio_shm = shared_memory.SharedMemory(gpio_name)

    def get_pin(self, pin: Pinout, pin_type: PinType = None) -> Pin:
        return Pin(pin, self._gpio_shm.buf, pin_type=pin_type)