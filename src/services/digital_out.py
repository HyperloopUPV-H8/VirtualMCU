from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
class DigitalOutService:
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.DigitalOut)
        
    def turn_on(self):
        self._pin.data.state = memory.DigitalOut.State.High
    
    def turn_off(self):
        self._pin.data.state = memory.DigitalOut.State.Low
    
    def toggle(self):
        if self._pin.data.state == memory.DigitalOut.State.High:
            self.turn_off()
        else:
            self.turn_on()
    
    def set_pin_state(self, state: memory.DigitalOut.State):
        self._pin.data.state = state
    
        
        
    


    
