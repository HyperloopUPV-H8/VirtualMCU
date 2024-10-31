from enum import Enum, auto, unique
from .pinout import Pinout

@unique
class PinType(Enum):
    NotUsed = auto()
    # TODO: add missing types


# TODO: fill in memory access classes
class DigitalOut:
    def __init__(self, shm: memoryview):
        self._mem = shm

    @property
    def is_on(self) -> bool: 
        return self._mem[0] != 0


    @is_on.setter
    def is_on(self, value: bool):
        self._mem[0] = 1 if value else 0

class DigitalIn: ...
class ADC: ...
class EXTI: ...
class Encoder: ...
class InputCapture: ...
class PWM: ...
class DualPWM: ...

class Pin:
    def __init__(self, pin: Pinout, shm: memoryview, pin_type: PinType = None):
        self._pin = pin
        self._get_memory_view(shm)
        if (pin_type != None):
            self._check_type(pin_type)
        self._init_data()

    data: DigitalOut | DigitalIn | ADC | EXTI | Encoder | InputCapture | PWM | DualPWM

    @property
    def type(self) -> PinType:
        # TODO: access shm
        pass

    def _get_memory_view(self, shm: memoryview):
        # TODO: get a view of just the bytes of this pin
        pass

    def _check_type(self, pin_type: PinType):
        # TODO: check pin type in shm
        pass

    def _init_data(self):
        # TODO: init pin data with self.pin_type and self._memory
        self.data = DigitalOut(self.mem)
        pass
