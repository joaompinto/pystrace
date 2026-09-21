from pystrace import Tracer
from .cli import parse_cmd_line
from sys import stderr

event_output = stderr # must be a global, cannot be an argument to on_event

def on_event(event):
    print(event, file=event_output)


def main():
    global event_output
    options, args = parse_cmd_line()
    if options.output is stderr:
        event_output = stderr
    else:
        event_output = open(options.output, "w")
    my_tracer = Tracer(
        args,
        on_event,
        filter_syscalls=options.filter_syscalls,
        filter_return=options.filter_return,
        timeout=int(options.timeout) if options.timeout else None,
        as_jsonl=options.jsonl,
        debug=options.debug,
    )
    exit_code = my_tracer.run()
    if exit_code != 0:
        print(f"ERROR: Terminated with exit code {exit_code}", file=stderr)
        exit(exit_code)


if __name__ == "__main__":
    main()
