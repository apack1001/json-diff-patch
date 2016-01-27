#!/usr/bin/env python
# coding: utf-8


""" Utility set for JSON configuration files handling.

    Provides:
        * pretty-printing and sed-like editing JSON configs;
        * parsing and reading values;
        * writeback facility;
        * diff'ing JSON documents in JSON Patch format.
"""

from __future__ import print_function

from .printer import print_json, main as _printer_main
from .diff import diff
from .patch import patch, main as _patch_main
from .loader import load, loads
