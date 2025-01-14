from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory
from vmcu.test_lib.condition import Condition
from vmcu.test_lib.input import Input
import asyncio
class EXTI:
    def __init__(self,shm: SharedMemory,pin: Pinout, trigger_signal: bool):
        self._pin= shm.get_pin(pin,PinType.EXTI)
        self._pin.data.trigger_signal = trigger_signal
    
    def get_is_on(self) -> bool:
        return self._pin.data.is_on
    
    def get_priority(self, priority:int):
        self._pin.data.priority = priority
    
    def set_trigger_signal(self, trigger_signal:bool):
        self._pin.data.trigger_signal = trigger_signal
    
    def get_trigger_mode(self):
        return  self._pin.data.trigger_mode
    class ExtiInput(Input):
        def __init__(self, Exti,trigger_signal):
            self._Exti = Exti
            self._trigger_signal = trigger_signal

        def apply(self):
            if not self._Exti.get_is_on():
                raise RuntimeError("Cannot generate a Trigger signal with the EXTI Disable")
            self._Exti.set_trigger_signal(self._trigger_signal)

    def generate_trigger_signal(self, trigger_signal: bool) -> Input:
        return self.ExtiInput(self, trigger_signal)
    
    class WaitForEnableCondition(Condition):
        def __init__(self, EXTI, cond):
            self._Exti = EXTI
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._Exti.get_is_on()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_enable_condition(self, cond: function) -> Condition:
        return self.WaitForEnableCondition(self, cond)
    
    def wait_for_enable(self) -> Condition:
        return self.WaitForEnableCondition(self,lambda x: x == True)
    
    def wait_for_disable(self) -> Condition:
        return self.WaitForEnableCondition(self,lambda x: x == False)
    
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
    
    class WaitForTriggerModeCondition(Condition):
        def __init__(self, Exti, cond):
            self._Exti = Exti
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._Exti.get_trigger_mode()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_Trigger_Mode(self, cond: function) -> Condition:
        return self.WaitForTriggerModeCondition(self, cond)