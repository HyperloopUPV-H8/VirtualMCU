# A test is a series of steps that can either fail or be succesfull

import asyncio

from ..condition.condition import ConditionFailedException
from .step import TestStep


class Test:

    def __init__(self, *steps: TestStep, timeout_s: float = None):
        self._steps = steps
        self._timeout = timeout_s

    async def run(self):
        async with asyncio.timeout(self._timeout):
            for i, step in enumerate(self._steps):
                try:
                    result = await step.run()
                    self.notify_success(i, result)
                except ConditionFailedException as reason:
                    self.notify_failure(i, reason)
    
    def notify_success(self, step: int, result):
        print(f"[success] step {step}: {str(result)}")
    
    def notify_failure(self, step: int, reason: ConditionFailedException):
        print(f"[failed!] step {step}: {str(reason)}")
