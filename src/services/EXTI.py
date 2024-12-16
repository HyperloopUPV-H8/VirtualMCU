from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from src.test_lib.input import Input
from src.test_lib.condition import Condition
import asyncio
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
    
    class ExtiInput(Input):
        def __init__(self, Exti,trigger_signal):
            self._Exti = Exti
            self._trigger_signal = trigger_signal

        def apply(self):
            self._Exti.set_trigger_signal(self._trigger_signal)

    def generate_trigger_signal(self, trigger_signal: bool) -> Input:
        return self.ExtiInput(self, trigger_signal)
    
    class WaitForStateCondition(Condition):
        def __init__(self, Exti, cond):
            self._Exti = Exti
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._Exti.get_is_on()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_state(self, cond: function) -> Condition:
        return self.WaitForStateCondition(self, cond)

    class WaitForPriorityCondition(Condition):
        def __init__(self, Exti, cond):
            self._Exti = Exti
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._Exti.get_priority()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_priority(self, cond: function) -> Condition:
        return self.WaitForPriorityCondition(self, cond)