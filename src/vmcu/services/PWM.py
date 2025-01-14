from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory
from vmcu.test_lib.condition import Condition
import asyncio
class PWM:
    def __init__(self,shm: SharedMemory, pin: Pinout):
        self._pin= shm.get_pin(pin, PinType.PWM)

    def get_is_on(self) -> bool:
        return self._pin.data.is_on

    def get_frequency(self) -> int:
        return self._pin.data.frequency
    
    def get_duty_cycle(self) -> float:
        return self._pin.data.duty_cycle

    def get_dead_time_ns(self) -> int:
        return self._pin.data.dead_time_ns
    class WaitForDutyCondition(Condition):
        def __init__(self, pwm, cond):
            self._pwm = pwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._pwm.get_duty_cycle()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_duty(self, cond: function) -> Condition:
        return self.WaitForDutyCondition(self, cond)
    class WaitForFrequencyCondition(Condition):
        def __init__(self, pwm, cond):
            self._pwm = pwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._pwm.get_frequency()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_frequency(self, cond: function) -> Condition:
        return self.WaitForFrequencyCondition(self, cond)

    class WaitForEnableCondition(Condition):
        def __init__(self, pwm, cond):
            self._pwm = pwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._pwm.get_is_on()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_enable_condition(self, cond: function) -> Condition:
        return self.WaitForEnableCondition(self, cond)
    
    def wait_for_enable(self) -> Condition:
        return self.WaitForEnableCondition(self,lambda x: x == True)
    
    def wait_for_disable(self) -> Condition:
        return self.WaitForEnableCondition(self,lambda x: x == False)
    class WaitForDeadTimeCondition(Condition):
        def __init__(self, pwm, cond):
            self._pwm = pwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._pwm.get_dead_time_ns()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_dead_time(self, cond: function) -> Condition:
        return self.WaitForDeadTimeCondition(self, cond)