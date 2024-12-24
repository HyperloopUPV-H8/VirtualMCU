from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from src.test_lib.condition import Condition
from ctypes import c_uint32
from enum import Enum, auto, unique
import asyncio
class DualPWM:
    def __init__(self,pin1: Pinout, pin2: Pinout):
            #register the pins 
            self._pin1 = SharedMemory.get_pin(pin1,memory.DualPWM)
            self._pin2 = SharedMemory.get_pin(pin2,memory.DualPWM)
            
    def get_is_on(self) -> bool:
        return self._pin1.data.is_on
    
    def get_duty_cycle(self) -> float:
        return self._pin1.data.duty_cycle
    
    def get_frequency(self) -> int:
        return self._pin1.data.frequency
    
    def get_dead_time_ns(self) -> int:
        return self._pin1.data.dead_time_ns
  
    class WaitForDutyCondition(Condition):
        def __init__(self, dualpwm, cond):
            self._dualpwm = dualpwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._dualpwm.get_duty_cycle()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_duty(self, cond: function) -> Condition:
        return self.WaitForDutyCondition(self, cond)
    class WaitForFrequencyCondition(Condition):
        def __init__(self, dualpwm, cond):
            self._dualpwm = dualpwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._dualpwm.get_frequency()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_frequency(self, cond: function) -> Condition:
        return self.WaitForFrequencyCondition(self, cond)
    
    class WaitForStateCondition(Condition):
        def __init__(self, dualpwm, cond):
            self._dualpwm = dualpwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._dualpwm.get_is_on()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_state(self, cond: function) -> Condition:
        return self.WaitForStateCondition(self, cond)
    
    def wait_for_high(self) -> Condition:
        return self.WaitForStateCondition(self,lambda x: x == True)
    
    def wait_for_low(self) -> Condition:
        return self.WaitForStateCondition(self,lambda x: x == False)

    class WaitForDeadTimeCondition(Condition):
        def __init__(self, dualpwm, cond):
            self._dualpwm = dualpwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._dualpwm.get_dead_time_ns()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_dead_time(self, cond: function) -> Condition:
        return self.WaitForDeadTimeCondition(self, cond)
    class WaitForDutyCondition(Condition):
        def __init__(self, dualpwm, cond):
            self._pwm = dualpwm
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._pwm.get_duty_cycle()):
                await asyncio.sleep(0)
                pass
            return True
    
    def wait_for_duty(self, cond: function) -> Condition:
        return self.WaitForDutyCondition(self, cond)