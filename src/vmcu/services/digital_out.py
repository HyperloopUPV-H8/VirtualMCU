from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory
class DigitalOutService:
    def __init__(self,shm: SharedMemory,pin: Pinout):
        self._pin = shm.get_pin(pin,PinType.DigitalOut)
        
    def get_pin_state(self) -> memory.DigitalOut.State:
        return self._pin.data.state

    
