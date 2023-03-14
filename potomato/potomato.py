# -*- coding: utf-8 -*-
"""
This is the command line interface for PoToMato

Created on Tue Mar 14 15:30:10 2023

@author: Daniel Geiszler
"""
import sys
import time

import numpy as np

from potomato import Config


def main():
    """The CLI entry point"""
    start = time.time()
    
    # Get command line arguments
    parser = Config().parser
    
    # np.random.seed(config.seed) //todo set seed
    
    # Parse datasets
    parse = 


if __name__ == '__main__':
    main()