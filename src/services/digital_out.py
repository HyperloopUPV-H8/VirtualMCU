
# EXAMPLE CODE
class DigitalOutService:
    def __init__(self, pin: Pinout):
        self._pin = SharedMemory.get_pin(pin)

    def is_on(self):
        return self._pin.data.is_on
