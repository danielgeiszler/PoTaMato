# -*- coding: utf-8 -*-
import logging

import pandas as pd


LOGGER = logging.getLogger(__name__)

def read_ionquant_protein(
        prot_fin,
        condition_tags=None,
        use_maxlfq=None,
        copy_data=True
):
    """
    

    Parameters
    ----------
    prot_fin : path to input or pandas dataframe
        DESCRIPTION.
    condition_tags : TYPE
        DESCRIPTION.
    use_maxlfq : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    """
    logging.info("Parsing IonQuant protein input...")
    
    if isinstance(prot_fin, pd.DataFrame):
        prot_df = prot_fin.copy(deep=copy_data)
    
    
    df = pd.read_csv(prot_fin, sep='\t')
    
    
    