from vmcu.shared_memory import SharedMemory
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType,memory
from enum import Enum



class ADC:
    ADC_MAX_VOLTAGE = 3.3
    MAX_16BIT = 0b1111111111111111
    MAX_14BIT = 0b0011111111111111
    MAX_12BIT = 0b0000111111111111
    MAX_10BIT = 0b0000001111111111

    class Resolution(Enum):
        ADC_RES_16BITS = 0x00000000,
        ADC_RES_14BITS = 0x00000004,
        ADC_RES_12BITS = 0x00000008,
        ADC_RES_10BITS = 0x0000000C 
    
    def __init__(self, shm: SharedMemory,pin: Pinout):
        self._pin = shm.get_pin(pin,PinType.ADC)
        
    def get_is_on(self) -> bool:
        return self._pin.data.is_on
    
    def set_value(self, value: int):
        resolution=ADC.Resolution(self._pin.data.resolution)

        if(value <= ADC.ADC_MAX_VOLTAGE or value >= 0):
            if(resolution==ADC.Resolution.ADC_RES_16BITS):
                scaled_value=value*ADC.MAX_16BIT/ADC.ADC_MAX_VOLTAGE
            elif(resolution==ADC.Resolution.ADC_RES_14BITS):
                scaled_value=value*ADC.MAX_14BIT/ADC.ADC_MAX_VOLTAGE
            elif(resolution==ADC.Resolution.ADC_RES_12BITS):
                scaled_value=value*ADC.MAX_12BIT/ADC.ADC_MAX_VOLTAGE
            elif(resolution==ADC.Resolution.ADC_RES_10BITS):
                scaled_value=value*ADC.MAX_10BIT/ADC.ADC_MAX_VOLTAGE
            else:
                raise ValueError("Invalid resolution")
            
            self._pin.data.value=int(scaled_value)
        else:
            raise ValueError("Value is greater than the maximum voltage")
    
   
    