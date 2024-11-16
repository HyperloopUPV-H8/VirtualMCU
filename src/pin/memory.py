from enum import Enum, auto, unique
import struct

class PinMemoryView:
    def __init__(self, shm: memoryview):
        self._mem = shm

class DigitalOut(PinMemoryView):
    @unique
    class State(Enum):
        High = True
        Low = False

    @property
    def state(self) -> State: 
        return DigitalOut.State(struct.unpack("=?", self._mem[0:1])[0])

class DigitalIn(PinMemoryView):
    @unique
    class State(Enum):
        High = True
        Low = False

    @property
    def state(self) -> State:
        return DigitalIn.State(struct.unpack("=?", self._mem[0:1])[0])

    @state.setter
    def state(self, state: State):
        struct.pack_into("=?", self._mem[0:1], 0, state)

class ADC(PinMemoryView):
    @property
    def value(self) -> int:
        return struct.unpack("=H", self._mem[0:2])[0]

    @value.setter
    def value(self, value: int):
        struct.pack_into("=H", self._mem[0:2], 0, value)

    @property
    def is_on(self) -> bool:
        return struct.unpack("=?", self._mem[2:3])[0]  

class EXTI(PinMemoryView):
    @property
    def priority(self) -> int:
        return struct.unpack("=L", self._mem[0:4])[0]

    @property
    def is_on(self) -> bool:
        return struct.unpack("=?", self._mem[4:5])[0]
    
    @property
    def trigger_signal(self) -> bool:
        return struct.unpack("=?", self._mem[5:6])[0]
    
    @trigger_signal.setter
    def trigger_signal(self, trigger_signal: bool):
        struct.pack_into("=?", self._mem[5:6], 0, trigger_signal)

    @unique
    class TriggerMode(Enum):
        RisingEdge = 1
        FallingEdge = 0
        BothEdges = 2

    @property
    def trigger_mode(self) -> TriggerMode:
        return EXTI.TriggerMode(struct.unpack("=B", self._mem[6:7])[0])

class Encoder(PinMemoryView):
    @property
    def counter(self) -> int:
        return struct.unpack("=B", self._mem[0:4])[0]
    
    @counter.setter
    def counter(self, counter: int):
        struct.pack_into("=L", self._mem[0:4], 0, counter)
    
    @unique
    class Direction(Enum):
        Forwards = True
        Backwards = False

    @property
    def direction(self) -> Direction:
        return Encoder.Direction(struct.unpack("=?", self._mem[4:5])[0])
    
    @direction.setter
    def direction(self, direction: Direction):
        struct.pack_into("=?", self._mem[4:5], 0, direction.value)
    
    @property
    def is_on(self) -> bool:
        return struct.unpack("=?", self._mem[5:6])[0]

# TODO: data definition missing in C++
class InputCapture(PinMemoryView):
    @property
    def duty_cycle(self) -> int:
        return struct.unpack("=B", self._mem[0:1])[0]
    
    @duty_cycle.setter
    def duty_cycle(self, duty_cycle: int):
        struct.pack_into("=B", self._mem[0:1], 0,duty_cycle)
    @property
    def frequency(self) -> int:
        return struct.unpack("=L", self._mem[1:5])[0]
    
    @frequency.setter
    def frequency(self, frequency: int):
        struct.pack_into("=L", self._mem[1:5], 0,frequency)
    
    
class PWM(PinMemoryView):
    @property
    def duty_cycle(self) -> float:
        return struct.unpack("=f", self._mem[0:4])[0]
    
    @property
    def frequency(self) -> int:
        return struct.unpack("=L", self._mem[4:8])[0]

    @property
    def is_on(self) -> bool:
        return struct.unpack("=?", self._mem[8:9])[0]

    @property
    def dead_time_ns(self) -> int:
        return struct.unpack("=l", self._mem[9:13])[0]
    

class DualPWM(PinMemoryView):
    @property
    def duty_cycle(self) -> float:
        return struct.unpack("=f", self._mem[0:4])[0]
    
    @property
    def frequency(self) -> int:
        return struct.unpack("=L", self._mem[4:8])[0]

    @property
    def is_on(self) -> bool:
        return struct.unpack("=?", self._mem[8:9])[0]

    @property
    def dead_time_ns(self) -> int:
        return struct.unpack("=l", self._mem[9:13])[0]
