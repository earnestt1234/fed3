# -*- coding: utf-8 -*-
'''This package provides example data for fed3.  The package comes
bundled with some CSV files of FED3 data.  These can be loaded via
fed3, returning FEDFrames.

fed3 uses this package to create reproducible examples for the documentation.

Data included in the package are all intended to be taken from real fed3
experiments.  If you have data you would like to contribute as an example,
please raise an issue on GitHub.

Datasets
-----

- `justin`: Seven FEDs with data collected over a long-term experiment (10 days).
These data represent FED3 data from multiple recordings, already concatenated.
Data were collected in "ProRat2" mode.  The data show pellet
retrieval in response to an active left poke.  '''

__all__ = ['list_examples', 'load_examples']

import os
import sys
import warnings

from fed3.core.fedfuncs import load

# module variables
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DATA = {}

def list_examples():
    '''
    List all the available example data sets - specifically the string
    keys which can be provided to `load_examples()`.

    Returns
    -------
    list
        All avaiable keys.
    '''

    return list(DATA.keys())

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
    for folder in sorted(os.listdir(DATADIR)):

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