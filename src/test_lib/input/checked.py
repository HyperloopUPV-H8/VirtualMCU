# Inputs that check some conditions before apply

from .input import Input


# Apply an input after check some conditions defined in a function
class Checked(Input):

    # check_function should return True or raise the considered Exception
    def __init__(self, check_function: function, test_input: Input):
        self._check_function = check_function
        self._input = test_input

    async def apply(self):
        if self._check_function():
            await self._input.apply()
