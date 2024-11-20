from enum import Enum, auto, unique
from shared_memory import SharedMemory

from .pinout import Pinout
from .memory import (
    DigitalOut,
    DigitalIn,
    ADC,
    EXTI,
    Encoder,
    InputCapture,
    PWM,
    DualPWM,
    SPI
)

@unique
class PinType(Enum):
    NotUsed = auto()
    DigitalOut = auto()
    DigitalIn = auto()
    ADC = auto()
    EXTI = auto()
    Encoder = auto()
    InputCapture = auto()
    PWM = auto()
    DualPWM = auto()
    SPI = auto()
    # TODO: add missing types

class DualPWM: ...

class Pin:
    _pin_type_offset_in_memory = 0

    _data: DigitalOut | DigitalIn | ADC | EXTI | Encoder | InputCapture | PWM | DualPWM | SPI

    def __init__(self, pin: Pinout, shm: memoryview, pin_type: PinType = None):
        self._pin = pin
        self._mem = Pin._get_memory_view(pin, shm)

        if (pin_type != None):
            self._check_type_is_same_as(pin_type)
        self._type = pin_type

        self._init_data()

    @property
    def type(self) -> PinType:
        return self._type
    
    @property
    def data(self):
        return self._data

    # returns a memoryview of the exact bytes that represent this pin
    def _get_memory_view(pin: Pinout, shm: memoryview) -> memoryview:
        base_address = pin.value * SharedMemory.pin_size_in_memory
        return shm[base_address:base_address + SharedMemory.pin_size_in_memory]

    # throws an exception if the pin type is different
    def _check_type_is_same_as(self, pin_type: PinType):
        stored_pin_type = self._mem[Pin._pin_type_offset_in_memory]
        if PinType(stored_pin_type) == pin_type:
            return
        raise DifferentPinType(pin_type, stored_pin_type)

    # construct the class to access the actual pin data and store it
    def _init_data(self):
        if self.type == PinType.DigitalOut:
            self._data = DigitalOut(self._mem[1:])
        elif self.type == PinType.DigitalIn:
            self._data = DigitalIn(self._mem[1:])
        elif self.type == PinType.ADC:
            self._data = ADC(self._mem[1:])
        elif self.type == PinType.EXTI:
            self._data = EXTI(self._mem[1:])
        elif self.type == PinType.Encoder:
            self._data = Encoder(self._mem[1:])
        elif self.type == PinType.InputCapture:
            self._data = InputCapture(self._mem[1:])
        elif self.type == PinType.PWM:
            self._data = PWM(self._mem[1:])
        elif self.type == PinType.DualPWM:
            self._data = DualPWM(self._mem[1:])
        # TODO: add missing types
        else:
            self._data = None


class DifferentPinType(Exception):
    def __init__(self, expected: PinType, got: PinType):
        self.expected = expected
        self.got = got

    def __str__(self) -> str:
        return f"pin declared as '{self.got}' when it should be '{self.expected}'"