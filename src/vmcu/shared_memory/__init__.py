from multiprocessing import shared_memory
from vmcu.pin.pinout import Pinout
from vmcu.pin import Pin, PinType

class SharedMemory:
    pin_size_in_memory = 18 # Remember to keep in sync with C++

    def __init__(self, gpio_name,state_machine_name):
        self._gpio_shm = shared_memory.SharedMemory(gpio_name, create=False)
        self._state_machine_shm = shared_memory.SharedMemory(state_machine_name, create=False)

    def get_pin(self, pin: Pinout, pin_type: PinType) -> Pin:
        return Pin(pin, self._gpio_shm.buf, pin_type)
    
    def get_state_machine_count(self)->int:
        return self._state_machine_shm.buf[0]
    
    def get_state_machine_state(self,sm_id:int)->int:
        if(sm_id>self.get_state_machine_count() or sm_id<1):
            return -1
        else:
            return self._state_machine_shm.buf[sm_id]
