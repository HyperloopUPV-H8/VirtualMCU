# Inputs that are applied on different timings

import asyncio
from .input import Input


# Apply an input after a delay
class After(Input):

    def __init__(self, delay_s: float, test_input: Input):
        self._delay = delay_s
        self._input = test_input

    async def apply(self):
        await asyncio.sleep(self._delay)
        await self._input.apply()
