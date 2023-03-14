# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:38:08 2023

@author: Daniel Geiszler
"""


import argparse
import textwrap


class PotomatoHelpFormatter(argparse.HelpFormatter):
    """Format help text to keep newlines and whitespace"""

    def _fill_text(self, text, width, indent):
        text_list = text.splitlines(keepends=True)
        return "\n".join(_process_line(l, width, indent) for l in text_list)



class Config:
    """
    PoToMato config options
    
    Options can be specified as command line arguments
    """
    
    def __init__(self, parser=None):
        """Initialize config options"""
        if parser is None:
            self.parser = _parser()
        else:
            self.parser = parser
            
    @property
    def args(self):
        """Collect args lazily."""
        if self._namespace is None:
            self._namespace = vars(self.parser.parse_args())

        return self._namespace

    def __getattr__(self, option):
        return self.args[option]
    
def _parser():
    """Config file parser"""
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "protein_file",
        type=str,
        help=(
            "Protein intensity input file"
            )
        )

def _process_line(line, width, indent):
    line = textwrap.fill(
        line,
        width,
        initial_indent=indent,
        subsequent_indent=indent,
        replace_whitespace=False,
    )
    return line.strip()