from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from src.test_lib.condition import Condition
import asyncio
class DigitalOutService:
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.DigitalOut)
        
    def get_pin_state(self) -> memory.DigitalOut.State:
        return self._pin.data.state

    class WaitForStateCondition(Condition):
        def __init__(self, digitalOut, cond):
            self._digitalOut = digitalOut
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._digitalOut.get_pin_state()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_state(self, cond: function) -> Condition:
        return self.WaitForStateCondition(self, cond)
