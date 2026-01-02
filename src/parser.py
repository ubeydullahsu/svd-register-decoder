#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
parser.py
Parse SVD files into register definitions and generate memory map.
Author: ubeydullahsu

Created: 2025-12-30
"""
import xml.etree.ElementTree as ET

class FieldDef:
    '''
    Class to represent a field of a register
    '''
    def __init__(self, name, bitOffset, bitWidth, desc = ""):
        self.name = name
        self.bitOffset = bitOffset
        self.bitWidth = bitWidth
        self.desc = desc

class RegisterDef:
    '''
    Class to represent a register
    '''
    def __init__(self, name, address, size, access = "", desc = ""):
        self.name = name
        self.address = address # absolute address (base + offset)
        self.size = size
        self.access = access
        self.desc = desc
        self.fields = []

    def add_field(self, field):
        '''
        Add a field to the register

        @param self: RegisterDef instance
        @param field: FieldDef object to add
        @return: None

        '''
        self.fields.append(field)

    def safe_int_convert(self, value_str):
        try:
            return int(value_str, 16)
        except ValueError:
            return 0
       
def pretty(d, indent=0):
   '''
   useful for printing nested dictionaries
   I used this only for debugging and testing
   
   @param d: Dictionary to print
   @param indent: Indentation level
   @return: None

   '''
   for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))

def parse_svd(file_path):
    '''
    Main function to parse SVD file and generate memory map

    @param file_path: Path to the SVD file
    @return: Dictionary representing memory map {address: RegisterDef}

    '''
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    memory_map = {}
    
    for peripheral in root.findall(".//peripheral"):
        baseAddress = int(peripheral.find("baseAddress").text, 16) 

        for register in peripheral.findall(".//register"):
            addressOffset = int(register.find("addressOffset").text, 16)
            address = baseAddress + addressOffset
            reg_obj = RegisterDef(
                name=register.find("name").text,
                address=address,
                size=int(register.find("size").text, 16),
                access=register.find("access").text if register.find("access") is not None else "",
                desc=register.find("description").text if register.find("description") is not None else ""
            )

            for field in register.findall(".//field"):
                field_obj = FieldDef(
                    name=field.find("name").text,
                    bitOffset=int(field.find("bitOffset").text),
                    bitWidth=int(field.find("bitWidth").text),
                    desc=field.find("description").text if field.find("description") is not None else ""
                )
                reg_obj.add_field(field_obj)

            if address not in memory_map:
                memory_map[address] = reg_obj

    # TO DO: Namespace management if root.findall cannot find elements. xlmns may be needed.

    # Some testing
    # print(memory_map[1073816320].name)
    # print(memory_map[1073816320].address)
    # print(memory_map[1073816320].size)
    # print(memory_map[1073816320].access)
    # print(memory_map[1073816320].desc)
    # pretty(memory_map)  # Pretty print the register details
    
    return memory_map

# testing whole file
#parse_svd("C:\github_ws\svd-register-decoder\data\stm32\stm32f4\STM32F401.svd")