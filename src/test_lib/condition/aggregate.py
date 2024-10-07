# Conditions that put together multiple other conditions into a single one.

import asyncio
from .condition import Condition, ConditionFailedException


# All the conditions must be met, fails on the first failed condition
class All(Condition):

    def __init__(self, *conditions: Condition):
        self._conditions = conditions

    async def check(self):
        return [await check for check in asyncio.as_completed([
            condition.check() for condition in self._conditions
        ])]


# At least one condition must be met, returns on the first valid condition
class Any(Condition):

    def __init__(self, *conditions: Condition):
        self._conditions = conditions

    async def check(self):
        failures = []
        result = None
        for check in asyncio.as_completed([
            condition.check() for condition in self._conditions
        ]):
            try:
                result = await check
            except Exception as failure:
                failures.append(failure)
        
        if len(failures) == len(self._conditions):
            raise Any.AllFailedError(failures)
    
        return result


    class AllFailedError(ConditionFailedException):

        def __init__(self, failures: list[ConditionFailedException]):
            self.failures = failures

        def __str__(self):
            return f"All conditions failed: {", ".join([str(failure) for failure in self.failures])}"
