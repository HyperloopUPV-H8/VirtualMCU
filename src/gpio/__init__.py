from multiprocessing import shared_memory
from .pinout import Pinout

# GPIO represents the microcontroller GPIO.
#
# The GPIO gets mapped to Shared Memory on construction and can be later on
# asigned.
#
# Once opened, the GPIO can only be destroyed, not closed. This is to prevent
# resource leaks
class GPIO:
    _pin_byte_size = 4 # CHANGE THIS VALUE TO MATCH THE FUTURE UNION TYPE

    # Creates a new GPIO shared memory. By default the zone is named
    # `vmcu__gpio__{name}`
    def __init__(self, name: str):
        self._pins = len(Pinout)

        self.mem = shared_memory.SharedMemory(
            name=f"vmcu__gpio__{name}",
            create=True,
            size=self._pins * self._pin_byte_size
        )

    # Write raw data to the GPIO shared memory to the specified pin
    def write_pin(self, pin: Pinout, data: bytearray):
        pin_offset = self._pin_offset(pin)
        for i in range(self._pin_byte_size):
            self.mem.buf[pin_offset + i] = data[i]

    # Read raw data from the GPIO shared memory of the specified pin
    def read_pin(self, pin):
        data = bytearray(self._pin_byte_size)
        pin_offset = self._pin_offset(pin)
        for i in range(self._pin_byte_size):
            data[i] = self.mem.buf[pin_offset + i]
        return data

    # Returns the size in bytes of the GPIO shared memory
    def mem_size(self):
        return len(self.mem.buf)

    def __del__(self):
        self.mem.close()
        self.mem.unlink()

    # Calculates the offset in the shared memory of the specified pin
    def _pin_offset(self, pin: Pinout):
        return pin.value * self._pin_byte_size

