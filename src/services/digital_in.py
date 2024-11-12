from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory

class DigitalInService:
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.DigitalIn)
        
    def read_pin_state(self) -> memory.DigitalIn.State:
        return self._pin.data.state