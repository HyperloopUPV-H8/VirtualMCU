from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory

class PWM:
    def __init__(self,shm: SharedMemory, pin: Pinout):
        self._pin= shm.get_pin(pin, PinType.PWM)

    def get_is_on(self) -> bool:
        return self._pin.is_on
    
    def set_is_on(self, is_on:bool):
        self._pin.data.is_on = is_on
    
    def set_frequency(self, frequency:memory.PWM.frequency):
        self._pin.data.frequency = frequency
    
    def set_duty_cycle(self, duty_cycle:memory.PWM.duty_cycle):
        self._pin.data.duty_cycle = duty_cycle
    
    def get_frequency(self) -> int:
        return self._pin.data.frequency
    
    def get_duty_cycle(self) -> float:
        return self._pin.data.duty_cycle
    
    def set_dead_time_ns(self, dead_time_ns:int):
        self._pin.data.dead_time_ns = dead_time_ns
    
    def get_dead_time_ns(self) -> int:
        return self._pin.data.dead_time_ns
    