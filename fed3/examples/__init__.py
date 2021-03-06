# -*- coding: utf-8 -*-
'''Example FED3 data for practice & demonstration of fed3.'''

__all__ = ['load_examples']

import os
import sys
import warnings

from fed3.core.fedfuncs import load

# module variables
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DATA = {}

def load_examples(key):
    '''
    Load the example data linked to a given key.

    Parameters
    ----------
    key : str
        Example to load.

    Raises
    ------
    KeyError
        Unrecognized key.

    Returns
    -------
    list
        FED3 example data, as a list of FEDFrame objects.

    '''

    try:
        return DATA[key]
    except KeyError:
        raise KeyError(f"No matching key '{key}'; options are: "
                       f"{list(DATA.keys())}")

def _build_examples():
    '''Load all the FED3 example data.  To be called on start up.'''
    if not os.path.isdir(DATADIR):
        warnings.warn("Unable to find fed3 example data directory; unable "
                      "to load example data.", RuntimeWarning)
        sys.exit()

    # main loop for loading data
    for folder in os.listdir(DATADIR):

        fullfolder = os.path.join(DATADIR, folder)
        if not os.path.isdir(fullfolder): continue;
        l = []

        for file in os.listdir(fullfolder):

            name, ext = os.path.splitext(file)
            if ext not in ['.csv', '.xlsx']: continue;
            fullfile = os.path.join(fullfolder, file)
            l.append(load(fullfile, deduplicate_index='keep_first'))

        DATA[folder] = l

_build_examples()