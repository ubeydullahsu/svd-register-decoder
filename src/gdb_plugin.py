#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gdb_plugin.py

GDB plugin for SVD register decoder.
Author: ubeydullahsu

Created: 2025-01-06
"""

import gdb
import os
import sys

from parser import parse_svd
from decoder import decode_register_value, format_output


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SVDPeekCommand(gdb.Command):
    """GDB command decoder using SVD files. Usage: svd_peek <address>"""

    def __init__(self):
        super(SVDPeekCommand, self).__init__("svd_peek", gdb.COMMAND_USER)
        self.memory_map = None # Lazy loading of memory map
