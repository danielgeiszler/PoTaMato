# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 19:49:38 2023

@author: Daniel J Geiszler
"""

import logging

def roast(model=None,
          prots=None):
    """
    This is the primary modelling function. Subfunctions are called to generate
    models based on which model parameter is used.

    Parameters
    ----------
    model : str, optional
        Calls the type of model. Currently implemented:
            1. prot_limma : estimates protein differential abundance using the
            limma algorithm (without limma-trend)
        The default is None.
        
    prots : protein dataset, optional
        The default is None.

    Returns
    -------
    None.
    """
    if model == "prot_limma":
        roast_protein_limma(prots)
    

def roast_protein_limma(prots):
    for prot in prots.proteins:
        print(prot)
        
        


    
    
    