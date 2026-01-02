#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
parser.py
Parse SVD files into register definitions and generate memory map.
Author: ubeydullahsu

Created: 2025-12-30
"""
import xml.etree.ElementTree as ET
import os
import json

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

def parse_filename_without_ext(path):
    """
    Given a file path, returns only the file name without extension.    
    @param path: Full file path as string
    @return: File name without extension as string
    Example: "C:\\...\\STM32F401.svd" -> "STM32F401"

    """
    if not path:
        return ""
    base = os.path.basename(path)
    name, _ = os.path.splitext(base)
    return name

def save_memory_map_as_json_database(memory_map, file_path):
    '''
    Save memory map as a JSON database

    @param memory_map: Dictionary representing memory map {address: RegisterDef}
    @param file_path: Path to save the JSON file
    @return: None

    '''

    json_map = {}
    for address, register in memory_map.items():
        json_map[address] = {
            "name": register.name,
            "address": register.address,
            "size": register.size,
            "access": register.access,
            "desc": register.desc,
            "fields": [
                {
                    "name": field.name,
                    "bitOffset": field.bitOffset,
                    "bitWidth": field.bitWidth,
                    "desc": field.desc
                } for field in register.fields
            ]
        }

    with open(file_path, 'w') as json_file:
        json.dump(json_map, json_file, indent=4)

    print("memory map saved to json database")


def parse_svd(file_path):
    '''
    Main function to parse SVD file and generate memory map

    @param file_path: Path to the SVD file
    @return: Dictionary representing memory map {address: RegisterDef}

    '''

    database_file_path = "database/" + parse_filename_without_ext(file_path) + ".json"

    if os.path.exists(database_file_path):
        with open(database_file_path, 'r') as json_file:
            json_map = json.load(json_file)
        
        memory_map = {}
        for address_str, reg_data in json_map.items():
            address = int(address_str)
            reg_obj = RegisterDef(
                name=reg_data["name"],
                address=reg_data["address"],
                size=reg_data["size"],
                access=reg_data["access"],
                desc=reg_data["desc"]
            )
            for field_data in reg_data["fields"]:
                field_obj = FieldDef(
                    name=field_data["name"],
                    bitOffset=field_data["bitOffset"],
                    bitWidth=field_data["bitWidth"],
                    desc=field_data["desc"]
                )
                reg_obj.add_field(field_obj)
            memory_map[address] = reg_obj
        print("memory map loaded from json database")

    else:
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

        print("memory map created from svd file")
        save_memory_map_as_json_database(memory_map, database_file_path)

    # TO DO: Namespace management if root.findall cannot find elements. xlmns may be needed.

    # Some testing
    print(memory_map[1073816320].name)
    print(memory_map[1073816320].address)
    print(memory_map[1073816320].size)
    print(memory_map[1073816320].access)
    print(memory_map[1073816320].desc)
    pretty(memory_map)  # Pretty print the register details
    
    return memory_map

# testing whole file
parse_svd("C:\github_ws\svd-register-decoder\data\stm32\stm32f4\STM32F401.svd")