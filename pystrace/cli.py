import sys
from optparse import OptionParser


def parse_cmd_line():
    parser = OptionParser()
    parser.add_option(
        "--debug", action="store_true", help="pring debug messages", default=False,
    )
    parser.add_option(
        "--filter-return",
        "-r",
        help="filter matching return status (-e status)",
        dest="filter_return",
        default="",
    )
    parser.add_option(
        "--filter-syscalls",
        "-s",
        help="filter matching syscall expression (-e trace)",
        dest="filter_syscalls",
        default="",
    )
    parser.add_option(
        "--timeout",
        "-t",
        help="set timeout on process execution",
        dest="timeout",
        default=None,
    )
    options, args = parser.parse_args()
    if len(args) == 0:
        print("Usage: {} [options] command".format(sys.argv[0]))
        exit(1)
    return options, args
