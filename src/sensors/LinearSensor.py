from src.services.ADC import ADC
from src.test_lib.input import Input
from src.test_lib.condition import Condition
import asyncio

class LinearSensor():
    def __init__(self,adc:ADC,slope:float, offset:float):
        self._adc=adc
        self.slope=slope
        self.offset=offset
        self.value=0.0
    
    def write(self,value:float):
        self.value=value
        adc_value=(self.value-self.offset)/self.slope
        input_action=self._adc.generate_value(adc_value)
        input_action.apply()

    def generate_case(self, initial_value: float, final_value: float, delay: float):
        async def case():
            self.write(initial_value)
            await asyncio.sleep(delay)
            self.write(final_value)
        
        return case

    async def is_value_above_threshold(self, threshold: float, timeout: float):
        def condition_func():
            return self.value>threshold

        condition=self._adc.wait_for_state(condition_func)

        try:
            return await asyncio.wait_for(condition.check(), timeout=timeout)
        except asyncio.TimeoutError:
            print("Condition not met within the estimated time")
            return False
        
    async def is_value_under_threshold(self, threshold: float, timeout: float):
        def condition_func():
            return self.value<threshold

        condition=self._adc.wait_for_state(condition_func)

        try:
            return await asyncio.wait_for(condition.check(), timeout=timeout)
        except asyncio.TimeoutError:
            print("Condition not met within the estimated time")
            return False