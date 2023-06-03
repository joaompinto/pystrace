from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from sys import stderr
import os
import subprocess
import re


class Tracer:
    def __init__(
        self,
        command_args,
        syscall_callback,
        follow_childs=True,
        filter_syscalls="",
        filter_return="",
        timeout=None,
        debug=False,
    ):
        self.command_args = command_args
        self.syscall_callback = syscall_callback
        self.follow_childs = follow_childs
        self.filter_syscalls = filter_syscalls
        self.filter_return = filter_return
        self.timeout = timeout
        self.debug = debug
        self.parse_regex_ok = re.compile(r"^(\d+)\s*(\w*)\((.*)\) = (\d+)$")
        self.parse_regex_fail = re.compile(
            r"^(\d+)\s*(\w*)\((.*)\) = ([-\d]+)\s*(\w+)\s*(.*)$"
        )

    def _create_log_fifo(self):
        self.temp_dir = TemporaryDirectory()
        fifo_filename = Path(self.temp_dir.name).joinpath("strace")
        self.fifo_filename = fifo_filename
        os.mkfifo(fifo_filename, 0o600)

    def run(self):
        self._create_log_fifo()
        strace_process = Process(
            target=self._run_strace)
        strace_process.start()
        rc = self.handle_strace_data()
        strace_process.join()
        return rc

    def handle_strace_data(self):

        while True:
            with open(self.fifo_filename, 'r') as fifo:
                data = fifo.read()
                while data:
                    # When there is an error during strace, it will not open the fifo
                    # which means we only get  single FIFO item with the rc
                    if data.lstrip("-").isnumeric():
                        rc = int(data)
                        return rc
                    for line in data.splitlines():
                        syscall_data = self.parse_regex_ok.findall(line)
                        if syscall_data:
                            pid, syscall, arguments, result = syscall_data[0]
                            syscall_dict = {
                                "pid": int(pid),
                                "syscall": syscall,
                                "arguments": arguments,
                                "result": int(result),
                            }
                            self.syscall_callback(syscall_dict)
                        else:
                            syscall_data = self.parse_regex_fail.findall(line)
                            if syscall_data:
                                (
                                    pid,
                                    syscall,
                                    arguments,
                                    result,
                                    errno,
                                    errdesc,
                                ) = syscall_data[0]
                                syscall_dict = {
                                    "pid": int(pid),
                                    "syscall": syscall,
                                    "arguments": arguments,
                                    "result": int(result),
                                    "errno": errno,
                                    "errdesc": errdesc,
                                }
                                self.syscall_callback(syscall_dict)
                    data = fifo.read()

    def _run_strace(self):
        strace_args = []
        if self.follow_childs:
            strace_args.append("-f")
        if self.filter_return:
            strace_args += ["-e", f"status={self.filter_return}"]
        if self.filter_syscalls:
            strace_args += ["-e", f"trace={self.filter_syscalls}"]
        strace_args += ["-o", self.fifo_filename]
        if self.debug:
            print("DEBUG ARGS:", strace_args)
        try:
            run_result = subprocess.run(
                ["strace"] + strace_args + self.command_args, capture_output=True,
                timeout = self.timeout
            )
        except subprocess.TimeoutExpired:
            rc = 1
        except FileNotFoundError:
            print("Could not execute 'strace', is it installed?")
            rc = 1
        else:
            rc = run_result.returncode
            if run_result.stdout:
                print(run_result.stdout.strip().decode().strip("\n"))
            if rc != 0:
                print((run_result.stderr.decode().strip("\n")), file=stderr)

        with open(self.fifo_filename, "w") as output:
            output.write(str(rc))


