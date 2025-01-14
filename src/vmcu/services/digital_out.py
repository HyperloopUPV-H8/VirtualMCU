from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory
from vmcu.test_lib.condition import Condition
import asyncio
class DigitalOutService:
    def __init__(self,shm: SharedMemory,pin: Pinout):
        self._pin = shm.get_pin(pin,PinType.DigitalOut)
        
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
    
    def wait_for_high(self) -> Condition:
        return self.WaitForStateCondition(self,lambda x: x == memory.DigitalOut.State.High)
    
    def wait_for_low(self) -> Condition:
        return self.WaitForStateCondition(self,lambda x: x == memory.DigitalOut.State.Low)
    
    
