import time
from threading import Thread
from typing import Iterable

# checks that a function returns true
def check(action, args: Iterable[any] = (), msg: str | None = None):
    if action(*args) == False:
        raise CheckError(msg)

# checks that a function returns successfully in the specified intervals (before a timeout and/or after a min delay)
def completes(action, args: Iterable[any] = (), before: float | None = None, after: float | None = None, msg: str | None = None):
    action_thread = Thread(target=action, args=args, name="check")

    start_time = time.time_ns()
    action_thread.start()
    action_thread.join(timeout = before)
    still_running =  action_thread.is_alive()
    end_time = time.time_ns()
    
    if before is not None and still_running:
        raise TooLateError(msg)

    took = end_time - start_time
    if after is not None and took < (after * NANOSECONDS):
        raise TooEarlyError(msg, took)


# create a function that blocks until the action returns true
def wait_until_true(action):
    def wrapper(args: Iterable[any] = ()):
        def block_until_true():
            result = action(*args)
            while not result:
                result = action(*args)

        return block_until_true

    return wrapper

SECONDS = 1
MILLISECONDS = 1000 * SECONDS
MICROSECONDS = 1000 * MILLISECONDS
NANOSECONDS = 1000 * MICROSECONDS

# turns seconds into seconds, seems dumb, but it is there for consistency and completeness
def seconds(s: float) -> float:
    return s / SECONDS

# turns milliseconds into seconds, intended to be used with functions that get durations as a parameter
def milliseconds(ms: float) -> float:
    return ms / MILLISECONDS

# turns microseconds into seconds, intended to be used with functions that get durations as a parameter
def microseconds(us: float) -> float:
    return us / MICROSECONDS

# turns nanoseconds into seconds, intended to be used with functions that get durations as a parameter
def nanoseconds(ns: float) -> float:
    return ns / NANOSECONDS

class TestException(Exception):
    def __init__(self, name: str, message: str | None = None):
        self._name = name
        self._message = message

    def __str__(self):
        exception_message = "[" + self._name + "]"
        if self._message is not None:
            exception_message += ": " + str(self._message)
        return exception_message


class CheckError(TestException):
    def __init__(self, message = None):
        super().__init__("Check Error", message)

class TooEarlyError(TestException):
    def __init__(self, message = None, took_ns = None):
        super().__init__("Too Early", message)
        self._took_ns = took_ns
    
    def __str__(self):
        message = super().__str__()
        if self._took_ns is not None:
            message += f" ({self._took_ns / NANOSECONDS})"
        return message

class TooLateError(TestException):
    def __init__(self, message = None):
        super().__init__("Too Late", message)
