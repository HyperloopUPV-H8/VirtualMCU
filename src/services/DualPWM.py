from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from ctypes import c_uint32
from enum import Enum, auto, unique
class DualPWM:
    def __init__(self,pin1: Pinout, pin2: Pinout):
            #register the pins 
            self._pin1 = SharedMemory.get_pin(pin1,memory.DualPWM)
            self._pin2 = SharedMemory.get_pin(pin2,memory.DualPWM)
            
    def get_is_on(self) -> bool:
        return self._pin1.data.is_on
    
    def get_duty_cycle(self) -> float:
        return self._pin1.data.duty_cycle
    
    def get_frequency(self) -> int:
        return self._pin1.data.frequency
    
    def get_dead_time_ns(self) -> int:
        return self._pin1.data.dead_time_ns
  