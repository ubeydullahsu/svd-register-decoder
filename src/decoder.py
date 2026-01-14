#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decoder.py
Decode raw register values based on register definitions from parser.
Author: ubeydullahsu

Created: 2025-12-30
"""
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import io

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
    output = f"Register: {reg_def.name} (0x{reg_def.address:08X})\n"
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


def format_output_gdb(reg_def, decoded_fields):
    """
    Convert decoded register fields into a rich-formatted string for GDB output.

    @param reg_def: RegisterDef object
    @param decoded_fields: Dictionary of field names and their decoded values
    @return: Formatted string with rich styling

    """
    # for capturing rich output as string (for GDB console)
    console = Console(file=io.StringIO(), force_terminal=True, width=100)

    # Title Panel (Register Name and Description)
    header_text = Text()
    header_text.append(f"Register: ", style="bold orchid")
    header_text.append(f"{reg_def.name}", style="bold white")
    header_text.append(f" (0x{reg_def.address:08X})\n", style="pale_turquoise1")
    header_text.append(f"Desc: ", style="bold sky_blue1")
    header_text.append(f"{reg_def.desc}", style="italic white")

    console.print(Panel(header_text, box=box.ROUNDED, border_style="plum1"))

    # Fields Table Panel
    table = Table(
        show_header=True, 
        header_style="bold hot_pink", 
        box=box.SIMPLE,
        row_styles=["none", "dim"] # Alternating row styles
    )
    
    table.add_column("Bits", style="cyan", justify="center")
    table.add_column("Field Name", style="bold sea_green1")
    table.add_column("Value", justify="center")
    table.add_column("Status", style="italic")
    table.add_column("Description", style="grey78")

    for field in reg_def.fields:
        value = decoded_fields.get(field.name, 0)
        bit_range = f"{field.bitOffset + field.bitWidth - 1}:{field.bitOffset}"
        
        # Color coding based on value
        if value == 0:
            val_str = Text(str(value), style="bold grey62")
            status = Text("OFF", style="bold misty_rose1")
        elif value == 1:
            val_str = Text(str(value), style="bold gold1")
            status = Text("ON", style="bold chartreuse1")
        else:
            val_str = Text(hex(value), style="bold light_salmon3")
            status = Text("DATA", style="bold sky_blue1")

        table.add_row(
            bit_range,
            field.name,
            val_str,
            status,
            field.desc
        )

    console.print(table)

    return console.file.getvalue()