
import locale
import os
import select
import signal
import sys
import termios
import threading
import time
import tty
import termios
import fcntl
import os

from typing import (
    Callable,
    ContextManager,
    Type,
    TextIO,
    Optional,
    List,
    Union,
    cast,
    Tuple,
    Any,
    IO
)
READ_SIZE = 1024

from types import TracebackType, FrameType
from .keymap import get_key

def is_main_thread() -> bool:
    return threading.current_thread() == threading.main_thread()

def getpreferredencoding() -> str:
    return locale.getpreferredencoding() or sys.getdefaultencoding()

class Nonblocking(ContextManager):
    """
    A context manager for making an KeyInput stream nonblocking.
    """

    def __init__(self, stream: IO) -> None:
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self) -> None:
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)

    def __exit__(
        self,
        type: Optional[Type[BaseException]] = None,
        value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)


class KeyInput(ContextManager["KeyInput"]):
    """Keypress and control event generator"""

    def __init__(self) -> None:

        self.in_stream = sys.__stdin__
        self.unprocessed_bytes: List[bytes] = []  # leftover from stdin, unprocessed yet

        self.wakeup_read_fd: Optional[int] = None
        self.wakeup_write_fd: Optional[int] = None
        self.readers = []

    # prospective: this could be useful for an external select loop
    def fileno(self) -> int:
        return self.in_stream.fileno()
    
    def __enter__(self) -> "KeyInput":
        # with enter
        self.original_stty = termios.tcgetattr(self.in_stream)
        tty.setcbreak(self.in_stream, termios.TCSANOW)

        # Non-main threads don't receive signals
        if is_main_thread():
            self.wakeup_read_fd, self.wakeup_write_fd = os.pipe()
            wfd = self.wakeup_write_fd
            os.set_blocking(wfd, False)
            signal.set_wakeup_fd(wfd, warn_on_full_buffer=False)

        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]] = None,
        value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        # with exit
        if is_main_thread():
            signal.set_wakeup_fd(-1)
            if self.wakeup_read_fd is not None:
                os.close(self.wakeup_read_fd)
            if self.wakeup_write_fd is not None:
                os.close(self.wakeup_write_fd)
        termios.tcsetattr(self.in_stream, termios.TCSANOW, self.original_stty)

    def get_input(self):
        return self.send(None)
    
    def _wait_for_read_ready_or_timeout(self,timeout):
        """Returns tuple of whether stdin is ready to read and an event.

        If an event is returned, that event is more pressing than reading
        bytes on stdin to create a keyboard KeyInput event.
        If stdin is ready, either there are bytes to read or a SIGTSTP
        triggered by dsusp has been received"""
        remaining_timeout = timeout
        t0 = time.time()
        while True:
            try:
                (rs, _, _) = select.select(
                    [self.in_stream.fileno()]
                    + ([] if self.wakeup_read_fd is None else [self.wakeup_read_fd])
                    + self.readers,
                    [],
                    [],
                    remaining_timeout,
                )
                if not rs:
                    return False, None
                r = rs[0]  # if there's more than one, get it in the next loop
                if r == self.in_stream.fileno():
                    return True, None
                elif r == self.wakeup_read_fd:
                    # In Python >=3.5 select won't raise this signal handler
                    signal_number = ord(os.read(r, 1))
                    if signal_number == signal.SIGINT:
                        raise InterruptedError()
                else:
                    os.read(r, 1024)
                    if self.queued_interrupting_events:
                        return False, self.queued_interrupting_events.pop(0)
                    elif remaining_timeout is not None:
                        remaining_timeout = max(0, t0 + remaining_timeout - time.time())
                        continue
                    else:
                        continue
            except OSError:
                if remaining_timeout is not None:
                    remaining_timeout = max(remaining_timeout - (time.time() - t0), 0)

    def send(self, timeout):
        """Returns an event or None if no events occur before timeout."""
        return self._send(timeout)

    def _send(self, timeout: Union[float, int, None]):
        def find_key() -> Optional[str]:
            """Returns keypress identified by adding unprocessed bytes or None"""
            current_bytes = []
            while self.unprocessed_bytes:
                current_bytes.append(self.unprocessed_bytes.pop(0))
                e = get_key(
                    current_bytes,
                    getpreferredencoding(),
                    full=len(self.unprocessed_bytes) == 0,
                )
                if e is not None:
                    return e
            if current_bytes:  # incomplete keys shouldn't happen
                raise ValueError("Couldn't identify key sequence: %r" % current_bytes)
            return None

        time_until_check = timeout

        # try to find an already pressed key from prev KeyInput
        e = find_key()
        if e is not None:
            return e

        stdin_ready_for_read, event = self._wait_for_read_ready_or_timeout(
            time_until_check
        )
        if event:
            return event
        if not stdin_ready_for_read:
            return None

        num_bytes = self._nonblocking_read()
        if num_bytes == 0:
            # thought stdin was ready, but not bytes to read is triggered
            # when SIGTSTP was send by dsusp
            return None

        e = find_key()
        assert e is not None
        return e

    def _nonblocking_read(self) -> int:
        """Returns the number of characters read and adds them to self.unprocessed_bytes"""
        with Nonblocking(self.in_stream):
            try:
                data = os.read(self.in_stream.fileno(), READ_SIZE)
            except BlockingIOError:
                return 0
            if data:
                self.unprocessed_bytes.extend(data[i : i + 1] for i in range(len(data)))
                return len(data)
            else:
                return 0

