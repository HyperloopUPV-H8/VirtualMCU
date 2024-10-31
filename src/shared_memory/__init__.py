
from pin.pinout import Pinout
from pin import Pin

class SharedMemory:
    gpio_memory = memoryview()
    pin_size_bytes_in_memory = 16 # TODO: update value to reflect c++

    def __init__(self):
        # TODO: open shared memory
        pass

    def get_pin(self, pin: Pinout) -> Pin:
        # TODO: return pin
        pass
