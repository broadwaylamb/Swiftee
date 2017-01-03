import subprocess
from typing import List
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
                   build_path: str,
                   package_type: PackageType,
                   c_compiler_flags: List[str],
                   swift_compiler_flags: List[str],
                   linker_flags: List[str],
                   stdout_callback,
                   stderr_callback,
                   completion_callback) -> None:

        process = subprocess.Popen(
            [
                SPMPackage.swift_path, SPMPackage.spm_command,
                "init",
                "--type", package_type.value,
                "--chdir", working_directory,
                "--build-path", build_path
            ] +
            ["-Xcc %s" % flag for flag in c_compiler_flags] +
            ["-Xswiftc %s" % flag for flag in swift_compiler_flags] +
            ["-Xlinker %s" % flag for flag in linker_flags],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        listen_process(process, stdout_callback, stderr_callback, completion_callback)

    def __init__(self, manifest_path: str) -> None:
        self.manifest_path = manifest_path
