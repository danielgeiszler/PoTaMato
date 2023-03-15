# -*- coding: utf-8 -*-
"""
This is the command line interface for PoTaMato

Created on Tue Mar 14 15:30:10 2023

Adapted from Mokapot by @wfondrie

@author: Daniel J Geiszler
"""

import time
import logging

from parsers.parse_ionquant import read_ionquant_protein
from config import Config
from season import season
from roast import roast

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
    prots = parse_prot_fin(
        config.protfile,
        config.condition_tags,
        config.use_maxlfq
       )
    
    # Season your datasets with some preprocessing
    season(prots=prots, transform="log2") # Todo implement log2 param
    
    # Roast your datasets with some modeling
    roast(model="prot_limma", prots=prots)


def get_parser(config, fin_level="protein"):
    """Figure out which parser to use
    
    Currently will only accept protein level data until inference from peptides
    is implemented.

    Parameters
    ----------
    config : argparse object
    fin_level : str, optional
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