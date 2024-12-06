# A test step simplifies executing inputs and checking conditions

import asyncio
from ..input import Input
from ..condition import Condition, ConditionFailedException


# Checks that after applying an input, a condition is fulfilled
class TestStep:

    # concurrent_check makes the condition run at the same time as the input
    # timeout_s sets a max delay for the test step to complete, otherwise it fails
    def __init__(self, test_input: Input, condition: Condition, timeout_s: float | None = None, concurrent_check = False):
        self._input = test_input
        self._condition = condition
        self._timeout = timeout_s
        self._concurrent_check = concurrent_check

    async def run(self):
        async with asyncio.timeout(self._timeout):
            if self._concurrent_check:
                return (await asyncio.gather([
                    self._input.apply(), self._condition.check()
                ]))[1]
            else:
                await self._input.apply()
                return await self._condition.check()
