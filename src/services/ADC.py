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
    class Instance:
        Resolution: 'ADC.ADCResolution' = None
        is_on: bool = False

    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin, memory.PinType.ADC)
        self.Instance.is_on = False
        self._pin.data.is_on = False
        
    def turn_on(self):
        self._pin.data.is_on = True
        self.Instance.is_on = True
    
    def get_value(self)->float:
        if(self.Instance.is_on):
            match self.Instance.Resolution:
                case ADC.ADC_RES_16BITS:
                    return (self._pin.data.value * self.ADC_MAX_VOLTAGE) / float(self.MAX_16BIT)
                case ADC.ADC_RES_14BITS:
                    return (self._pin.data.value * self.ADC_MAX_VOLTAGE) / float(self.MAX_14BIT)
                case ADC.ADC_RES_12BITS:
                    return (self._pin.data.value * self.ADC_MAX_VOLTAGE) / float(self.MAX_12BIT)
                case ADC.ADC_RES_10BITS:
                    return (self._pin.data.value * self.ADC_MAX_VOLTAGE) / float(self.MAX_10BIT)
                case _:
                    return 0
                
    def get_int_value(self) -> int:
        if(self.Instance.is_on):
            match self.Instance.Resolution:
                case ADC.ADC_RES_16BITS:
                    return (self._pin.data.value)
                case ADC.ADC_RES_14BITS:
                    return (self._pin.data.value << 2)
                case ADC.ADC_RES_12BITS:
                    return (self._pin.data.value <<4)
                case ADC.ADC_RES_10BITS:
                    return (self._pin.data.value << 6)
                case _:
                    return 0
    