# Conditions indicate weather a TestStep was successful or not based on the
# VMCU state

from abc import ABC, abstractmethod

# All conditions should inherit this one
class Condition(ABC):

    # returns a value when the condition passes or throws a
    # ConditionFailedException otherwise
    @abstractmethod
    async def check(self): ...


# All condition failure exceptions should inherit this one
class ConditionFailedException(Exception):

    def __str__(self):
        return "condition failed"


# Always gets fulfilled
class Fulfilled(Condition):

    async def check(self):
        return True


# Always fails
class Failed(Condition):

    async def check(self):
        raise ConditionFailedException()


# Negates the result of the condition
class Not(Condition):

    def __init__(self, condition: Condition):
        self._condition = condition

    async def check(self):
        try:
            fulfilled = await self._condition.check()
        except ConditionFailedException as failed:
            return failed
        
        raise Not.Fulfilled(fulfilled)


    class Fulfilled(ConditionFailedException):

        def __init__(self, result):
            self.result = result

        def __str__(self):
            return f"condition fulfilled: {self.result}"
