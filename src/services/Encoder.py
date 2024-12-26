from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
from src.pin import PinType,memory
from ctypes import c_uint32
from enum import Enum, auto, unique
class Encoder:
    def __init__(self,shm:SharedMemory,pin1: Pinout, pin2: Pinout):
        _registered_encoder = []
        if (pin1,pin2) not in _registered_encoder:
            #register the pins 
            _registered_encoder.append((pin1,pin2))
            self._pin1 = shm.get_pin(pin1,PinType.Encoder)
            self._pin2 = shm.get_pin(pin2,PinType.Encoder)
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
        