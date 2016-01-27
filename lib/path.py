#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" JSON paths manipulation utilities: splitting, etc.
"""

import re


class JSONPathError(ValueError): pass


def _split_json_pointer(path):
    """ Splits the given :path treating it as JSON Pointer (RFC 6901).
    """
    result = []
    for key in path.split('/')[1:]:
        try:
            index = int(key)
        except ValueError:
            # The key contains non-digital symbols
            # Skip empty keys
            if key:
                result.append(('object-field', key))
        else:
            # JSON Pointer spec treats numbers as array indices only
            result.append(('array-index', index))

    return result


def _split_json_path(path):
    """ Splits the given :path treating it as JSONPath.

        Currently only supports dot-notation & no advanced features.
    """
    if not path:
        return []

    result = []

    if path[0] == '.':
        skip = 1
    elif path[0] == '[':
        skip = 0
    else:
        raise JSONPathError('Syntax error: should start with "." or "["')

    for key in path.split('.')[skip:]:
        if not key:
            raise JSONPathError('Empty keys are not allowed in JSONPath')

        field_end = key.find('[')
        if field_end < 0:
            # The key doesn't contain brackets
            result.append(('object-field', key))
        elif field_end == 0 and result:
            raise JSONPathError('Keys must start with an alphanumeric')
        else:
            # The key contains at least one array indexing expression
            if field_end > 0:
                result.append(('object-field', key[0:field_end]))

            if not re.match(r'\[\d+\]+', key[field_end:]):
                raise JSONPathError('Invalid syntax in {}'.format(key))

            for index in re.findall(r'\[(\d+)\]', key):
                result.append(('array-index', int(index)))

    return result


def split(path):
    """ Splits the given :path into a list of tuples: (type, name).

        Possible types are:
            * object-field;
            * array-index.

        The types have mean:
            * require certain type of parent sub-document in case it exists;
            * insert a sub-document of certain type otherwise.

        This is the minimal set of types to support both JSON Pointer and
        some basic features of JSONPath.
    """
    if not isinstance(path, basestring):
        raise TypeError("JSON path must be a string")

    if path.startswith('/'):
        return _split_json_pointer(path)
    elif path.startswith('$'):
        return _split_json_path(path[1:])
    else:
        raise JSONPathError("JSON path must start with a slash")


def join(path):
    """ Joins an internal representation of JSON path into a JSONPath
        expression (dot-notation).
    """
    res = '$'
    for t, v in path:
        if t == 'object-field':
            fmt = '.{}'
        elif t == 'array-index':
            fmt = '[{}]'
        res += fmt.format(v)
    return res


def _check_type(t, doc, name):
    if t == 'object-field' and not isinstance(doc, dict):
        raise ValueError('Expected an object for {}'.format(repr(name)))
    elif t == 'array-index' and not isinstance(doc, list):
        raise ValueError('Expected a list')


def _make_nodes(jpath):
    if isinstance(jpath, basestring):
        return split(jpath)
    elif isinstance(jpath, list):
        return jpath
    else:
        raise TypeError('JSON path must be a string or a list of tuples')


def resolve(doc, jpath):
    """ Resolves the given :path against :doc.
    """
    d = doc
    for t, v in _make_nodes(jpath):
        _check_type(t, d, v)
        if v != '':
            d = d[v]

    return d


def create(jpath, value=None):
    """ Create a minimal JSON document, against which the given :path
        can be resolved.

        The final node is initialized with :value.
    """
    def descend(tail):
        if not tail:
            return value

        t, v = tail[0]
        if t == 'object-field':
            d = {v: descend(tail[1:])}
        else:
            d = [None] * v + [descend(tail[1:])]
        return d

    return descend(_make_nodes(jpath))


def find(doc, jpath, joined=False):
    """ Find a minimal subsequence of :path in the JSON document :doc.

        Returns a tuple (found, not_found, doc, reason), where
            * 'found' is the matched parted of :path;
            * 'not_found' is the remainder of the :path;
            * 'doc' is the object pointed by 'found';
            * 'reason' is an explanation of why the matching failed (possible
               values: None - all matched, 'type', 'key', 'index').
    """
    nodes = _make_nodes(jpath)
    d = doc
    reason = None
    i = 0
    for i, (t, v) in enumerate(nodes):
        try:
            _check_type(t, d, v)
        except ValueError:
            reason = 'type'
            break

        try:
            d = d[v]
        except KeyError:
            reason = 'key'
            break
        except IndexError:
            reason = 'index'
            break
    else:
        # Full path has been matched
        i += 1

    if not joined:
        return (nodes[:i], nodes[i:], d, reason)
    else:
        return (join(nodes[:i]), join(nodes[i:]), d, reason)
