#!/usr/bin/env python
#-*- coding:utf-8 -*-


""" Pretty-printing facility for JSON.
"""


from __future__ import print_function

import json
import sys

from . import path
from .print_style import colorize, check_color_caps
from .loader import load


def print_json(data, jpath, pretty=False, tab_size=4, f=sys.stdout):
    """ Prints JSON in a fancy colorized maner.
    """
    check_color_caps(f)

    def _apply_style(text, *args, **kwargs):
        if pretty:
            return colorize(text, *args, **kwargs)
        else:
            return text

    LBRACE = _apply_style('{', 'blue')
    RBRACE = _apply_style('}', 'blue')
    LSQ = _apply_style('[', 'blue')
    RSQ = _apply_style(']', 'blue')

    def _recursive_print(chunk, indent=0, needs_comma=True, context=None):
        """ Recursively pretty-prints a single JSON atom (@a chunk).
        """
        if isinstance(chunk, dict):
            print(' ' * indent if context == 'array' else '', LBRACE, sep='', file=f)
            l = len(chunk)
            for i, (k, v) in enumerate(sorted(chunk.items()), 1):
                print(' ' * (indent + tab_size), '"',
                      _apply_style(k, 'yellow', bold=True),
                      sep='', end='": ', file=f)
                _recursive_print(v, indent + tab_size, i < l)
            print(' ' * indent, RBRACE, ',' if needs_comma else '', sep='', file=f)
        elif isinstance(chunk, list):
            print(' ' * indent if context == 'array' else '', LSQ, sep='', file=f)
            l = len(chunk)
            for i, item in enumerate(chunk, 1):
                _recursive_print(item, indent + tab_size, i < l, 'array')
            print(' ' * indent, RSQ, ',' if needs_comma else '', sep='', file=f)
        else:
            if context == 'array':
                print(' ' * indent, end='', file=f)

            view = json.dumps(chunk)
            if isinstance(chunk, int):
                view = _apply_style(view, 'red')
            elif isinstance(chunk, float):
                view = _apply_style(view, 'red')
            elif isinstance(chunk, basestring):
                view = _apply_style(view, 'green')
            print(view, ',' if needs_comma else '', sep='', file=f)

    _recursive_print(path.resolve(data, jpath), needs_comma=False)


def main():
    import argparse

    parser = argparse.ArgumentParser("json print")
    parser.add_argument('-c', '--colorize', action='store_true',
                        help='Colorize the output', default=True, dest='pretty')
    parser.add_argument('-p', '--pretty', action='store_true',
                        help='Colorize the output', default=True, dest='pretty')
    parser.add_argument('-f', '--filter',
                        help='Filter using path before printing',
                        default='/', metavar='JPATH')
    parser.add_argument('input', help='Path to the file to be patched',
                        nargs='?', default=sys.stdin,
                        type=argparse.FileType('r'))
    args = parser.parse_args()

    data = load(args.input)
    print_json(data, args.filter, args.pretty)


if __name__ == '__main__':
    main()
