# Inputs that check some conditions before apply

from .input import Input


# Apply an input after check some conditions defined in a function
class Checked(Input):

    # check_function should raise the considered Exception, otherwise do nothing
    def __init__(self, check_function: function, test_input: Input):
        self._check_function = check_function
        self._input = test_input

    async def apply(self):
        self._check_function()
        await self._input.apply()
