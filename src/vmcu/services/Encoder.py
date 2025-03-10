from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
import vmcu.pin.memory as memory
from ctypes import c_uint32
from enum import Enum, auto, unique
registered_encoder = []
class Encoder:
    def __init__(self,pin1: Pinout, pin2: Pinout):
        if (pin1,pin2) not in Encoder.registered_encoder:
            #register the pins 
            Encoder.registered_encoder.append((pin1,pin2))
            self._pin1 = SharedMemory.get_pin(pin1,memory.Encoder)
            self._pin2 = SharedMemory.get_pin(pin2,memory.Encoder)
        else: 
            print("ERROR: The pins were already registered")

    def get_is_on(self) -> bool:
        return self._pin1.data.is_on
    
    def set_direction(self,direction: memory.Encoder.Direction) ->None:
        self._pin1.data.direction = self._pin2.data.direction = direction
        
    def set_counter(self,counter_value: int) -> None:
        self._pin1.data.counter = self._pin2.data.counter = counter_value
    
    def increase_counter(self) -> None:
        self.set_counter(self._pin1.data.counter +1)
        