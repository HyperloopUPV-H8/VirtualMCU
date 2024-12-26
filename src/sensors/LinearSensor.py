from src.services.ADC import ADC
from src.pin.pinout import Pinout
from src.shared_memory import SharedMemory
from test_lib.input.aggregate import Multiple
from test_lib.input.input import Input, InputFailedException
from test_lib.condition.condition import Condition

class LinearSensor():
    def __init__(self,shm:SharedMemory,pin:Pinout,slope:float, offset:float):
        self._adc=ADC(shm,pin)
        self._slope=slope
        self._offset=offset
        self._value=0.0
    
    class LinearSensorException(InputFailedException):
        def __str__(self):
            return "The ADC is not on"

    def write(self,value:float) -> Input:
        if(self._adc.get_is_on()):
            self._value=value
            adc_value=(self._value-self._offset)/self._slope
            input_action=self._adc.generate_value(adc_value)
            input_action.apply()
            return self._adc.generate_value(adc_value)
        else:
            raise self.LinearSensorException()
