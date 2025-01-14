from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
from src.pin import PinType
from src.vmcu.pin import memory
class DigitalOutService:
    def __init__(self,shm: SharedMemory,pin: Pinout):
        self._pin = shm.get_pin(pin,PinType.DigitalOut)
        
    def get_pin_state(self) -> memory.DigitalOut.State:
        return self._pin.data.state

    
