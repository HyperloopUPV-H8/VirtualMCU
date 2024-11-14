from src.shared_memory import SharedMemory
from src.pin.pinout import Pinout
import src.pin.memory as memory
from enum import Enum, auto, unique



class ADC:
    ADC_MAX_VOLTAGE = 3.3
    MAX_16BIT= 0b1111111111111111
    MAX_14BIT= 0b0011111111111111
    MAX_12BIT= 0b0000111111111111
    MAX_10BIT= 0b0000001111111111
    class ADCResolution(Enum):
        ADC_RES_16BITS = 0x00000000
        ADC_RES_14BITS = 0x00000004
        ADC_RES_12BITS = 0x00000008
        ADC_RES_10BITS = 0x0000000C

    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.ADC)
        
    def get_is_on(self) -> bool:
        return self._pin.is_on
    
    def set_value(self, value: int):
        if(value <= ADC.ADC_MAX_VOLTAGE):
            self._pin.value = value
        else:
            raise ValueError("Value is greater than the maximum voltage")
    
   
    