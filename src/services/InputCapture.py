from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
from src.pin import PinType,memory
from ctypes import c_uint32
from enum import Enum, auto, unique
class InputCapture:
    def __init__(self,shm:SharedMemory,pin1: Pinout):
            #make the connection between the shared_memory and the pin
            self._pin1 = shm.get_pin(pin1,PinType.InputCapture)

    def get_is_on(self) -> bool:
        return self._pin1.data.is_on
    
    def set_duty_cycle(self, duty_cycle: int) -> None:
        self._pin1.data.duty_cycle = duty_cycle
        
    
    def set_frequency(self,frequency: int) -> None:
        self._pin1.data.frequency = frequency