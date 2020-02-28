# pystrace

Python library and command line tool for collecting strace events

## Purpose

This library works as wrapper for strace generating syscall events that may be used by applications for system calls activity analisys.

In order to be able to handle long process executions without massive log generation, the library uses a multiprocess architecture. The main process runs strace with the output being sent to a name FIFO, a secondary process consumes the data from the FIFO, parses, and generates the events.

## Install

```bash
pip3 install --user pystrace
```

## How to use (Lib)
```python
from pystrace import Tracer

def on_event(event):
    print(event)

my_tracer = Tracer(["id"], on_event, filter_syscalls="file", filter_return="successful")
my_tracer.run()
```

## How to use (command ine tool)
```bash
pystrace -- command
```

## Example:
```bash
# Trace only file related syscalls with successful result
pystrace -s file -r successful -- who
```