# -*- coding: utf-8 -*-
"""
This is the command line interface for PoToMato

Created on Tue Mar 14 15:30:10 2023

Adapted from Mokapot by @wfondrie

@author: Daniel J Geiszler
"""
import sys
import time
import logging

from os.path import basename

import numpy as np

from parsers.parse_ionquant import read_ionquant_protein
from config import Config

def main():
    """The CLI entry point"""
    start = time.time()
    
    # Get command line arguments
    config = Config()
    config.args
    
    # Setup logging
    verbosity_dict = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        }

    logging.basicConfig(
        format=("[{levelname}] {message}"),
        style="{",
        level=verbosity_dict[config.verbosity],
        )

    # Parse input
    parse_prot_fin = get_parser(config, "protein")
    prot_data = parse_prot_fin(
        config.protfile,
        config.condition_tags,
        config.use_maxlfq
       )
    


def get_parser(config, fin_level="protein"):
    """Figure out which parser to use
    
    Currently will only accept protein level data until inference from peptides
    is implemented.

    Parameters
    ----------
    config : argparse object
        DESCRIPTION.
    fin_level : TYPE, optional
        DESCRIPTION. The default is "protein".

    Returns
    -------
    callable
        returns the correct parser for the files

    """
    
    if fin_level == "protein":
        if config.protfile is not None:
            if config.protformat == "ionquant":
                return read_ionquant_protein
            else:
                logging.warning(
                    "Protein input file (%s) is not a recognized format", 
                    config.protfile 
                )
    else:
        logging.warning(
            "Cannot parse input level (%s)", 
            fin_level 
        )
            

if __name__ == '__main__':
    main()