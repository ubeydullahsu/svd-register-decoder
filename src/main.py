#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py
Main entry point for the SVD register decoder.
Author: ubeydullahsu

Created: 2025-12-30
"""

import argparse
from parser import parse_svd
from decoder import decode_register_value, format_output
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def show_banner():
    console = Console()

    pink = "deep_pink3"
    lila = "plum2"
    soft_purple = "medium_purple2"
    sparkle_white = "grey93"
    

    # Jellyfish ASCII (my spirit animal)
    jellyfish = f"""
    [{pink}]  _---_  [/{pink}]
    [{pink}] (     ) [/{pink}]
    [{lila}]  | | | | [/{lila}]
    [{soft_purple}]  || || [/{soft_purple}]
    """

    title_text = Text()
    title_text.append("SVD-REGISTER-DECODER", style=f"bold {pink}")
    
    about_text = Text()
    about_text.append("\nVersion: 0.1\n", style=lila)
    about_text.append("Author: ubeydullahsu (a.k.a derya kara ⋅˚₊‧ ଳ ‧₊˚ ⋅)\n", style=soft_purple)
    about_text.append("Github: https://github.com/ubeydullahsu/svd-register-decoder", style="italic grey70")

    # Create banner panel
    banner_panel = Panel(
        Text.assemble(title_text, about_text),
        subtitle=f"[{pink}]Happy Debugging![/{pink}]",
        border_style=lila,
        padding=(1, 2)
    )

    console.print(jellyfish, justify="center")
    console.print(banner_panel)
    console.print("\n" + "─" * 60 + "\n", style=soft_purple)


def get_args():
    '''
    Parse command line arguments
    @return: Parsed arguments

    '''
    parser = argparse.ArgumentParser(description="SVD Register Decoder CLI")
    parser.add_argument("--svd", help="Path to the SVD file", required=True)
    parser.add_argument("--addr", help="Register address to decode (hex format, e.g., 0x40021000)", required=True)
    parser.add_argument("--val", help="Raw register value to decode (hex format, e.g., 0x00000001)", required=True)
    
    return parser.parse_args()


def normalize_hex(value_str):
    '''
    Normalize hex string to integer

    @param value_str: Hex string (e.g., "0x1A")
    @return: Integer value

    '''
    try:
        return int(value_str, 0)
    except ValueError:
        print(f"Invalid hex value: {value_str}")
        exit(1)
    
    
if __name__ == "__main__":

    show_banner()

    args = get_args()

    svd_file = args.svd
    register_address = normalize_hex(args.addr)
    raw_value = normalize_hex(args.val)

    # Parse the SVD file to get the memory map
    try:
        memory_map = parse_svd(svd_file)
    except FileNotFoundError:
        print(f"SVD file not found: {svd_file}")
        exit(1)
    except Exception as e:
        print(f"Critical Error: {e}")
        exit(1)

    # Find the register definition
    if register_address not in memory_map:
        print(f"Register address 0x{register_address:08X} not found in memory map.")
    else:
        reg_def = memory_map[register_address]

        # Decode the raw register value
        decoded_fields = decode_register_value(reg_def, raw_value)

        # Format and print the output
        output = format_output(reg_def, decoded_fields)
        print(output)