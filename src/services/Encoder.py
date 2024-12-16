from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from src.test_lib.input import Input
from src.test_lib.condition import Condition
from ctypes import c_uint32
from enum import Enum, auto, unique
import asyncio
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
    
    class DirectionInput(Input):
        def __init__(self,Encoder, direction):
            self._Encoder = Encoder
            self._direction = direction

        def apply(self):
            self._Encoder.set_direction(self._direction)

    def generate_direction(self, direction: memory.Encoder.Direction) -> Input:
        return self.DirectionInput(self, direction)
    
    class CounterInput(Input):
        def __init__(self, Encoder, counter):
            self._Encoder = Encoder
            self._counter = counter

        def apply(self):
            self._Encoder.set_counter(self._counter)

    def generate_counter(self, counter: int) -> Input:
        return self.CounterInput(self, counter)
    
    class WaitForStateCondition(Condition):
        def __init__(self, Encoder, cond):
            self._Encoder = Encoder
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._Encoder.get_is_on()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_state(self, cond: function) -> Condition:
        return self.WaitForStateCondition(self, cond)
