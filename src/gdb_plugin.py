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

from parser import parse_svd_gdb    
from decoder import decode_register_value, format_output_gdb

# insert the path to the current directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SVDPeekCommand(gdb.Command):
    """GDB command decoder using SVD files. Usage: svd_peek <address>"""

    def __init__(self):
        super(SVDPeekCommand, self).__init__("svd_peek", gdb.COMMAND_USER)
        self.memory_map = None # Lazy loading of memory map

    def get_architecture_name(self):
        # Get the architecture name from GDB. Program must be running.
        try:
            frame = gdb.selected_frame()
            arch = frame.architecture().name()
            return arch
        except gdb.error:
            return None

    def load_memory_map(self):
        if self.memory_map is None:
            # To Do: Find a way to specific SVD file path dynamically
            chip_name = self.get_architecture_name()
            if chip_name is None:
                print("[ ૮₍ ˃ ⤙ ˂ ₎ა ] Unable to determine architecture. Is the program running? [y/n]")
                if input().lower() != 'y':
                    print("What is the chip name? If you dont know press enter to continue.")
                    chip_name = input().strip()
                else:
                    print("[ ૮₍ ˃ ⤙ ˂ ₎ა ] Execute command after running the program. Exiting.")
                    exit(1)
            
            self.memory_map = parse_svd_gdb(chip_name)
            
        return self.memory_map

    def read_memory_address(self, address, size=4):
        # Read 32-bit address from GDB
        try:
            inferior = gdb.selected_inferior()
            mem = inferior.read_memory(address, size)
            return int.from_bytes(mem, byteorder='little')
        except gdb.MemoryError:
            return None

    def invoke(self, arg):
        # main method called when svd_peek command is used

        # Parse arguments (Hex string to integer)
        argv = gdb.string_to_argv(arg)

        if not argv:
            print("[ ⋅˚₊‧ ଳ ‧₊˚ ⋅ ] Usage: svd_peek <address>")
            return
        
        try:
            target_addr = int(argv[0], 16)
        except ValueError:
            print("[ ૮₍ ˃ ⤙ ˂ ₎ა ] Invalid address format. Please provide a hexadecimal address.")
            return
        
        memory_map = self.load_memory_map()
        if memory_map is None:
            print("[ ૮₍ ˃ ⤙ ˂ ₎ა ] Failed to load SVD memory map.")
            return
        
        if target_addr not in memory_map:
            print(f"[ ૮₍ ˃ ⤙ ˂ ₎ა ] Address 0x{target_addr:X} not found in SVD memory map.")
            return

        register_value = self.read_memory_address(target_addr)
        if register_value is None:
            print("[ ૮₍ ˃ ⤙ ˂ ₎ა ] Failed to read memory. Is the device connected?")
            return

        register_info = memory_map[target_addr]
        decoded_output = decode_register_value(register_info, register_value)
        formatted_output = format_output_gdb(register_info, decoded_output)
        print(formatted_output)