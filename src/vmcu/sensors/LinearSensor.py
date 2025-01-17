from src.vmcu.services.ADC import ADC
from src.vmcu.pin.pinout import Pinout
from src.vmcu.shared_memory import SharedMemory
from test_lib.input.aggregate import Multiple
from test_lib.input.input import Input, InputFailedException
from test_lib.condition.condition import Condition
from test_lib.input.checked import Checked

class LinearSensor():
    def __init__(self,shm:SharedMemory,pin:Pinout,slope:float, offset:float):
        self._adc=ADC(shm,pin)
        self._slope=slope
        self._offset=offset
        self._value=0.0
    
    class LinearSensorException(InputFailedException):
        def __str__(self):
            return "The ADC is not on"
    
    def _check_pin_state(self) -> bool:
        if not self._adc.get_is_on():
            raise self.LinearSensorException()
        else:
            return True

    def generate_value(self, value: float) -> Input:
        adc_value = (value - self._offset) / self._slope
        return Checked(self._check_pin_state, self._adc.generate_value(adc_value))
