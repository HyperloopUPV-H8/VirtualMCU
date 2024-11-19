# Inputs are signals sent to the VMCU during tests to check their outputs

from abc import ABC, abstractmethod


# All inputs should inherit from this one
class Input(ABC):

    # returns a value when the input is applied correctly, otherwise
    # throws an exception
    @abstractmethod
    async def apply(self): ...


# All Input failure exceptions should extend this class
class InputFailedException(Exception):

    def __str__(self):
        return "input failed"
