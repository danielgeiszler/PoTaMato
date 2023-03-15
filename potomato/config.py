# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:38:08 2023

Adapted from Mokapot by @wfondrie

@author: Daniel J Geiszler
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
        self._namespace = None
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
        "--protfile",
        default=None,
        type=str,
        help=(
            "protein intensity input file"
            )
        )
    
    parser.add_argument(
        "--protformat",
        default="ionquant",
        type=str,
        choices=["ionquant"],
        help=(
            "protein intensity input file format"
            )
        )
    
    parser.add_argument(
        "--condition_tags",
        default=None,
        type=str,
        help=(
            "comma-separated list of tags, e.g., \"control,treatment\""
            )
        )
    
    
    parser.add_argument(
        "--use_maxlfq",
        default=True,
        type=bool,
        help=(
            "use maxlfq intensities"
            )
        )
    
    parser.add_argument(
       "-v",
       "--verbosity",
       default=2,
       type=int,
       choices=[0, 1, 2, 3],
       help=(
           "Specify the verbosity of the current "
           "process. Each level prints the following "
           "messages, including all those at a lower "
           "verbosity: 0-errors, 1-warnings, 2-messages"
           ", 3-debug info."
       ),   
    )
    
    return parser


def _process_line(line, width, indent):
    line = textwrap.fill(
        line,
        width,
        initial_indent=indent,
        subsequent_indent=indent,
        replace_whitespace=False,
    )
    return line.strip()