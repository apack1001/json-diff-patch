#!/usr/bin/env python
#-*- coding:utf-8 -*-


""" Functions to patch JSON documents.
"""

from __future__ import print_function

from . import path
from .loader import load


def add(data, jpath, value, replace=False):
    """ Add a new value to the given JSON document :data at JSON-path :path.

        If the the path is already used, then no changes are made.
    """
    match, remainder, d, reason = path.find(data, jpath)

    if reason == 'type':
        raise TypeError('Bad subdoc type after {}'.format(path.join(match)))

    if not reason:
        if replace:
            d = path.resolve(data, match[:-1])
            d[match[-1][1]] = value
    else:
        sub_doc = path.create(remainder[1:], value)
        name = remainder[0][1]
        if reason == 'key':
            d[name] = sub_doc
        elif reason == 'index':
            while len(d) < name:
                d.append(None)
            d.append(sub_doc)

    return data


def replace(data, jpath, value):
    """ Replace the value of the document's subelement at @a path with value
        @a value.
    """
    return add(data, jpath, value, True)


def remove(data, jpath):
    nodes = path.split(jpath)
    d = data
    for t, name in nodes[:-1]:
        if t == 'object-field':
            if not isinstance(d, dict) or name not in d:
                return
        elif t == 'array-index':
            if not isinstance(d, list) or name >= len(d):
                return
        d = d[name]
    try:
        del d[nodes[-1][1]]
    except:
        pass
    return data


def patch(data, patch):
    """ Apply a JSON @a patch to the given JSON object @a data.
    """
    for change in patch:
        if 'add' in change:
            add(data, change['add'], change['value'])
        elif 'replace' in change:
            replace(data, change['replace'], change['value'])
        elif 'remove' in change:
            remove(data, change['remove'])
    return data


def main():
    import argparse
    import sys
    from .printer import print_json

    parser = argparse.ArgumentParser("json patch")
    parser.add_argument('-c', '--colorize', action='store_true',
                        help='Colorize the output', default=True)
    parser.add_argument('-i', '--inplace', action='store_true',
                        help='Edit the input file inplace')
    parser.add_argument('input', help='Path to the file to be patched',
                        type=argparse.FileType('r'))
    parser.add_argument('patch', nargs='*', help='Path to a single patch',
                        type=argparse.FileType('r'), default=[sys.stdin])
    args = parser.parse_args()

    data = load(args.input)

    for patch_file in args.patch:
        data = patch(data, load(patch_file))

    f = open(args.input.name, 'w') if args.inplace else sys.stdout
    print_json(data, "/", args.colorize, f=f)


if __name__ == '__main__':
    main()
