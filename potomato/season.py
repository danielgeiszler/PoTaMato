# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 22:53:56 2023

@author: Daniel J Geiszler
"""

def season(prots=None,
           peps=None,
           transform=None,
           scale=None
           ):
    """
    Preprocesses datasaets to prep for modeling.

    Parameters
    ----------
    prots : protein dataset, optional
        The default is None.
    peps : peptide dataset, optional
        The default is None.
    transform : str, optional
        Accepts parameters for transformation. These ultimately call prot- or
        peptide-level dataset class functions to perform the transformation on
        the data. Currently implemented:
            1. log2
        The default is None.
    scale : str, optional
        Rescales/centers data. Not currently implemented because ionquant does
        scaling internally. Might want to rename this. The default is None.

    Returns
    -------
    None.
    """
    
    # Todo This blocl will eventually have logic determing transformations
    # basedd on input and model
    preprocessProts(prots, transform, scale)


def preprocessProts(prots, transform=None, scale=None):
    if transform == 'log2':
        prots.log2_transform