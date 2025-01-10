from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory

class DigitalInService:
    def __init__(self, shm: SharedMemory,pin: Pinout):
        self._pin = shm.get_pin(pin, PinType.DigitalIn)
        
    def turn_on(self):
        self._pin.data.state = memory.DigitalIn.State.High
    
    def turn_off(self):
        self._pin.data.state = memory.DigitalIn.State.Low
    
    def toggle(self):
        if self._pin.data.state == memory.DigitalIn.State.High:
            self.turn_off()
        else:
            self.turn_on()
    
    def set_pin_state(self, state: memory.DigitalIn.State):
        self._pin.data.state = state
    