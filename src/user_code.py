import signal
import subprocess

from control import CTRLMap
from gpio import GPIOMap


class UserCode:
    def __init__(self, name: str, args: list[str]):
        self.name = name
        self._args = args
        
        self._process = None
        self._gpio_map = None
        self._ctrl_map = None
    
    def start(self):
        if self._process is not None:
            raise UserCode.AlreadyRunningError(self.name)
        self._process = subprocess.Popen(self._args)
        
        self._ctrl_map = CTRLMap(self.name)
        self._gpio_map = GPIOMap(self.name)

    
    def signal(self, sig: signal.Signals):
        if self._process is None:
            raise UserCode.NotRunningError(self.name)
        self._process.send_signal(sig.value)

    def stop(self, timeout: float = None, force: bool = False) -> int:
        if self._process is None:
            raise UserCode.NotRunningError(self.name)

        if force:
            self._process.kill()
        else:
            self._process.terminate()

        retcode = self._process.wait(timeout=timeout)
        self._cleanup()
        return retcode

    def _cleanup(self):
        self._process = None
        if self._gpio_map:
            self._gpio_map.close()
        if self._ctrl_map:
            self._ctrl_map.close()

    class AlreadyRunningError(Exception):
        def __init__(self, name: str):
            self.name = name

        def __str__(self):
            return f"{self.name} user code is already running"


    class NotRunningError(Exception):
        def __init__(self, name: str):
            self.name = name

        def __str__(self):
            return f"{self.name} user code is not running"
