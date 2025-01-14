from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
from src.pin import PinType
from src.vmcu.pin import memory




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
    
   
    