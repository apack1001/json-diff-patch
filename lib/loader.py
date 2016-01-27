#!/usr/bin/env python
# coding: utf-8

""" JSON loading facilities with support for embedded C++ style comments.

    NOTE: Support for multiline comments is limited for now. */ should be
          placed on its own line, otherwise the parser will fail :(
"""

import json


def _strip_comments(s):
    """ Strips all comments from ``s``, so that it could be passed to
        ``json.loads``.

        TODO-1: Make a cleaner grammar-based parser.
        TODO-2: Add full support for /* .. */ comments.
    """
    meaningful_lines = []
    comment = False

    for line in s.splitlines():
        line = line.strip()
        if not comment:
            if line.startswith('//'):
                continue
            elif line.startswith('/*'):
                comment = True
                continue
            else:
                meaningful_lines.append(line)
        else:  # comment == True
            if line.endswith('*/'):
                comment = False

    return ''.join(meaningful_lines)


def loads(s, *args, **kwargs):
    """ Deserialize ``s`` (a ``str`` or ``unicode`` instance containing a JSON
        document) to a Python object.

        Supports the same set of arguments as ``json.loads``.
    """
    return json.loads(_strip_comments(s), *args, **kwargs)


def load(fp, *args, **kwargs):
    """ Deserialize ``fp`` (a ``.read()``-supporting file-like object
        containing a JSON document) to a Python object.

        Supports the same set of arguments as ``json.load``.
    """
    return loads(fp.read(), *args, **kwargs)
