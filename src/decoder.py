#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decoder.py
Decode raw register values based on register definitions from parser.
Author: ubeydullahsu

Created: 2025-12-30
"""

def extract_bits (value, offset, width):
    '''
    Extract bits from a value given offset and width

    @param value: Integer value to extract bits from
    @param offset: Bit offset
    @param width: Bit width
    @return: Extracted bits as integer

    '''
    mask = (1 << width) - 1
    return (value >> offset) & mask


def decode_register_value(reg_def, raw_value):
    '''
    Main decoding function
    Decode a raw register value into its fields based on the register definition

    @param reg_def: RegisterDef object
    @param raw_value: Raw integer value of the register
    @return: Dictionary of field names and their decoded values

    '''
    decoded_fields = {}

    for field in reg_def.fields:
        field_value = extract_bits(raw_value, field.bitOffset, field.bitWidth)
        decoded_fields[field.name] = field_value

    return decoded_fields


def format_output(reg_def, decoded_fields):
    '''
    Format the decoded fields into a readable string

    @param reg_def: RegisterDef object
    @param decoded_fields: Dictionary of field names and their decoded values
    @return: Formatted string

    '''
    output = f"Register: {reg_def.name} (0x{reg_def.address:X})\n"
    output += f"Description: {reg_def.desc}\n"
    output += "Fields:\n"

    for field in reg_def.fields:
        value = decoded_fields.get(field.name, 0)
        output += f"  {field.name} (bits {field.bitOffset}:{field.bitOffset + field.bitWidth - 1}): {value} - {field.desc}\n"
        if value == 0:
            output += f"    Note: Field {field.name} has a value of 0, which may indicate a default or uninitialized state. DISABLED\n"
        elif value == 1:
            output += f"    Note: Field {field.name} has a value of 1, which may indicate an enabled or active state. ENABLED\n"
        else:
            pass

    return output