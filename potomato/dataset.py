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


class Dataset(ABC):
    """
    Store intensities
    
    :meta private:
    """
    
    @abstractmethod
    def _add_condition_col_from_map(self):
        """
        Adds a new column to dataframe based on condition_map

        Parameters
        ----------
        cond_map : dict
            sample_name -> sample_condition.

        Returns
        -------
        NONE
        """
        
    
    def __init__(
            self,
            data,
            id_cols,
            sample_col,
            intensity_col,
            other_cols=None,
            condition_map=None,
            design_mat=None
            ):
        """Initialize dataset"""
        self._data = data
        self._id_cols = id_cols
        self._sample_col = sample_col
        self._intensity_col = intensity_col
        self._other_cols = other_cols
        self._condition_map=condition_map
        self._design_mat=design_mat
        
    @property
    def data(self):
        return self._data
    
    @property
    def id_cols(self):
        return self._id_cols
    
    @property
    def sample_col(self):
        return self._sample_col
    
    @property
    def intensity_col(self):
        return self._intensity_col
    
    @property
    def other_cols(self):
        return self._other_cols
    
    @property
    def condition_map(self):
        return self._condition_map
    
    @property
    def design_mat(self):
        return self._design_mat

    @property
    def length(self):
        return len(self._data["index"])

    def log2_transform(self):
        self.data[self.intensity_col] = np.log2(
            self.data[self.intensity_col])
    
    
    
class ProteinDataset(Dataset):
    """
    Vessel for protein intensities
    """
    
    def __init__(
            self,
            data,
            id_cols,
            sample_col,
            intensity_col,
            other_cols=None,
            condition_map=None,
            design_mat=None
            ):
        """Initialize dataset"""
        super().__init__(
            data=data,
            id_cols=id_cols,
            sample_col=sample_col,
            intensity_col=intensity_col,
            condition_map=condition_map,
            design_mat=design_mat
            )
        
        self._add_condition_col_from_map()
        

    @property
    def proteins(self):
        return self.data["protein"].values

    
    def _add_condition_col_from_map(self):
        """
        Adds a new column to dataframe based on condition_map

        Parameters
        ----------
        cond_map : dict
            sample_name -> sample_condition.

        Returns
        -------
        None.
        """
        self.data["condition"] = self.data[
            self.sample_col].map(self._condition_map)
    
        