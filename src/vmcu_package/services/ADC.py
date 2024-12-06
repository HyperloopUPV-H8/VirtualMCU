from vmcu_package.shared_memory import SharedMemory
from vmcu_package.pin.pinout import Pinout
import pin.memory as memory




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
    
   
    