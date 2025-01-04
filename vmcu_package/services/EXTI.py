from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory

class EXTI:
    def __init__(self, pin: Pinout, trigger_mode:memory.EXTI_Trigger_Mode):
        self._pin= SharedMemory.get_pin(pin, memory.PinType.EXTI)
        self._pin.trigger_signal = trigger_mode
    
    def get_is_on(self) -> bool:
        return self._pin.is_on
    
    def set_priority(self, priority:int):
        self._pin.priority = priority
    
    def set_trigger_signal(self, trigger_signal:bool):
        self._pin.trigger_signal = trigger_signal