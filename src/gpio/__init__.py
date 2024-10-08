from multiprocessing import shared_memory

from .mode import PinMode, UnusedPinError
from .pinout import Pinout

class GPIOMap:
    _pin_byte_size = 4 # CHANGE THIS VALUE TO MATCH THE FUTURE UNION TYPE

    def __init__(self, name: str):
        self._pins = len(Pinout)

        self.mem = shared_memory.SharedMemory(
            name=f"vmcu__gpio__{name}",
            create=True,
            size=self._pins * self._pin_byte_size
        )

        self._pin_views = {}

    def configure_pin(self, pin: Pinout, mode: PinMode):
        pin_offset = self._pin_offset(pin)
        self.mem.buf[pin_offset] = mode.value

    # Passing a mode ensures the pin is in that mode, either by configuring the
    # pin or throwing an exception if the current mode is not the same
    def pin(self, pin: Pinout, mode: PinMode = None):
        pin_offset = self._pin_offset(pin)
        current_mode = PinMode(self.mem.buf[pin_offset])
        if mode is None:
            mode = current_mode
        elif current_mode is PinMode.NOT_USED:
            self.mem.buf[pin_offset] = mode.value
        elif current_mode is not mode:
            raise InvalidModeError(pin, current_mode, mode)

        pin_mem_slice = self.mem.buf[pin_offset:pin_offset + self._pin_byte_size]
        view = mode.get_view(pin, pin_mem_slice)
        self._pin_views[pin] = view
        return view

    def mem_size(self):
        return len(self.mem.buf)

    def close(self):
        self.mem.close()
        self.mem.unlink()

    def _pin_offset(self, pin: Pinout):
        return pin.value * self._pin_byte_size



class InvalidModeError(Exception):
    def __init__(self, pin: Pinout, current_mode: PinMode, desired_mode: PinMode):
        self.pin = pin
        self.current_mode = current_mode
        self.desired_mode = desired_mode
    
    def __str__(self):
        return f"Tried to access pin {self.pin.name} in {self.desired_mode.name} mode, but it is configured already in {self.current_mode.name} mode"