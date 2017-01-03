import threading
import subprocess
from typing import Callable


def listen_process(process: subprocess.Popen,
                   stdout_callback: Callable[[str], None],
                   stderr_callback: Callable[[str], None],
                   completion_callback: Callable[[int], None]):

    def _dispatched():

        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()

        while stdout_line or stdout_line:
            if stdout_line:
                stdout_callback(stdout_line)
                stdout_line = process.stdout.readline()
            elif stderr_line:
                stderr_callback(stderr_line)
                stderr_line = process.stderr.readline()

        completion_callback(process.wait())

    thread = threading.Thread(target=_dispatched)
    thread.start()
