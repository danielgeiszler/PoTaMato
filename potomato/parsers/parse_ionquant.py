# -*- coding: utf-8 -*-
"""
This is the parsers for ionquant input.

Created on Tue Mar 14 15:35:15 2023

Adapted from Mokapot by @wfondrie

@author: Daniel J Geiszler
"""
import logging

import pandas as pd
import numpy as np

from dataset import ProteinDataset

LOGGER = logging.getLogger(__name__)

def read_ionquant_protein(
        prot_fin,
        condition_tags=None,
        use_maxlfq=None,
        copy_data=True
):
    """
    Parses an ionquant combined_protein.tsv file.
    
    This can be made more memory efficient by dropping unused columns and
    using the pandas chunk function. Chunking will make dataframe sorting
    more difficult down the line. gzip can be used for large files
    (see mokapot). Will need to add a column checker for TMT experiments.
    It's safe to assume that if the user already has a large dataframe, then 
    they can handle a copy of it with dropped columns or can make it smaller 
    on their own before passing the dataframe. The whole dataframe interface is
    untested for now. Use at your own risk :). Conditions will be transferred
    to a design matrix at some point, but the string tags will be kept for
    usability for non bioinformaticians.

    Parameters
    ----------
    prot_fin : str/pandas.DataFrame
        path to input or pandas dataframe
    condition_tags : comma separated strings of condition names
        comma separated strings of condition names
    use_maxlfq : bool
        use MaxLFQ intensities if present

    Returns
    -------
    None.
    """
    logging.info("Parsing IonQuant protein input...")
    
    # Get or load dataframe
    if isinstance(prot_fin, pd.DataFrame):
        prot_df = prot_fin.copy(deep=copy_data)
    else:
        prot_df = pd.read_csv(prot_fin, sep='\t', nrows=(10))
        
    # Find all necessary columns, case-insensitive
    prot_col = [c for c in prot_df.columns if c.lower() == "protein"]
    maxlfq_cols = [c for c in prot_df.columns 
                  if "maxlfq intensity" in c.lower()]
    inten_cols = [c for c in prot_df.columns 
                 if ("intensity" in c.lower() 
                 and "maxlfq" not in c.lower())]
    
    # Validate that MaxLFQ columns are present
    if use_maxlfq == True:
        if validate_maxquant_cols(maxlfq_cols) == True:
            target_cols = maxlfq_cols
        else:
            use_maxlfq == False
            target_cols = inten_cols
    else:
        target_cols = inten_cols

    # Todo move columns renaming to here

    # Make condition map from condition tags
    if condition_tags is not None:
        condition_map = {
            condition:i for i,condition 
            in enumerate(condition_tags.split(','))
            }
        sample_to_condition_map = validate_condition_tags(condition_map, 
                                                          target_cols)
        
    # Load relevant columns only to save memory
    # todo this can be chunked and made to read gzipped files I think
    if isinstance(prot_fin, pd.DataFrame):
        drop_cols = [col for col in prot_df.columns if col not in target_cols]
        prot_df.drop(columns=drop_cols)
    else:
        keep_cols = prot_col + target_cols
        prot_df = pd.read_csv(prot_fin, sep='\t', usecols=keep_cols)
    
    # Melt dataframe into long form
    prot_df = pd.melt(prot_df, 
                      id_vars=prot_col, 
                      value_vars=target_cols,
                      var_name="sample",
                      value_name="intensity"
                      )
    
    # Clean columns and intensities
    prot_df.columns = map(str.lower, prot_df.columns)
    prot_df["sample"] = prot_df["sample"].str.replace(
        " maxlfq intensity" if use_maxlfq else " intensity", "",
        case=False, 
        )
        
    # IonQuant uses 0 for undetected proteins, so replace with np.NaN
    prot_df = prot_df.replace(0, np.nan)
    
    # Construct and return ProteinDataset object
    # target_cols/condition_map will need to be reworked once design matrices 
    # are implemented
    return ProteinDataset(
        data=prot_df,
        id_cols=prot_col,
        sample_col="sample",
        intensity_col="intensity",
        condition_map=sample_to_condition_map
        )
        
        
def validate_maxquant_cols(maxlfq_cols):
    status = True
    if maxlfq_cols == []:
        logging.warning(
            "\"use_maxlfq\" set to True but no MaxLFQ \
            intensity columns found. Defaulting to Intensity."
        )
        status = False
    return status

        
def validate_condition_tags(condition_map, target_cols):
    """Validates that the parameters conditions are valid for the input file.
    Checks: 1 that there is at least two samples for each tag
            2 that there are no overlapping sample that are ambiguous

    Parameters
    ----------
    condition_map : dict
        {condition: sample}
    target_cols : list
        list of cols to be checked

    Returns
    -------
    sample_to_condition_map : dict
        maps each sample to to a condition
    """
    # Map conditions to samples
    condition_sample_map = {
        condition:[col for col in target_cols if condition in col.lower()]
        for condition in condition_map.keys()
        }
    cum_cols = []
    # Make sure there is at least 2 for each tag
    for k,v in condition_sample_map.items():
        if len(v) < 2:
            logging.error(
                "%s columns found matching tag \"%s\".",
                str(len(v)),
                k
                )
            raise ValueError(
                "%s columns found matching tag %s." %
                (str(len(v)), k)
                )
        cum_cols += v
    # Make sure that there are no redundant tags
    if len(set(cum_cols)) != len(cum_cols):
        logging.error(
            "Some columns match multiple tags and cannot be uniquely \
            assigned.",
            k
            )
        raise RuntimeError(
            "Some columns could not be uniquely assigned to a condition tag.\n\
                Please make sure condition tags do not overlap."
            )
    
    # Make sample -> condition map
    sample_to_condition_map = {}
    for k, v in condition_sample_map.items():
        for v2 in v:
            sample_to_condition_map[v2] = k
    
    return sample_to_condition_map
    