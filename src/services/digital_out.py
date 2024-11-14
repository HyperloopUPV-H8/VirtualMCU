from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
class DigitalOutService:
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.DigitalOut)
        
    def get_pin_state(self) -> memory.DigitalOut.State:
        return self._pin.data.state
        
        
    


    
