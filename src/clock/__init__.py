
from collections.abc import Callable
from multiprocessing import shared_memory
from threading import Thread
from typing import Any, Iterable, Mapping

import ischedule

from .timer import Timer, TimerEvent


class Clock(Thread):
    # Crates the clock sync thread, the control memory zone must be created beforehand!
    def __init__(self, shm_name: str, target_pid: int, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self._mock_ctrl = shared_memory.SharedMemory(
            name=f"vmcu__ctrl__{shm_name}",
            create=False,
            size=self._pins * self._pin_byte_size
        )

        self._target = target_pid
        self._timers = []

    def add_timer(self, event: TimerEvent, delay_sec: float):
        self._timers.append(Timer(event, self._mock_ctrl[0], self._target, delay_sec))

    def run(self):
        ischedule.reset()
        for timer in self._timers:
            ischedule.schedule(timer.tick, timer.delay)
        
        ischedule.run_loop()

    def close(self):
        pass # TODO: actually close the thread sending signals