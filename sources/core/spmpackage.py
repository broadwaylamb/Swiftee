import subprocess
from typing import Callable
from enum import Enum
from .listening import listen_process


class SPMPackage(object):

    swift_path = "/usr/bin/swift"
    spm_command = "package"
    manifest_filename = "Package.swift"

    class PackageType(Enum):
        EMPTY = "empty"
        LIBRARY = "library"
        EXECUTABLE = "executable"
        SYSTEM_MODULE = "system-module"

    @classmethod
    def initialize(cls,
                   working_directory: str,
                   package_type: PackageType,
                   stdout_callback: Callable[[str], None],
                   stderr_callback: Callable[[str], None],
                   completion_callback: Callable[[int], None]) -> None:

        process = subprocess.Popen(
            [
                SPMPackage.swift_path, SPMPackage.spm_command,
                "init",
                "--type", package_type.value,
                "--chdir", working_directory,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        listen_process(process, stdout_callback, stderr_callback, completion_callback)

    def __init__(self, manifest_path: str) -> None:
        self.manifest_path = manifest_path
