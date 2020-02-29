# pystrace

Python library and command line tool for collecting strace events

## Purpose

This library works as wrapper for strace generating syscall events, this events can be used by applications for system calls activity analisys.

In order to handle long executions without generating massive aummounts of logs, the library creates a named FIFO and an extra process where the strace is executed outputing to the FIFO. The main process consumes all the data and generates the corresponding events.

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