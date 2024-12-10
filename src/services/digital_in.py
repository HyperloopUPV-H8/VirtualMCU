from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from src.test_lib.input import Input
class DigitalInService:
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.DigitalIn)
        
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
    
    class StateInput(Input):
        def __init__(self, digitalIn, state):
            self._digitalIn = digitalIn
            self._state = state

        def apply(self):
            self._digitalIn.set_pin_state(self._state)

    def generate_state(self, state: memory.DigitalIn.state) -> Input:
        return self.StateInput(self, state)
    