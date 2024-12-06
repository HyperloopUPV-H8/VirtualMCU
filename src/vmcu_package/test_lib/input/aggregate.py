# Inputs that put togheter multiple other inputs into a single one

import asyncio
from .input import Input


# Applies multiple inputs simultaneously, fails if any input fails
class Multiple(Input):

    def __init__(self, *inputs: Input):
        self._inputs = inputs

    async def apply(self):
        return await asyncio.gather(*[
            test_input.apply() for test_input in self._inputs
        ])
