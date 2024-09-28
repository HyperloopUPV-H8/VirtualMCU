import signal
import subprocess


class UserCode:
    def __init__(self, name: str, args: list[str]):
        self.name = name
        self._args = args
        self._process = None
    
    def start(self):
        if self._process is not None:
            raise UserCode.AlreadyRunningError(self.name)
        self._process = subprocess.Popen(self._args)
        # TODO: initialize shared memory, clock, etc.
    
    def signal(self, sig: signal.Signals):
        if self._process is None:
            raise UserCode.NotRunningError(self.name)
        self._process.send_signal(sig.value)

    def stop(self):
        if self._process is None:
            raise UserCode.NotRunningError(self.name)
        self._process.terminate()

    def force_stop(self):
        if self._process is None:
            raise UserCode.NotRunningError(self.name)
        self._process.kill()


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
