from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from src.test_lib.input import Input
from src.test_lib.condition import Condition


class ADC:
    ADC_MAX_VOLTAGE = 3.3
    
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.ADC)
        
    def get_is_on(self) -> bool:
        return self._pin.is_on
    
    def set_value(self, value: int):
        if(value <= ADC.ADC_MAX_VOLTAGE or value >= 0):
            self._pin.value = value
        else:
            raise ValueError("Value is greater than the maximum voltage")
    
    class ValueInput(Input):
        def __init__(self, adc, value):
            self._adc = adc
            self._value = value

        def apply(self):
            self._adc.set_value(self._value)

    def generate_value(self, value: int) -> Input:
        return self.ValueInput(self, value)
    
    class WaitForStateCondition(Condition):
        def __init__(self, ADC, cond):
            self._ADC = ADC
            self._cond = cond
        
        async def check(self) -> bool:
            while not self._cond(self._ADC.get_is_on()):
                pass
            return True

    def wait_for_state(self, cond: function) -> Condition:
        return self.WaitForStateCondition(self, cond)
