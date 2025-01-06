from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from ctypes import c_uint32
from enum import Enum, auto, unique
from src.test_lib.input import Input
class InputCapture:
    def __init__(self,pin1: Pinout):
            #make the connection between the shared_memory and the pin
            self._pin1 = SharedMemory.get_pin(pin1,memory.InputCapture)

    def set_duty_cycle(self, duty_cycle: int) -> None:
        self._pin1.data.duty_cycle = duty_cycle
        
    
    def set_frequency(self,frequency: int) -> None:
        self._pin1.data.frequency = frequency
    
    class DutyInput(Input):
        def __init__(self, InputCapture, duty):
            self._InputCapture = InputCapture
            self._duty = duty

        def apply(self):
            self._InputCapture.set_duty_cycle(self._duty)

    def generate_duty(self, duty: int) -> Input:
        return self.DutyInput(self, duty)        
    
    class FrequencyInput(Input):
        def __init__(self, InputCapture, frequency):
            self._InputCapture = InputCapture
            self._frequency = frequency

        def apply(self):
            self._InputCapture.set_frequency(self._frequency)

    def generate_frequency(self, frequency: int) -> Input:
        return self.FrequencyInput(self, frequency)      