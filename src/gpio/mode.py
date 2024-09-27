from enum import Enum, unique

from .pinout import Pinout


# PinModeEnum is used to autogenerate all the pin values starting at 0. By
# default auto() starts at 1.
class PinModeEnum(Enum):
    def __new__(self):
        value = len(self.__members__)
        obj = object.__new__(self)
        obj._value_ = value
        return obj


@unique
class PinMode(PinModeEnum):
    NOT_USED = ()
    INPUT    = () 
    OUTPUT   = ()
    PWM_IN   = ()
    PWM_OUT  = ()

    def get_view(mode, pin: Pinout, mem: memoryview):
        if mode is PinMode.NOT_USED:
            raise UnusedPinError()
        elif mode is PinMode.INPUT or mode is PinMode.OUTPUT:
            return DigitalPin(pin, mem)
        elif mode is PinMode.PWM_IN or mode is PinMode.PWM_OUT:
            return PWMPin(pin, mem)
        else:
            raise UnknownModeError()


class UnusedPinError(Exception): ...


class UnknownModeError(Exception): ...


class PinState(Enum):
    LOW  = 0x00
    HIGH = 0xFF


class PinView:
    def __init__(self, pin: Pinout, mem: memoryview):
        self._pin = pin
        self._mem = mem

    def close(self):
        del self._mem


class DigitalPin(PinView):
    @property
    def state(self) -> PinState:
        return PinState(self._mem[1])

    @state.setter
    def state(self, state: PinState):
        self._mem[1] = state.value

    def set(self):
        self.state = PinState.HIGH

    def reset(self):
        self.state = PinState.LOW
    
    def toggle(self):
        self.state = PinState.HIGH if self.state is PinState.LOW else PinState.LOW


class PWMPin(PinView):
    @property
    def duty_cycle(self) -> float:
        return self._mem[1] / 255.0 * 100.0
    
    @duty_cycle.setter
    def duty_cycle(self, duty: float):
        self._mem[1] = int(duty / 100.0 * 255.0)

    @property
    def frequency_khz(self) -> float:
        raw_value = (self._mem[2] << 8) + self._mem[3]
        return raw_value / 65536.0 * 10000.0

    @frequency_khz.setter
    def frequency_khz(self, freq: float):
        value = int(freq * 65536.0 / 10000.0)
        self._mem[2] = value >> 8
        self._mem[3] = value & ((1 << 8) - 1)

    def set(self, duty: float, freq_khz: float):
        self.duty_cycle = duty
        self.frequency_khz = freq_khz
    
    def reset(self):
        self.duty_cycle = 0
        self.frequency_khz = 0
