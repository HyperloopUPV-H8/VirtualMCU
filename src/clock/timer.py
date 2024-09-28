

from enum import Flag, auto, unique
import signal


@unique
class TimerEvent(Flag):
    HIGH_PRECISION = auto()
    MID_PRECISION  = auto() 
    LOW_PRECISION  = auto()


class Timer:
    def __init__(self, event: TimerEvent, ctrl_mem: memoryview, target_process: int, delay: float):
        self._mem = ctrl_mem
        self.event = event
        self._target_process = target_process
        self.delay = delay

    @property
    def event(self) -> TimerEvent:
        return self._event
    
    @event.setter
    def event(self, event: TimerEvent):
        self._event = event

    def tick(self):
        self._mem[0] |= self.event
        signal.pidfd_send_signal(self._target_process, signal.SIGUSR1)