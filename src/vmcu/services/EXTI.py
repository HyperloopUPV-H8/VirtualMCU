from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
from src.pin import PinType,memory

class EXTI:
    def __init__(self,shm: SharedMemory,pin: Pinout, trigger_signal: bool):
        self._pin= shm.get_pin(pin,PinType.EXTI)
        self._pin.data.trigger_signal = trigger_signal
    
    def get_is_on(self) -> bool:
        return self._pin.data.is_on
    
    def get_priority(self, priority:int):
        self._pin.data.priority = priority
    
    def set_trigger_signal(self, trigger_signal:bool):
        self._pin.data.trigger_signal = trigger_signal
    
    def get_trigger_mode(self):
        return  self._pin.data.trigger_mode