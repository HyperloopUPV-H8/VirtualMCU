from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory
from vmcu.test_lib.input import Input
from vmcu.test_lib.condition import Condition
import asyncio



class ADC:
    ADC_MAX_VOLTAGE = 3.3
    
    def __init__(self, shm: SharedMemory,pin: Pinout):
        self._pin = shm.get_pin(pin,PinType.ADC)
        
    def get_is_on(self) -> bool:
        return self._pin.data.is_on
    
    def set_value(self, value: int):
        if(value <= ADC.ADC_MAX_VOLTAGE or value >= 0):
            self._pin.data.value=value
        else:
            raise ValueError("Value is greater than the maximum voltage")
    
    class ValueInput(Input):
        def __init__(self, adc, value):
            self._adc = adc
            self._value = value

        def apply(self):
            if not self._adc.get_is_on():
                raise RuntimeError("Cannot generate a value with the ADC Disable")
            self._adc.set_value(self._value)

    def generate_value(self, value: int) -> Input:
        return self.ValueInput(self, value)
    
    class WaitForEnableCondition(Condition):
        def __init__(self, adc, cond):
            self._adc = adc
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._adc.get_is_on()):
                await asyncio.sleep(0)
                pass
            return True

    def wait_for_enable_condition(self, cond: function) -> Condition:
        return self.WaitForEnableCondition(self, cond)
    
    def wait_for_enable(self) -> Condition:
        return self.WaitForEnableCondition(self,lambda x: x == True)
    
    def wait_for_disable(self) -> Condition:
        return self.WaitForEnableCondition(self,lambda x: x == False)
    
   
    