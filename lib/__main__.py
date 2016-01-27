#!/usr/bin/env python
# encoding: utf-8

""" CLI tool entry point.
"""

from __future__ import print_function

import sys
from optparse import OptionParser

import json_diff_patch
from .print_style import colorize
from .loader import load


def usage():
    _CMDS = {
        'print': 'Pretty-print a JSON file',
        'diff': 'Diff between two JSON documents',
        'patch': 'Patch a JSON document',
    }
    print("Usage:", sys.argv[0], " <cmd> [options]")
    print("\nAvailable commands:")
    for cmd, info in _CMDS.items():
        print("  ", colorize(cmd, bold=True), "\t", info)


def diff():
    parser = OptionParser()
    parser.add_option("-c", "--color", dest="colors", action="store_true",
                      help="Colorize the output", default=False)
    options, files = parser.parse_args()
    if len(files) < 2:
        print("Need at least 2 JSON files", file=sys.stderr)
        exit(-1)

    try:
        with open(files[0]) as f:
            local = load(f)
    except IOError:
        print('Local not found', file=sys.stderr)
        exit(-1)
    except KeyError:
        print('Path to file not specified', file=sys.stderr)
        exit(-1)

    try:
        with open(files[1]) as f:
            other = load(f)
    except IOError:
        print('Other not found', file=sys.stderr)
        exit(-1)
    except KeyError:
        print('Path to other file not specified', file=sys.stderr)
        exit(-1)

    res = json_diff_patch.diff(local, other)
    json_diff_patch.print_json(res, "/", options.colors)


COMMANDS = {
    'print': json_diff_patch._printer_main,
    'diff': diff,
    'patch': json_diff_patch._patch_main
}


def main():
    if len(sys.argv) < 2:
        usage()
        exit(-1)
    else:
        cmd = sys.argv[1]
        sys.argv = sys.argv[1:]
        try:
            handler = COMMANDS[cmd]
        except KeyError:
            print('Bad command:', cmd, file=sys.stderr)
            exit(-1)

        handler()


if __name__ == '__main__':
    main()
