from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from ctypes import c_uint32
from enum import Enum, auto, unique

class Encoder:
    registered_encoder = []

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
        actual_counter_value = self._pin1.data.counter
        new_counter_value = actual_counter_value + 1
        self._pin1.data.counter = self._pin2.data.counter = new_counter_value
        