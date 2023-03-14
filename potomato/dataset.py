# -*- coding: utf-8 -*-
"""


Created on Tue Mar 14 18:45:13 2023

@author: Daniel J Geiszler
"""


import logging
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class ProteinDataset(ABC):
    """
    Store protein-centric intensities
    
    :meta private:
    """
    
    def __init__(
            self,
            data,
            target_col #todo will long or short format be faster?
            ):
        """Initialize dataset"""
        self._data = data
        self._target_col = target_col
    
    