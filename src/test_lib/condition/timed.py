# Conditions that ensure timely fulfillment of other conditions

import asyncio
from .condition import Condition, ConditionFailedException

seconds = 1
milliseconds = seconds / 1000
microseconds = milliseconds / 1000
nanoseconds = microseconds / 1000


# The condition must be met before the delay
class Before(Condition):

    def __init__(self, delay_s: float, condition: Condition):
        self._delay = delay_s
        self._condition = condition

    async def check(self):
        async with asyncio.timeout(self._delay):
            return await self._condition.check()


# The condition must only be met after the delay
class After(Condition):

    def __init__(self, delay_s: float, condition: Condition):
        self._delay = delay_s
        self._condition = condition

    async def check(self):
        delay_elapsed = False
        for check in asyncio.as_completed([
            self._condition.check(),
            asyncio.sleep(
                self._delay,
                result=After._DelayElapsed()
            )
        ]):
            result = await check
            if isinstance(result, After._DelayElapsed):
                delay_elapsed = True
            elif not delay_elapsed:
                raise After.HappenedBeforeError(result)
            else:
                return result


    class _DelayElapsed: ...


    class HappenedBeforeError(ConditionFailedException):

        def __init__(self, result):
            self.result = result

        def __str__(self):
            return f"condition fulfilled before deadline: {self.result}"


# Delay a condition check
class CheckAfter(Condition):

    def __init__(self, delay_s: float, condition: Condition):
        self._delay = delay_s
        self._condition = condition

    async def check(self):
        await asyncio.sleep(self._delay)
        return await self._condition.check()
