from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory

class PWM:
    def __init__(self, pin: Pinout):
        self._pin= SharedMemory.get_pin(pin, memory.PinType.PWM)

    def get_is_on(self) -> bool:
        return self._pin.is_on
    
    def set_is_on(self, is_on:bool):
        self._pin.is_on = is_on
    
    def set_frequency(self, frequency:int):
        self._pin.frequency = frequency
    
    def set_duty_cycle(self, duty_cycle:float):
        self._pin.duty_cycle = duty_cycle
    
    def get_frequency(self) -> int:
        return self._pin.frequency
    
    def get_duty_cycle(self) -> float:
        return self._pin.duty_cycle
    
    def set_dead_time_ns(self, dead_time_ns:int):
        self._pin.dead_time_ns = dead_time_ns
    
    def get_dead_time_ns(self) -> int:
        return self._pin.dead_time_ns
    